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

    def approved(self, overall_sum_incl, purchase_order):
        approved = False
        if purchase_order.first_approval:
            approved = True
            if overall_sum_incl and overall_sum_incl > 5000:
                approved = True if purchase_order.second_approval else False
        return approved

    @property
    def wrapped_purchase_order(self):
        purchase_order = self.purchase_order(self.kwargs.get('order_number', None))
        return PurchaseOrderModelWrapper(purchase_order, request_type=None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_number = kwargs.get('order_number', None)
        purchase_order = self.purchase_order(order_number=order_number)
        prf = self.purchase_requisition(purchase_order.prf_number)
        add_request_href = self.wrapped_purchase_order.approval_request.href
        overall_sum_incl = context.get('overall_sum_incl', None)
        approved = self.approved(overall_sum_incl, purchase_order)
        context.update(
            prf_obj=prf,
            add_request_href=add_request_href,
            approved=approved)
        return context
