from core.viewsets import OrgScopedModelViewSet
from inventory.models import Item, StockMove, Warehouse
from inventory.serializers import ItemSerializer, StockMoveSerializer, WarehouseSerializer


class ItemViewSet(OrgScopedModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class WarehouseViewSet(OrgScopedModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer


class StockMoveViewSet(OrgScopedModelViewSet):
    queryset = StockMove.objects.select_related("item", "warehouse").all()
    serializer_class = StockMoveSerializer
