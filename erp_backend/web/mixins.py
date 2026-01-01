from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

from core.models import Membership, Organization


class CurrentOrgMixin(LoginRequiredMixin):
    """
    Provides self.current_org for org-scoped pages (selected via session).
    Ensures the user is an active member of the org.
    """

    current_org: Organization | None = None

    def dispatch(self, request, *args, **kwargs):
        org_id = request.session.get("current_org_id")
        if not org_id:
            # context processor will auto-select if possible
            org_id = request.session.get("current_org_id")
        if not org_id:
            raise Http404("No organization selected.")

        if not Membership.objects.filter(user=request.user, org_id=org_id, is_active=True, org__is_active=True).exists():
            raise Http404("Organization not found.")

        self.current_org = Organization.objects.get(id=org_id)
        return super().dispatch(request, *args, **kwargs)

