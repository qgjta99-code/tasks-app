from decimal import Decimal

from django.conf import settings
from django.db import models

from core.models import OrgModel
from inventory.models import Item, Warehouse


class Customer(OrgModel):
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, default="")
    phone = models.CharField(max_length=50, blank=True, default="")
    address = models.TextField(blank=True, default="")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class SalesInvoiceStatus(models.TextChoices):
    DRAFT = "DRAFT", "DRAFT"
    POSTED = "POSTED", "POSTED"
    VOID = "VOID", "VOID"


class SalesInvoice(OrgModel):
    number = models.CharField(max_length=30)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="invoices")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name="sales_invoices")
    invoice_date = models.DateField()
    status = models.CharField(max_length=10, choices=SalesInvoiceStatus.choices, default=SalesInvoiceStatus.DRAFT)
    total_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="created_sales_invoices"
    )

    class Meta:
        unique_together = [("org", "number")]
        ordering = ["-invoice_date", "-created_at"]

    def __str__(self) -> str:
        return f"SI-{self.number}"


class SalesInvoiceLine(OrgModel):
    invoice = models.ForeignKey(SalesInvoice, on_delete=models.CASCADE, related_name="lines")
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name="sales_lines")
    qty = models.DecimalField(max_digits=14, decimal_places=3)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    line_total = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))

    class Meta:
        ordering = ["id"]

    def save(self, *args, **kwargs):
        self.line_total = (self.qty or 0) * (self.unit_price or 0)
        return super().save(*args, **kwargs)
