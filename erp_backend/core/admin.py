from django.contrib import admin

from core.models import Membership, Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    search_fields = ("name",)
    list_filter = ("is_active",)


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ("org", "user", "is_active", "is_admin", "created_at")
    list_filter = ("is_active", "is_admin", "org")
    search_fields = ("user__username", "user__email", "org__name")
