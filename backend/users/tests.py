import uuid
from datetime import date, datetime, timedelta

from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from couples.models import Couple
from files.models import File
from lists.models import List, Option
from menu.models import IngType, Ingredients, RecipeType, Recipes, IngInRecipe, Fridge
from plans.models import CalendarPlan, Color, Plan, Repeat
from users.models import Auth, User
from wishes.models import Wish, WishPhoto


class BaseAPITestCase(APITestCase):
    def create_user(self, login_value):
        user = User.objects.create(
            first_name=login_value.title(),
            second_name="Test",
            birth_date=date(2000, 1, 1),
        )
        Auth.objects.create(
            user=user,
            login=login_value,
            password=make_password("password123"),
        )
        return user

    def auth(self, user):
        self.client.force_authenticate(user=user)

    def create_couple(self):
        first = self.create_user("first")
        second = self.create_user("second")
        couple = Couple.objects.create(
            partner=first,
            second_partner=second,
            date_of_start=date(2025, 1, 1),
        )
        return first, second, couple


class AuthAndUsersAPITests(BaseAPITestCase):
    def test_protected_endpoint_requires_authentication(self):
        response = self.client.get("/api/couples/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_registration_login_and_logout(self):
        response = self.client.post(
            "/api/users/",
            {
                "first_name": "Kirill",
                "second_name": "Test",
                "birth_date": "2005-01-01",
                "login": "kirill",
                "password": "password123",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn("password", response.data)

        login_response = self.client.post(
            "/api/auth/login/",
            {"login": "kirill", "password": "password123"},
            format="json",
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertEqual(login_response.data["user"]["login"], "kirill")

        me = self.client.get("/api/users/")
        self.assertEqual(me.status_code, status.HTTP_200_OK)
        self.assertEqual(len(me.data), 1)

        logout_response = self.client.post("/api/auth/logout/")
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)

    def test_user_crud(self):
        user = self.create_user("user1")

        self.auth(user)
        list_response = self.client.get("/api/users/")
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)

        detail_response = self.client.get(f"/api/users/{user.user_id}/")
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)

        patch_response = self.client.patch(
            f"/api/users/{user.user_id}/",
            {"first_name": "Updated"},
            format="json",
        )
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)

        delete_response = self.client.delete(
            f"/api/users/{user.user_id}/"
        )
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_change_password(self):
        user = self.create_user("user2")
        self.auth(user)

        response = self.client.post(
            "/api/auth/change-password/",
            {
                "old_password": "password123",
                "new_password": "newpassword123",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CouplesAPITests(BaseAPITestCase):
    def test_couple_crud(self):
        first = self.create_user("first")
        second = self.create_user("second")
        self.auth(first)

        create = self.client.post(
            "/api/couples/",
            {
                "second_partner": str(second.user_id),
                "date_of_start": "2025-01-01",
            },
            format="json",
        )
        self.assertEqual(create.status_code, status.HTTP_201_CREATED)
        couple_id = create.data["couple_id"]

        get_response = self.client.get("/api/couples/")
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

        patch = self.client.patch(
            f"/api/couples/{couple_id}/",
            {"date_of_start": "2025-02-01"},
            format="json",
        )
        self.assertEqual(patch.status_code, status.HTTP_200_OK)

        stats = self.client.get("/api/couples/stats/")
        self.assertEqual(stats.status_code, status.HTTP_200_OK)

        delete_response = self.client.delete(f"/api/couples/{couple_id}/")
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invite_and_join(self):
        first = self.create_user("invite_first")
        second = self.create_user("invite_second")

        self.auth(first)
        invite = self.client.post("/api/couples/invite/")
        self.assertEqual(invite.status_code, status.HTTP_200_OK)

        cache_code = invite.data["code"]
        self.client.force_authenticate(user=second)
        join = self.client.post(
            "/api/couples/join/",
            {"code": cache_code, "date_of_start": "2025-01-01"},
            format="json",
        )
        self.assertEqual(join.status_code, status.HTTP_201_CREATED)


class WishesAPITests(BaseAPITestCase):
    def test_wishes_crud_and_photos(self):
        first, _, couple = self.create_couple()
        self.auth(first)

        create = self.client.post(
            "/api/wishes/",
            {
                "couple": couple.couple_id,
                "link": "https://example.com/item",
                "wish_name": "Headphones",
                "price": 15000,
                "wish_note": "White",
            },
            format="json",
        )
        self.assertEqual(create.status_code, status.HTTP_201_CREATED)
        wish_id = create.data["wish_id"]

        get_response = self.client.get("/api/wishes/")
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(get_response.data), 1)

        photo = self.client.post(
            f"/api/wishes/{wish_id}/photos/",
            {"wish_photo_link": "https://example.com/photo.jpg"},
            format="json",
        )
        self.assertEqual(photo.status_code, status.HTTP_201_CREATED)

        photos = self.client.get(f"/api/wishes/{wish_id}/photos/")
        self.assertEqual(photos.status_code, status.HTTP_200_OK)
        self.assertEqual(len(photos.data), 1)

        patch = self.client.patch(
            f"/api/wishes/{wish_id}/",
            {"price": 12000},
            format="json",
        )
        self.assertEqual(patch.status_code, status.HTTP_200_OK)

        delete = self.client.delete(f"/api/wishes/{wish_id}/")
        self.assertEqual(delete.status_code, status.HTTP_204_NO_CONTENT)


class RemainingCRUDAPITests(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.first, self.second, self.couple = self.create_couple()
        self.auth(self.first)

    def test_files_crud(self):
        response = self.client.post(
            "/api/files/",
            {
                "couple": self.couple.couple_id,
                "file_name": "doc",
                "file_type": "pdf",
                "file_URL": "https://example.com/doc.pdf",
                "file_note": "test",
                "file_original_name": "document.pdf",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        file_id = response.data["fileid"]
        self.assertEqual(
            self.client.patch(
                f"/api/files/{file_id}/",
                {"file_note": "updated"},
                format="json",
            ).status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            self.client.delete(f"/api/files/{file_id}/").status_code,
            status.HTTP_204_NO_CONTENT,
        )

    def test_lists_and_options_crud(self):
        response = self.client.post(
            "/api/lists/",
            {"couple": self.couple.couple_id},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        list_id = response.data["list_id"]

        option = self.client.post(
            "/api/lists/options/",
            {"list": list_id, "option_name": "Option 1"},
            format="json",
        )
        self.assertEqual(option.status_code, status.HTTP_201_CREATED)
        option_id = option.data["id"]

        self.assertEqual(
            self.client.patch(
                f"/api/lists/options/{option_id}/",
                {"option_name": "Updated"},
                format="json",
            ).status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            self.client.delete(
                f"/api/lists/options/{option_id}/"
            ).status_code,
            status.HTTP_204_NO_CONTENT,
        )

    def test_plans_and_calendar_crud(self):
        color = self.client.post(
            "/api/plans/colors/",
            {"col_id": 1, "col_text": "Red"},
            format="json",
        )
        self.assertEqual(color.status_code, status.HTTP_201_CREATED)

        repeat = self.client.post(
            "/api/plans/repeats/",
            {"rep_id": 1, "rep_text": "Daily"},
            format="json",
        )
        self.assertEqual(repeat.status_code, status.HTTP_201_CREATED)

        plan_id = str(uuid.uuid4())
        plan = self.client.post(
            "/api/plans/",
            {
                "plan_id": plan_id,
                "plan_name": "Test plan",
                "deadline": "2026-10-01T12:00:00Z",
                "plan_note": "Note",
                "couple": self.couple.couple_id,
            },
            format="json",
        )
        self.assertEqual(plan.status_code, status.HTTP_201_CREATED)

        calendar = self.client.post(
            "/api/plans/calendar-plans/",
            {
                "calendar_plan_id": 1,
                "plan": plan_id,
                "date_of_start": "2026-10-01T10:00:00Z",
                "date_of_end": "2026-10-01T11:00:00Z",
                "repeat": 1,
                "color": 1,
            },
            format="json",
        )
        self.assertEqual(calendar.status_code, status.HTTP_201_CREATED)

    def test_menu_crud(self):
        ing_type = self.client.post(
            "/api/menu/ingredient-types/",
            {"type_id": 1, "type_name": "Vegetables"},
            format="json",
        )
        self.assertEqual(ing_type.status_code, status.HTTP_201_CREATED)

        ingredient_id = str(uuid.uuid4())
        ingredient = self.client.post(
            "/api/menu/ingredients/",
            {
                "ing_id": ingredient_id,
                "ing_name": "Tomato",
                "ing_type": 1,
            },
            format="json",
        )
        self.assertEqual(ingredient.status_code, status.HTTP_201_CREATED)

        recipe_type = self.client.post(
            "/api/menu/recipe-types/",
            {"type_id": 1, "type_name": "Dinner"},
            format="json",
        )
        self.assertEqual(recipe_type.status_code, status.HTTP_201_CREATED)

        recipe_id = str(uuid.uuid4())
        recipe = self.client.post(
            "/api/menu/recipes/",
            {
                "recipe_id": recipe_id,
                "recipe_name": "Salad",
                "recipe_link": "https://example.com/recipe",
                "recipe_note": "Simple",
                "recipe_type": 1,
            },
            format="json",
        )
        self.assertEqual(recipe.status_code, status.HTTP_201_CREATED)

        relation = self.client.post(
            "/api/menu/recipe-ingredients/",
            {
                "recipe": recipe_id,
                "ingredient": ingredient_id,
                "ing_amount": 2,
            },
            format="json",
        )
        self.assertEqual(relation.status_code, status.HTTP_201_CREATED)

        fridge = self.client.post(
            "/api/menu/fridge/",
            {
                "ingredient": ingredient_id,
                "couple": self.couple.couple_id,
                "ing_amount": 5,
            },
            format="json",
        )
        self.assertEqual(fridge.status_code, status.HTTP_201_CREATED)
