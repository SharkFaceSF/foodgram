import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Импортирует ингредиенты из JSON-файла в модель Ingredient'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, 'data', 'ingredients.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        ingredients = [
            Ingredient(
                name=item['name'], measurement_unit=item['measurement_unit']
            )
            for item in data
        ]

        Ingredient.objects.bulk_create(ingredients, ignore_conflicts=True)

        self.stdout.write(
            self.style.SUCCESS(f'Загружено {len(ingredients)} ингредиентов')
        )
