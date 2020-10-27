from django.conf import settings
from edc_model_wrapper import ModelWrapper

from .request_approval_model_wrapper_mixin import RequestApprovalModelWrapperMixin


class PurchaseRequisitionModelWrapper(
        RequestApprovalModelWrapperMixin, ModelWrapper):

    model = 'procurement.purchaserequisition'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'purchase_req_listboard_url')
    next_url_attrs = ['prf_number']
    querystring_attrs = ['prf_number', ]
