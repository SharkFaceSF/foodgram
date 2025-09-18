from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Follow, User
from .serializers import SetAvatarSerializer, UserWithRecipesSerializer


class UserViewSet(DjoserUserViewSet):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    pagination_class = LimitOffsetPagination
    page_size_query_param = 'limit'

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request):
        queryset = User.objects.filter(
            following__user=request.user,
        )
        page = self.paginate_queryset(queryset)
        serializer = UserWithRecipesSerializer(
            page,
            many=True,
            context={"request": request},
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, id=None):
        author = self.get_object()
        if request.method == "POST":
            if request.user == author:
                return Response(
                    {"errors": "Нельзя подписаться"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            follow, created = Follow.objects.get_or_create(
                user=request.user,
                author=author,
            )
            if not created:
                return Response(
                    {"errors": "Нельзя подписаться"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = UserWithRecipesSerializer(
                author,
                context={"request": request},
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        deleted_count, _ = Follow.objects.filter(
            user=request.user,
            author=author,
        ).delete()
        if deleted_count == 0:
            return Response(
                {"errors": "Не подписан"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=["put", "delete"],
        permission_classes=[IsAuthenticated],
        url_path="me/avatar",
    )
    def me_avatar(self, request):
        if request.method == "PUT":
            serializer = SetAvatarSerializer(
                request.user,
                data=request.data,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        request.user.avatar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
