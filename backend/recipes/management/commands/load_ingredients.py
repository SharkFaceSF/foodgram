import json

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        with open(
            "/app/data/ingredients.json", "r", encoding="utf-8"
        ) as f:
            data = json.load(f)
            for item in data:
                Ingredient.objects.get_or_create(
                    name=item["name"],
                    measurement_unit=item["measurement_unit"],
                )
        self.stdout.write(
            self.style.SUCCESS(f"Загружено {len(data)} ингредиентов")
        )
