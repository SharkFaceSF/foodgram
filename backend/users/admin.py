from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Follow

User = get_user_model()


@admin.register(User)
class AnyUserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "avatar")
    search_fields = ("email", "username")
    list_filter = ("email", "username")
    ordering = ("username",)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("user", "author")
    search_fields = ("user__username", "author__username")
    list_filter = ("user", "author")
