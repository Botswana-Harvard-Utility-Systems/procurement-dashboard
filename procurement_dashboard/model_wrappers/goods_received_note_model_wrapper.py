from django.conf import settings
from edc_model_wrapper import ModelWrapper


class GoodsReceivedNoteModelWrapper(ModelWrapper):

    model = 'procurement.goodsreceivednote'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'purchase_order_report_url')
    next_url_attrs = ['order_number', 'vendor']
    querystring_attrs = ['order_number', ]
