from django.conf import settings
from edc_model_wrapper import ModelWrapper

from .request_approval_model_wrapper_mixin import RequestApprovalModelWrapperMixin


class PurchaseOrderModelWrapper(RequestApprovalModelWrapperMixin, ModelWrapper):

    model = 'procurement.purchaseorder'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'purchase_order_listboard_url')
    next_url_attrs = ['prf_number', 'request_type', ]
    querystring_attrs = ['prf_number', ]

    @property
    def document_id(self):
        return self.order_number

#     @property
#     def purchase_order_total(self):
#         import pdb; pdb.set_trace()
#         order_items = self.object.purchaseorderitem_set.all()
#         total = 0
#         for order_item in order_items:
#             total += order_item.total_price_incl
#         return float(total)
