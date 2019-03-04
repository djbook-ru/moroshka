# -*- coding: utf-8 -*-

from django.contrib import admin


class Immutable(admin.ModelAdmin):
    """Mixin denies any changes on the models."""

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return super().has_change_permission(request, obj)
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class UserMixin:
    """Mixin saves the current admin user into the models."""
    def save_model(self, request, obj, form, change):
        _ = form
        if not change:
            obj.created_by = request.user
        obj.save()

