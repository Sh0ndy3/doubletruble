from rest_framework import serializers

from .models import Fridge, IngInRecipe, IngType, Ingredients, RecipeType, Recipes


class IngTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngType
        fields = "__all__"


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = "__all__"


class RecipeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeType
        fields = "__all__"


class RecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipes
        fields = "__all__"


class IngInRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngInRecipe
        fields = "__all__"


class FridgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fridge
        fields = "__all__"
