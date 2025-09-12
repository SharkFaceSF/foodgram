from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

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
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="recipes/images/")
    text = models.TextField()
    cooking_time = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
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
        validators=[MinValueValidator(1)]
    )

    class Meta:
        unique_together = ["recipe", "ingredient"]


class Favorite(models.Model):
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

    class Meta:
        unique_together = ["user", "recipe"]


class ShoppingCart(models.Model):
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

    class Meta:
        unique_together = ["user", "recipe"]
