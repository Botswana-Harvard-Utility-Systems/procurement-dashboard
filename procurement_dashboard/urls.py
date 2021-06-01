from django.urls import path
from edc_dashboard import UrlConfig

from .patterns import order_number, prf_number, ccp_number
from .views import (HomeView, PurchaseOrderListboardView, PurchaseOrderReportView)
from .views import PurchaseRequisitionListboardView, CreditCardPurchaseListboardView
from . import utils

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

purchase_req_listboard_url_config = UrlConfig(
    url_name='purchase_req_listboard_url',
    view_class=PurchaseRequisitionListboardView,
    label='purchase_req_listboard',
    identifier_label='prf_number',
    identifier_pattern=prf_number)

credit_card_listboard_url_config = UrlConfig(
    url_name='credit_card_listboard_url',
    view_class=CreditCardPurchaseListboardView,
    label='credit_card_listboard',
    identifier_label='ccp_number',
    identifier_pattern=ccp_number)

urlpatterns = []
urlpatterns += [path('procurement/', HomeView.as_view(), name='procurement_url')]
urlpatterns += [path('email_report/', utils.email_report, name="email_report_url"),]
urlpatterns += purchase_order_listboard_url_config.listboard_urls
urlpatterns += purchase_order_report_url_config.listboard_urls
urlpatterns += purchase_req_listboard_url_config.listboard_urls
urlpatterns += credit_card_listboard_url_config.listboard_urls
