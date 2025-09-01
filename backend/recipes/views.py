from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Tag, Ingredient, Recipe, Favorite, ShoppingCart, RecipeIngredient
from .serializers import TagSerializer, IngredientSerializer, RecipeSerializer, RecipeMinifiedSerializer
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .filters import RecipeFilter, IngredientFilter
from django.db.models import Sum
from io import BytesIO

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly]

class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    @action(detail=True, methods=['post', 'delete'], permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        return self._add_remove_relation(request, Favorite, pk, 'favorites')

    @action(detail=True, methods=['post', 'delete'], permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        return self._add_remove_relation(request, ShoppingCart, pk, 'shopping_cart')

    def _add_remove_relation(self, request, model, pk, error_field):
        recipe = self.get_object()
        if request.method == 'POST':
            _, created = model.objects.get_or_create(user=request.user, recipe=recipe)
            if not created:
                return Response({'errors': 'Already added'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = RecipeMinifiedSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        obj = model.objects.filter(user=request.user, recipe=recipe)
        if not obj.exists():
            return Response({'errors': 'Not added'}, status=status.HTTP_400_BAD_REQUEST)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients = RecipeIngredient.objects.filter(recipe__in_cart__user=request.user).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount')).order_by('ingredient__name')

        content = 'Shopping List\n\n'
        for ing in ingredients:
            content += f"{ing['ingredient__name']} ({ing['ingredient__measurement_unit']}) - {ing['amount']}\n"

        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="shopping_cart.txt"'
        return response

    @action(detail=True, methods=['get'], url_path='get-link')
    def get_link(self, request, pk):
        recipe = self.get_object()
        short_link = f'http://{request.get_host()}/recipes/{recipe.id}'
        return Response({'short-link': short_link})
