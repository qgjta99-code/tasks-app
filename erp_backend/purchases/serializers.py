from rest_framework import serializers

from inventory.models import Item
from purchases.models import PurchaseBill, PurchaseBillLine, Vendor


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ["id", "org", "name", "email", "phone", "address", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "org", "created_at", "updated_at"]


class PurchaseBillLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseBillLine
        fields = ["id", "org", "bill", "item", "qty", "unit_price", "line_total", "created_at", "updated_at"]
        read_only_fields = ["id", "org", "bill", "line_total", "created_at", "updated_at"]


class PurchaseBillSerializer(serializers.ModelSerializer):
    lines = PurchaseBillLineSerializer(many=True, read_only=True)

    class Meta:
        model = PurchaseBill
        fields = [
            "id",
            "org",
            "number",
            "vendor",
            "warehouse",
            "bill_date",
            "status",
            "total_amount",
            "created_by",
            "created_at",
            "updated_at",
            "lines",
        ]
        read_only_fields = ["id", "org", "status", "total_amount", "created_by", "created_at", "updated_at", "lines"]


class PurchaseBillCreateLineSerializer(serializers.Serializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
    qty = serializers.DecimalField(max_digits=14, decimal_places=3)
    unit_price = serializers.DecimalField(max_digits=12, decimal_places=2)


class PurchaseBillCreateSerializer(serializers.ModelSerializer):
    lines = PurchaseBillCreateLineSerializer(many=True)

    class Meta:
        model = PurchaseBill
        fields = ["id", "org", "number", "vendor", "warehouse", "bill_date", "lines"]
        read_only_fields = ["id", "org"]

    def create(self, validated_data):
        lines_data = validated_data.pop("lines", [])
        bill = PurchaseBill.objects.create(**validated_data)
        total = 0
        for line in lines_data:
            obj = PurchaseBillLine.objects.create(
                org=bill.org,
                bill=bill,
                item=line["item"],
                qty=line["qty"],
                unit_price=line["unit_price"],
            )
            total += obj.line_total
        bill.total_amount = total
        bill.save(update_fields=["total_amount", "updated_at"])
        return bill
