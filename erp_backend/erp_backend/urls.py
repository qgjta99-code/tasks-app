from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.viewsets import MembershipViewSet, OrganizationViewSet
from inventory.viewsets import ItemViewSet, StockMoveViewSet, WarehouseViewSet
from purchases.viewsets import PurchaseBillViewSet, VendorViewSet
from sales.viewsets import CustomerViewSet, SalesInvoiceViewSet

admin.site.site_header = "ERP Admin"
admin.site.site_title = "ERP Admin"

router = DefaultRouter()
router.register(r"orgs", OrganizationViewSet, basename="org")

org_router = DefaultRouter()
org_router.register(r"memberships", MembershipViewSet, basename="membership")
org_router.register(r"items", ItemViewSet, basename="item")
org_router.register(r"warehouses", WarehouseViewSet, basename="warehouse")
org_router.register(r"stock-moves", StockMoveViewSet, basename="stockmove")
org_router.register(r"customers", CustomerViewSet, basename="customer")
org_router.register(r"sales-invoices", SalesInvoiceViewSet, basename="salesinvoice")
org_router.register(r"vendors", VendorViewSet, basename="vendor")
org_router.register(r"purchase-bills", PurchaseBillViewSet, basename="purchasebill")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/", include(router.urls)),
    path("api/orgs/<uuid:org_id>/", include(org_router.urls)),
]
