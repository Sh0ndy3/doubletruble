import uuid

from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied

from .models import Fridge, IngInRecipe, IngType, Ingredients, RecipeType, Recipes
from .serializers import (
    FridgeSerializer,
    IngInRecipeSerializer,
    IngTypeSerializer,
    IngredientsSerializer,
    RecipeTypeSerializer,
    RecipesSerializer,
)


class IngTypeViewSet(viewsets.ModelViewSet):
    queryset = IngType.objects.all()
    serializer_class = IngTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


class RecipeTypeViewSet(viewsets.ModelViewSet):
    queryset = RecipeType.objects.all()
    serializer_class = RecipeTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(ing_id=uuid.uuid4())


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(recipe_id=uuid.uuid4())


class IngInRecipeViewSet(viewsets.ModelViewSet):
    queryset = IngInRecipe.objects.all()
    serializer_class = IngInRecipeSerializer
    permission_classes = [permissions.IsAuthenticated]


class FridgeViewSet(viewsets.ModelViewSet):
    serializer_class = FridgeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (Fridge.objects.filter(
            couple__partner=self.request.user
        ) | Fridge.objects.filter(
            couple__second_partner=self.request.user
        )).distinct()

    def perform_create(self, serializer):
        couple = serializer.validated_data["couple"]
        if not (
            couple.partner_id == self.request.user.user_id
            or couple.second_partner_id == self.request.user.user_id
        ):
            raise PermissionDenied("You can only use your own couple.")
        serializer.save()
