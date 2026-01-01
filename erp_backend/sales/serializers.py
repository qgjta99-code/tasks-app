from rest_framework import serializers

from inventory.models import Item
from sales.models import Customer, SalesInvoice, SalesInvoiceLine


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "org", "name", "email", "phone", "address", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "org", "created_at", "updated_at"]


class SalesInvoiceLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesInvoiceLine
        fields = ["id", "org", "invoice", "item", "qty", "unit_price", "line_total", "created_at", "updated_at"]
        read_only_fields = ["id", "org", "invoice", "line_total", "created_at", "updated_at"]


class SalesInvoiceSerializer(serializers.ModelSerializer):
    lines = SalesInvoiceLineSerializer(many=True, read_only=True)

    class Meta:
        model = SalesInvoice
        fields = [
            "id",
            "org",
            "number",
            "customer",
            "warehouse",
            "invoice_date",
            "status",
            "total_amount",
            "created_by",
            "created_at",
            "updated_at",
            "lines",
        ]
        read_only_fields = ["id", "org", "status", "total_amount", "created_by", "created_at", "updated_at", "lines"]


class SalesInvoiceCreateLineSerializer(serializers.Serializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
    qty = serializers.DecimalField(max_digits=14, decimal_places=3)
    unit_price = serializers.DecimalField(max_digits=12, decimal_places=2)


class SalesInvoiceCreateSerializer(serializers.ModelSerializer):
    lines = SalesInvoiceCreateLineSerializer(many=True)

    class Meta:
        model = SalesInvoice
        fields = ["id", "org", "number", "customer", "warehouse", "invoice_date", "lines"]
        read_only_fields = ["id", "org"]

    def create(self, validated_data):
        lines_data = validated_data.pop("lines", [])
        invoice = SalesInvoice.objects.create(**validated_data)
        total = 0
        for line in lines_data:
            obj = SalesInvoiceLine.objects.create(
                org=invoice.org,
                invoice=invoice,
                item=line["item"],
                qty=line["qty"],
                unit_price=line["unit_price"],
            )
            total += obj.line_total
        invoice.total_amount = total
        invoice.save(update_fields=["total_amount", "updated_at"])
        return invoice
