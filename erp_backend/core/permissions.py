from uuid import UUID

from rest_framework.permissions import BasePermission

from core.models import Membership


def _parse_uuid(value: str) -> UUID | None:
    try:
        return UUID(str(value))
    except Exception:
        return None


class IsActiveOrgMember(BasePermission):
    """
    Requires the request.user to have an active Membership in org_id (from URL kwarg).
    """

    message = "You are not an active member of this organization."

    def has_permission(self, request, view) -> bool:
        org_id = getattr(view, "kwargs", {}).get("org_id")
        org_uuid = _parse_uuid(org_id) if org_id is not None else None
        if org_uuid is None:
            return True  # Not an org-scoped endpoint
        if not request.user or not request.user.is_authenticated:
            return False
        return Membership.objects.filter(org_id=org_uuid, user=request.user, is_active=True).exists()


class IsOrgAdmin(BasePermission):
    """
    Requires active membership with is_admin=True for the org_id (from URL kwarg).
    """

    message = "You must be an organization admin to perform this action."

    def has_permission(self, request, view) -> bool:
        org_id = getattr(view, "kwargs", {}).get("org_id")
        org_uuid = _parse_uuid(org_id) if org_id is not None else None
        if org_uuid is None:
            return False
        if not request.user or not request.user.is_authenticated:
            return False
        return Membership.objects.filter(
            org_id=org_uuid, user=request.user, is_active=True, is_admin=True
        ).exists()
