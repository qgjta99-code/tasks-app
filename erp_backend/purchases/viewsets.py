from decimal import Decimal

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from core.viewsets import OrgScopedModelViewSet
from inventory.models import StockMove, StockMoveType
from purchases.models import PurchaseBill, PurchaseBillStatus, Vendor
from purchases.serializers import (
    PurchaseBillCreateSerializer,
    PurchaseBillSerializer,
    VendorSerializer,
)


class VendorViewSet(OrgScopedModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class PurchaseBillViewSet(OrgScopedModelViewSet):
    queryset = PurchaseBill.objects.select_related("vendor", "warehouse", "created_by").prefetch_related("lines").all()

    def get_serializer_class(self):
        if self.action in {"create"}:
            return PurchaseBillCreateSerializer
        return PurchaseBillSerializer

    def perform_create(self, serializer):
        serializer.save(org_id=self.kwargs["org_id"], created_by=self.request.user)

    @action(detail=True, methods=["post"])
    def post_bill(self, request, org_id=None, pk=None):
        bill: PurchaseBill = self.get_object()
        if bill.status != PurchaseBillStatus.DRAFT:
            return Response({"detail": "Only DRAFT bills can be posted."}, status=status.HTTP_400_BAD_REQUEST)

        total = Decimal("0.00")
        for line in bill.lines.all():
            total += line.line_total
            StockMove.objects.create(
                org=bill.org,
                item=line.item,
                warehouse=bill.warehouse,
                move_type=StockMoveType.IN,
                qty=line.qty,
                reference=f"PurchaseBill:{bill.number}",
            )

        bill.total_amount = total
        bill.status = PurchaseBillStatus.POSTED
        bill.save(update_fields=["total_amount", "status", "updated_at"])
        return Response(PurchaseBillSerializer(bill).data, status=status.HTTP_200_OK)
