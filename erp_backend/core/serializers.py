from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.models import Membership, Organization


User = get_user_model()


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["id", "name", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class MembershipSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Membership
        fields = [
            "id",
            "org",
            "user",
            "user_username",
            "is_active",
            "is_admin",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class MembershipCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ["id", "org", "user", "is_active", "is_admin"]
        read_only_fields = ["id"]
