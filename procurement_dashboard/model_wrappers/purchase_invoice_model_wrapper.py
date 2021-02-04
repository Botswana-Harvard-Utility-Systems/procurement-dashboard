from django.conf import settings
from edc_model_wrapper import ModelWrapper


class PurchaseInvoiceModelWrapper(ModelWrapper):

    model = 'procurement.purchaseinvoice'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'purchase_order_report_url')
    next_url_attrs = ['order_number', 'vendor', 'company', ]
    querystring_attrs = ['order_number', ]
