import uuid

from django.conf import settings
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Organization(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Membership(TimeStampedModel):
    """
    Row-level multi-tenancy:
    - User must have an active Membership in an Organization.
    - is_admin grants org management privileges.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="memberships")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        unique_together = [("org", "user")]
        ordering = ["org__name", "user_id"]

    def __str__(self) -> str:
        return f"{self.user} @ {self.org}"


class OrgModel(TimeStampedModel):
    """
    Base for org-scoped data models.
    """

    org = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="%(class)ss")

    class Meta:
        abstract = True
