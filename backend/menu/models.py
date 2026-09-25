from django.db import models


class IngType(models.Model):
    type_id = models.IntegerField(
        primary_key=True,
        db_column="typeID"
    )

    type_name = models.CharField(
        max_length=255,
        db_column="typeName"
    )

    def __str__(self):
        return self.type_name


class Ingredients(models.Model):
    ing_id = models.UUIDField(
        primary_key=True,
        editable=False,
        db_column="ingID"
    )

    ing_name = models.CharField(
        max_length=255,
        db_column="ingName"
    )

    ing_type = models.ForeignKey(
        IngType,
        on_delete=models.PROTECT,
        db_column="ingType",
        related_name="ingredients"
    )

    def __str__(self):
        return self.ing_name


class RecipeType(models.Model):
    type_id = models.IntegerField(
        primary_key=True,
        db_column="typeID"
    )

    type_name = models.CharField(
        max_length=255,
        db_column="typeName"
    )

    def __str__(self):
        return self.type_name


class Recipes(models.Model):
    recipe_id = models.UUIDField(
        primary_key=True,
        editable=False,
        db_column="recipeID"
    )

    recipe_name = models.CharField(
        max_length=255,
        db_column="recipeName"
    )

    recipe_link = models.CharField(
        max_length=255,
        db_column="recipeLink"
    )

    recipe_note = models.CharField(
        max_length=255,
        db_column="recipeNote"
    )

    recipe_type = models.ForeignKey(
        RecipeType,
        on_delete=models.PROTECT,
        db_column="recipeType",
        related_name="recipes"
    )

    def __str__(self):
        return self.recipe_name


class IngInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        db_column="recipeID",
        related_name="ingredients"
    )

    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        db_column="ingID",
        related_name="recipes"
    )

    ing_amount = models.IntegerField(
        db_column="ingAmount"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredient"],
                name="unique_ingredient_in_recipe"
            )
        ]

    def __str__(self):
        return f"{self.recipe} — {self.ingredient}"


class Fridge(models.Model):
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        db_column="ingID",
        related_name="fridge_entries"
    )

    couple = models.ForeignKey(
        "couples.Couple",
        on_delete=models.CASCADE,
        db_column="coupleID",
        related_name="fridge"
    )

    ing_amount = models.IntegerField(
        db_column="ingAmount"
    )

    class Meta: #для уникального рецепта
        constraints = [
            models.UniqueConstraint(
                fields=["ingredient", "couple"],
                name="unique_ingredient_in_fridge"
            )
        ]

    def __str__(self):
        return f"{self.ingredient} — {self.ing_amount}"