from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from core.models import Membership, Organization
from core.permissions import IsActiveOrgMember, IsOrgAdmin
from core.serializers import MembershipCreateSerializer, MembershipSerializer, OrganizationSerializer


class OrgScopedModelViewSet(viewsets.ModelViewSet):
    """
    Base viewset for models with an `org` FK and org-scoped URLs.
    Expects `org_id` kwarg.
    """

    permission_classes = [IsActiveOrgMember]

    def get_queryset(self):
        qs = super().get_queryset()
        org_id = self.kwargs.get("org_id")
        if org_id is None:
            return qs.none()
        return qs.filter(org_id=org_id)

    def perform_create(self, serializer):
        serializer.save(org_id=self.kwargs["org_id"])


class OrganizationViewSet(viewsets.ModelViewSet):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Organization.objects.none()
        return Organization.objects.filter(memberships__user=user, memberships__is_active=True).distinct()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        org = serializer.save()
        Membership.objects.create(org=org, user=request.user, is_active=True, is_admin=True)
        out = self.get_serializer(org)
        return Response(out.data, status=status.HTTP_201_CREATED)


class MembershipViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsOrgAdmin]
    serializer_class = MembershipSerializer
    queryset = Membership.objects.select_related("org", "user")

    def get_queryset(self):
        return super().get_queryset().filter(org_id=self.kwargs["org_id"])

    def get_serializer_class(self):
        if self.action in {"create"}:
            return MembershipCreateSerializer
        return MembershipSerializer
