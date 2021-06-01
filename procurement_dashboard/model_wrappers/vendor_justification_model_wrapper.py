from django.conf import settings
from edc_model_wrapper import ModelWrapper


class VendorJustificationModelWrapper(ModelWrapper):

    model = 'procurement.vendorjustification'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'purchase_req_listboard_url')
    next_url_attrs = ['justification_number', 'prf_number', 'request_type',
                      'selected_vendor', ]
    querystring_attrs = ['justification_number', ]
