from rest_framework import serializers

from inventory.models import Item, StockMove, Warehouse


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [
            "id",
            "org",
            "sku",
            "name",
            "uom",
            "sale_price",
            "purchase_price",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "org", "created_at", "updated_at"]


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ["id", "org", "code", "name", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "org", "created_at", "updated_at"]


class StockMoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMove
        fields = [
            "id",
            "org",
            "item",
            "warehouse",
            "move_type",
            "qty",
            "reference",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "org", "created_at", "updated_at"]
