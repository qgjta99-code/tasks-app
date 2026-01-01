from decimal import Decimal

from django.db import models

from core.models import OrgModel


class Item(OrgModel):
    sku = models.CharField(max_length=64)
    name = models.CharField(max_length=200)
    uom = models.CharField(max_length=30, default="pcs")
    sale_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = [("org", "sku")]
        ordering = ["sku"]

    def __str__(self) -> str:
        return f"{self.sku} - {self.name}"


class Warehouse(OrgModel):
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = [("org", "code")]
        ordering = ["code"]

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"


class StockMoveType(models.TextChoices):
    IN = "IN", "IN"
    OUT = "OUT", "OUT"
    ADJUST = "ADJUST", "ADJUST"


class StockMove(OrgModel):
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name="stock_moves")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name="stock_moves")
    move_type = models.CharField(max_length=10, choices=StockMoveType.choices)
    qty = models.DecimalField(max_digits=14, decimal_places=3)
    reference = models.CharField(max_length=200, blank=True, default="")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.move_type} {self.qty} {self.item} @ {self.warehouse}"
