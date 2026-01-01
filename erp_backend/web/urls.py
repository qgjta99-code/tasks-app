from django.urls import path
from django.contrib.auth.views import LogoutView

from web.views import (
    CustomerCreateView,
    CustomerUpdateView,
    CustomersListView,
    DashboardView,
    ItemCreateView,
    ItemUpdateView,
    ItemsListView,
    VendorCreateView,
    VendorUpdateView,
    VendorsListView,
    WarehouseCreateView,
    WarehouseUpdateView,
    WarehousesListView,
    WebLoginView,
    switch_org,
)

app_name = "web"

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("login/", WebLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("switch-org/", switch_org, name="switch_org"),
    # Master data
    path("items/", ItemsListView.as_view(), name="items_list"),
    path("items/new/", ItemCreateView.as_view(), name="items_new"),
    path("items/<int:pk>/edit/", ItemUpdateView.as_view(), name="items_edit"),
    path("warehouses/", WarehousesListView.as_view(), name="warehouses_list"),
    path("warehouses/new/", WarehouseCreateView.as_view(), name="warehouses_new"),
    path("warehouses/<int:pk>/edit/", WarehouseUpdateView.as_view(), name="warehouses_edit"),
    path("customers/", CustomersListView.as_view(), name="customers_list"),
    path("customers/new/", CustomerCreateView.as_view(), name="customers_new"),
    path("customers/<int:pk>/edit/", CustomerUpdateView.as_view(), name="customers_edit"),
    path("vendors/", VendorsListView.as_view(), name="vendors_list"),
    path("vendors/new/", VendorCreateView.as_view(), name="vendors_new"),
    path("vendors/<int:pk>/edit/", VendorUpdateView.as_view(), name="vendors_edit"),
]

