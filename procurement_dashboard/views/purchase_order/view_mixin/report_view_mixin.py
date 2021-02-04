from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from django.views.generic.base import ContextMixin

from ....model_wrappers import PurchaseOrderModelWrapper


class ReportViewMixin(ContextMixin):

    def purchase_order(self, order_number=None):
        try:
            purchase_order = self.model_cls.objects.get(
                order_number=order_number)
        except self.model_cls.DoesNotExist:
            raise ValidationError(
                f'Purchase Order number {order_number} does not exist.')
        else:
            return purchase_order

    def purchase_requisition(self, prf_number):
        prf_model_cls = django_apps.get_model('procurement.purchaserequisition')
        try:
            prf_obj = prf_model_cls.objects.get(prf_number=prf_number)
        except prf_model_cls.DoesNotExist:
            raise ValidationError('Purchase requisition does not exist.')
        else:
            return prf_obj

    def justification(self, prf_number):
        justification_cls = django_apps.get_model('procurement.vendorjustification')
        try:
            justification = justification_cls.objects.get(prf_number=prf_number)
        except justification_cls.DoesNotExist:
            raise ValidationError('Vendor justification does not exist.')
        else:
            return justification

    def goods_received_note(self, order_number):
        goods_received_cls = django_apps.get_model('procurement.goodsreceivednote')
        try:
            goods_received = goods_received_cls.objects.get(order_number=order_number)
        except goods_received_cls.DoesNotExist:
            return None
        else:
            return goods_received

    def purchase_invoice(self, order_number):
        purchase_invoice_cls = django_apps.get_model('procurement.purchaseinvoice')
        try:
            purchase_invoice = purchase_invoice_cls.objects.get(order_number=order_number)
        except purchase_invoice_cls.DoesNotExist:
            return None
        else:
            return purchase_invoice

    @property
    def wrapped_purchase_order(self):
        purchase_order = self.purchase_order(self.kwargs.get('order_number', None))
        return PurchaseOrderModelWrapper(purchase_order, request_type=None)

    @property
    def wrapped_by_first_approver(self):
        purchase_order = self.purchase_order(self.kwargs.get('order_number', None))
        return PurchaseOrderModelWrapper(
            purchase_order, request_type=None, request_to=purchase_order.first_approver)

    @property
    def wrapped_by_second_approver(self):
        purchase_order = self.purchase_order(self.kwargs.get('order_number', None))
        return PurchaseOrderModelWrapper(
            purchase_order, request_type=None, request_to=purchase_order.second_approver)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_number = kwargs.get('order_number', None)
        purchase_order = self.purchase_order(order_number=order_number)
        prf = self.purchase_requisition(purchase_order.prf_number)
        add_request_href = self.wrapped_purchase_order.approval_request.href
        approved = purchase_order.authorised
        auth_one_request = self.wrapped_by_first_approver.request_by_approver
        auth_two_request = self.wrapped_by_second_approver.request_by_approver
        goods_received = self.goods_received_note(order_number=order_number)
        purchase_invoice = self.purchase_invoice(order_number=order_number)
        context.update(
            prf_obj=prf,
            wrapped_purchase_order=self.wrapped_purchase_order,
            add_request_href=add_request_href,
            auth_one_request=auth_one_request,
            auth_two_request=auth_two_request,
            purchase_invoice=purchase_invoice,
            goods_received=goods_received,
            approved=approved)
        return context
