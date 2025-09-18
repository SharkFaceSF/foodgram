from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from .constants import (INGREDIENT_NAME_MAX_LENGTH, INGREDIENT_UNIT_MAX_LENGTH,
                        MIN_VALUE, RECIPE_NAME_MAX_LENGTH, TAG_NAME_MAX_LENGTH,
                        TAG_SLUG_MAX_LENGTH)

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=TAG_NAME_MAX_LENGTH, unique=True)
    slug = models.SlugField(max_length=TAG_SLUG_MAX_LENGTH, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=INGREDIENT_NAME_MAX_LENGTH)
    measurement_unit = models.CharField(max_length=INGREDIENT_UNIT_MAX_LENGTH)

    class Meta:
        ordering = ["name"]
        unique_together = ["name", "measurement_unit"]

    def __str__(self):
        return f"{self.name}, {self.measurement_unit}"


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
    )
    name = models.CharField(max_length=RECIPE_NAME_MAX_LENGTH)
    image = models.ImageField(upload_to="recipes/images/")
    text = models.TextField()
    cooking_time = models.PositiveIntegerField(
        validators=[MinValueValidator(MIN_VALUE)]
    )
    tags = models.ManyToManyField(Tag, related_name="recipes")
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="ingredients",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
    )
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(MIN_VALUE)]
    )

    class Meta:
        unique_together = ["recipe", "ingredient"]


class UserRecipeBase(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True
        unique_together = ["user", "recipe"]


class Favorite(UserRecipeBase):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorited_by",
    )


class ShoppingCart(UserRecipeBase):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shopping_cart",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="in_cart",
    )
