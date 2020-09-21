from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import TemplateRequestContextMixin

from ..view_mixin import PdfResponseMixin


class ReportView(
        PdfResponseMixin, EdcBaseViewMixin, TemplateRequestContextMixin, TemplateView):

    report_template = 'purchase_order_report_template'
    pdf_name = 'purchase_orders'

    @property
    def model_cls(self):
        return django_apps.get_model('procurement.purchaseorder')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def purchase_order(self, order_number=None):
        try:
            purchase_order = self.model_cls.objects.get(
                order_number=order_number)
        except self.model_cls.DoesNotExist:
            raise ValidationError(
                f"Purchase Order number {order_number} does not exist.")
        else:
            return purchase_order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_number = kwargs.get('order_number', None)
        context.update(
            order_number=order_number,
            purchase_order=self.purchase_order(order_number=order_number))
        return context

    def get_template_names(self):
        return [self.get_template_from_context(self.report_template)]
