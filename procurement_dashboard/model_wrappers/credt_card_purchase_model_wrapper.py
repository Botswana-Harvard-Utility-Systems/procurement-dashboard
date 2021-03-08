from django.conf import settings
from edc_model_wrapper import ModelWrapper


class CreditCardPurchaseModelWrapper(ModelWrapper):

    model = 'procurement.creditcardpurchase'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'credit_card_listboard_url')
    next_url_attrs = ['ccp_number', 'request_by', ]
    querystring_attrs = ['ccp_number', ]

    def document_id(self):
        return self.object.ccp_number

    def request_type(self):
        return ''
