from core.models import Membership


def org_context(request):
    """
    Exposes:
    - org_memberships: list of active memberships for current user
    - current_org: selected Organization (session) or first membership org
    """
    user = getattr(request, "user", None)
    if not user or not user.is_authenticated:
        return {"org_memberships": [], "current_org": None}

    memberships = (
        Membership.objects.select_related("org")
        .filter(user=user, is_active=True, org__is_active=True)
        .order_by("org__name")
    )
    current_org = None
    org_id = request.session.get("current_org_id")
    if org_id:
        for m in memberships:
            if str(m.org_id) == str(org_id):
                current_org = m.org
                break
    if current_org is None:
        first = memberships.first()
        if first is not None:
            current_org = first.org
            request.session["current_org_id"] = str(first.org_id)

    return {"org_memberships": memberships, "current_org": current_org}

