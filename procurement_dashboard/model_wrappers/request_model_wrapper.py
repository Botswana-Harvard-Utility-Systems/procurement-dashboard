from django.conf import settings
from edc_model_wrapper import ModelWrapper


class RequestModelWrapper(ModelWrapper):

    model = 'procurement.request'
    next_url_name = settings.DASHBOARD_URL_NAMES.get('purchase_req_listboard_url')
    next_url_attrs = ['request_approval', 'request_to', 'status', 'request_type', 'order_number', ]
    querystring_attrs = ['request_approval', 'request_to', ]

    @property
    def request_approval(self):
        return self.object.request_approval.id

    @property
    def request_to(self):
        return self.object.request_to.id
