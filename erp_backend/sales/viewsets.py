from decimal import Decimal

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from core.viewsets import OrgScopedModelViewSet
from inventory.models import StockMove, StockMoveType
from sales.models import Customer, SalesInvoice, SalesInvoiceStatus
from sales.serializers import CustomerSerializer, SalesInvoiceCreateSerializer, SalesInvoiceSerializer


class CustomerViewSet(OrgScopedModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class SalesInvoiceViewSet(OrgScopedModelViewSet):
    queryset = SalesInvoice.objects.select_related("customer", "warehouse", "created_by").prefetch_related("lines").all()

    def get_serializer_class(self):
        if self.action in {"create"}:
            return SalesInvoiceCreateSerializer
        return SalesInvoiceSerializer

    def perform_create(self, serializer):
        serializer.save(org_id=self.kwargs["org_id"], created_by=self.request.user)

    @action(detail=True, methods=["post"])
    def post_invoice(self, request, org_id=None, pk=None):
        invoice: SalesInvoice = self.get_object()
        if invoice.status != SalesInvoiceStatus.DRAFT:
            return Response({"detail": "Only DRAFT invoices can be posted."}, status=status.HTTP_400_BAD_REQUEST)

        total = Decimal("0.00")
        for line in invoice.lines.all():
            total += line.line_total
            StockMove.objects.create(
                org=invoice.org,
                item=line.item,
                warehouse=invoice.warehouse,
                move_type=StockMoveType.OUT,
                qty=line.qty,
                reference=f"SalesInvoice:{invoice.number}",
            )

        invoice.total_amount = total
        invoice.status = SalesInvoiceStatus.POSTED
        invoice.save(update_fields=["total_amount", "status", "updated_at"])
        return Response(SalesInvoiceSerializer(invoice).data, status=status.HTTP_200_OK)
