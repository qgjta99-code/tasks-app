from django import forms

from inventory.models import Item, Warehouse
from purchases.models import Vendor
from sales.models import Customer


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["sku", "name", "uom", "sale_price", "purchase_price", "is_active"]


class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ["code", "name", "is_active"]


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "email", "phone", "address", "is_active"]


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ["name", "email", "phone", "address", "is_active"]

