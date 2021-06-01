from django.conf import settings
from edc_model_wrapper import ModelWrapper

from .purchase_order_model_wrapper_mixin import PurchaseOrderModelWrapperMixin
from .request_approval_model_wrapper_mixin import RequestApprovalModelWrapperMixin
from .vendor_justification_model_wrapper_mixin import VendorJustificationModelWrapperMixin


class PurchaseRequisitionModelWrapper(
        RequestApprovalModelWrapperMixin, VendorJustificationModelWrapperMixin,
        PurchaseOrderModelWrapperMixin, ModelWrapper):

    model = 'procurement.purchaserequisition'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'purchase_req_listboard_url')
    next_url_attrs = ['prf_number', 'request_type', ]
    querystring_attrs = ['prf_number', ]

    @property
    def document_id(self):
        return self.prf_number
