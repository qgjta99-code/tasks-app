from django.contrib import admin

from purchases.models import PurchaseBill, PurchaseBillLine, Vendor


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ("org", "name", "email", "phone", "is_active")
    list_filter = ("org", "is_active")
    search_fields = ("name", "email", "phone")


class PurchaseBillLineInline(admin.TabularInline):
    model = PurchaseBillLine
    extra = 0


@admin.register(PurchaseBill)
class PurchaseBillAdmin(admin.ModelAdmin):
    list_display = ("org", "number", "vendor", "warehouse", "bill_date", "status", "total_amount", "created_by")
    list_filter = ("org", "status", "bill_date")
    search_fields = ("number", "vendor__name")
    inlines = [PurchaseBillLineInline]
