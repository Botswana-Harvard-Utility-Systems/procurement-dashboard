from django.conf import settings
from edc_model_wrapper import ModelWrapper


class RequestApprovalModelWrapper(ModelWrapper):

    model = 'procurement.requestapproval'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'purchase_req_listboard_url')
    next_url_attrs = ['prf_number']
    querystring_attrs = ['prf_number', 'rfa_number']
