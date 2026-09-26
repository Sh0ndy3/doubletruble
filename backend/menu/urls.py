from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    FridgeViewSet,
    IngInRecipeViewSet,
    IngTypeViewSet,
    IngredientsViewSet,
    RecipeTypeViewSet,
    RecipesViewSet,
)


router = DefaultRouter()
router.register("ingredient-types", IngTypeViewSet, basename="ingredient-type")
router.register("ingredients", IngredientsViewSet, basename="ingredient")
router.register("recipe-types", RecipeTypeViewSet, basename="recipe-type")
router.register("recipes", RecipesViewSet, basename="recipe")
router.register("recipe-ingredients", IngInRecipeViewSet, basename="recipe-ingredient")
router.register("fridge", FridgeViewSet, basename="fridge")

urlpatterns = [
    path("", include(router.urls)),
]
