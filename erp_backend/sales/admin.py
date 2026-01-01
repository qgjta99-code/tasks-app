from django.contrib import admin

from sales.models import Customer, SalesInvoice, SalesInvoiceLine


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("org", "name", "email", "phone", "is_active")
    list_filter = ("org", "is_active")
    search_fields = ("name", "email", "phone")


class SalesInvoiceLineInline(admin.TabularInline):
    model = SalesInvoiceLine
    extra = 0


@admin.register(SalesInvoice)
class SalesInvoiceAdmin(admin.ModelAdmin):
    list_display = ("org", "number", "customer", "warehouse", "invoice_date", "status", "total_amount", "created_by")
    list_filter = ("org", "status", "invoice_date")
    search_fields = ("number", "customer__name")
    inlines = [SalesInvoiceLineInline]
