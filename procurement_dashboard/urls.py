from django.urls import path
from edc_dashboard import UrlConfig

from .patterns import order_number
from .views import (HomeView, PurchaseOrderListboardView, PurchaseOrderReportView)

app_name = 'procurement_dashboard'

purchase_order_listboard_url_config = UrlConfig(
    url_name='purchase_order_listboard_url',
    view_class=PurchaseOrderListboardView,
    label='purchase_order_listboard',
    identifier_label='order_number',
    identifier_pattern=order_number)

purchase_order_report_url_config = UrlConfig(
    url_name='purchase_order_report_url',
    view_class=PurchaseOrderReportView,
    label='purchase_order_report',
    identifier_label='order_number',
    identifier_pattern=order_number)

urlpatterns = []
urlpatterns += [path('procurement/', HomeView.as_view(), name='procurement_url')]
urlpatterns += purchase_order_listboard_url_config.listboard_urls
urlpatterns += purchase_order_report_url_config.listboard_urls
