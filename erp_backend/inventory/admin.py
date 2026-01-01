from django.contrib import admin

from inventory.models import Item, StockMove, Warehouse


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("org", "sku", "name", "uom", "sale_price", "purchase_price", "is_active")
    list_filter = ("org", "is_active")
    search_fields = ("sku", "name")


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ("org", "code", "name", "is_active")
    list_filter = ("org", "is_active")
    search_fields = ("code", "name")


@admin.register(StockMove)
class StockMoveAdmin(admin.ModelAdmin):
    list_display = ("org", "move_type", "item", "warehouse", "qty", "reference", "created_at")
    list_filter = ("org", "move_type", "warehouse")
    search_fields = ("reference", "item__sku", "item__name")
