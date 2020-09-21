from django.conf import settings
from edc_model_wrapper import ModelWrapper


class PurchaseOrderModelWrapper(ModelWrapper):

    model = 'procurement.purchaseorder'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'purchase_order_listboard_url')
    next_url_attrs = ['order_number']
    querystring_attrs = ['order_number', ]

    @property
    def purchase_order_total(self):
        order_items = self.object.purchaseorderitem_set.all()
        total = 0
        for order_item in order_items:
            total += order_item.total_price_incl
        return float(total)
