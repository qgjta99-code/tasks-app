from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, UpdateView

from inventory.models import Item, Warehouse
from purchases.models import Vendor
from sales.models import Customer
from web.forms import CustomerForm, ItemForm, VendorForm, WarehouseForm
from web.mixins import CurrentOrgMixin


class WebLoginView(LoginView):
    template_name = "web/login.html"
    redirect_authenticated_user = True


class DashboardView(CurrentOrgMixin, TemplateView):
    template_name = "web/dashboard.html"


def switch_org(request):
    if not request.user.is_authenticated:
        return redirect("/login/")
    org_id = request.POST.get("org_id") or request.GET.get("org_id")
    if org_id:
        request.session["current_org_id"] = str(org_id)
    return redirect(request.GET.get("next") or "/")


class OrgListView(CurrentOrgMixin, ListView):
    paginate_by = 20
    template_name = "web/list.html"
    context_object_name = "rows"
    title = ""

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(org=self.current_org).order_by("-created_at")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = self.title
        return ctx


class OrgCreateView(CurrentOrgMixin, CreateView):
    template_name = "web/form.html"
    success_url = reverse_lazy("web:dashboard")
    title = ""

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.org = self.current_org
        obj.save()
        messages.success(self.request, "تم الحفظ بنجاح")
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = self.title
        return ctx


class OrgUpdateView(CurrentOrgMixin, UpdateView):
    template_name = "web/form.html"
    success_url = reverse_lazy("web:dashboard")
    title = ""

    def get_queryset(self):
        return super().get_queryset().filter(org=self.current_org)

    def form_valid(self, form):
        messages.success(self.request, "تم التحديث بنجاح")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = self.title
        return ctx


class ItemsListView(OrgListView):
    model = Item
    title = "الأصناف"
    template_name = "web/items_list.html"


class ItemCreateView(OrgCreateView):
    form_class = ItemForm
    title = "إضافة صنف"
    success_url = reverse_lazy("web:items_list")


class ItemUpdateView(OrgUpdateView):
    model = Item
    form_class = ItemForm
    title = "تعديل صنف"
    success_url = reverse_lazy("web:items_list")


class WarehousesListView(OrgListView):
    model = Warehouse
    title = "المستودعات"
    template_name = "web/warehouses_list.html"


class WarehouseCreateView(OrgCreateView):
    form_class = WarehouseForm
    title = "إضافة مستودع"
    success_url = reverse_lazy("web:warehouses_list")


class WarehouseUpdateView(OrgUpdateView):
    model = Warehouse
    form_class = WarehouseForm
    title = "تعديل مستودع"
    success_url = reverse_lazy("web:warehouses_list")


class CustomersListView(OrgListView):
    model = Customer
    title = "العملاء"
    template_name = "web/customers_list.html"


class CustomerCreateView(OrgCreateView):
    form_class = CustomerForm
    title = "إضافة عميل"
    success_url = reverse_lazy("web:customers_list")


class CustomerUpdateView(OrgUpdateView):
    model = Customer
    form_class = CustomerForm
    title = "تعديل عميل"
    success_url = reverse_lazy("web:customers_list")


class VendorsListView(OrgListView):
    model = Vendor
    title = "الموردون"
    template_name = "web/vendors_list.html"


class VendorCreateView(OrgCreateView):
    form_class = VendorForm
    title = "إضافة مورد"
    success_url = reverse_lazy("web:vendors_list")


class VendorUpdateView(OrgUpdateView):
    model = Vendor
    form_class = VendorForm
    title = "تعديل مورد"
    success_url = reverse_lazy("web:vendors_list")
