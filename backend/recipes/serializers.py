from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "slug")


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")


class IngredientInRecipeWriteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField(min_value=1)


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = RecipeIngredient
        fields = ("id", "name", "measurement_unit", "amount")


class RecipeMinifiedSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientInRecipeSerializer(
        many=True,
        read_only=True,
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def get_author(self, obj):
        from users.serializers import CustomUserSerializer

        return CustomUserSerializer(obj.author, context=self.context).data

    def get_is_favorited(self, obj):
        if self.context["request"].user.is_authenticated:
            return Favorite.objects.filter(
                user=self.context["request"].user,
                recipe=obj,
            ).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        if self.context["request"].user.is_authenticated:
            return ShoppingCart.objects.filter(
                user=self.context["request"].user,
                recipe=obj,
            ).exists()
        return False

    def validate(self, data):
        if "image" not in self.initial_data or self.initial_data[
            "image"
        ] is None:
            raise serializers.ValidationError("Поле image обязательно")

        if "ingredients" not in self.initial_data or not self.initial_data[
            "ingredients"
        ]:
            raise serializers.ValidationError("Требуются ингредиенты")

        ingredients = self.initial_data["ingredients"]
        ingredient_ids = [item["id"] for item in ingredients]
        if len(ingredient_ids) != len(set(ingredient_ids)):
            raise serializers.ValidationError("Дублирующиеся ингредиенты")

        existing_ingredients = Ingredient.objects.filter(
            id__in=ingredient_ids).values_list('id', flat=True)
        missing_ingredients = set(ingredient_ids) - set(existing_ingredients)
        if missing_ingredients:
            raise serializers.ValidationError(
                "Такого ингредиента не существует"
            )

        for item in ingredients:
            amount = int(item["amount"])
            if amount < 1:
                raise serializers.ValidationError(
                    "Количество должно быть не менее 1."
                )

        if "tags" not in self.initial_data or not self.initial_data["tags"]:
            raise serializers.ValidationError("Требуются теги")

        tags = self.initial_data["tags"]
        if len(tags) != len(set(tags)):
            raise serializers.ValidationError("Дублирующиеся теги")

        existing_tags = Tag.objects.filter(id__in=tags).values_list(
            'id', flat=True
        )
        missing_tags = set(tags) - set(existing_tags)
        if missing_tags:
            raise serializers.ValidationError(
                "Такого тэга не существует"
            )

        return data

    def create(self, validated_data):
        tags = self.initial_data.get("tags")
        ingredients = self.initial_data.get("ingredients")
        recipe = Recipe.objects.create(
            author=self.context["request"].user,
            **validated_data,
        )
        recipe.tags.set(tags)
        for item in ingredients:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient_id=item["id"],
                amount=item["amount"],
            )
        return recipe

    def update(self, instance, validated_data):
        tags = self.initial_data.get("tags")
        ingredients = self.initial_data.get("ingredients")
        instance = super().update(instance, validated_data)
        if tags:
            instance.tags.set(tags)
        if ingredients:
            instance.ingredients.all().delete()
            for item in ingredients:
                RecipeIngredient.objects.create(
                    recipe=instance,
                    ingredient_id=item["id"],
                    amount=item["amount"],
                )
        return instance
