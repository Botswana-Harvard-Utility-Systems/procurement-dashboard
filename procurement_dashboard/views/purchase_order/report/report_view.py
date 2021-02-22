from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import TemplateRequestContextMixin
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from edc_navbar import NavbarViewMixin


from ..view_mixin import PdfResponseMixin, PurchaseOrderCalcMixin


class ReportViewError(Exception):
    pass


class ReportView(EdcBaseViewMixin, PurchaseOrderCalcMixin, PdfResponseMixin,
                 NavbarViewMixin, TemplateRequestContextMixin, TemplateView):

    template_name = 'procurement_dashboard/purchase_order/dashboard.html'
    report_template = 'purchase_order_report_template'
    pdf_name = 'purchase_orders'
    model = 'procurement.purchaseorder'
    navbar_name = 'procurement_dashboard'
    navbar_selected_item = 'purchase_order'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_number = kwargs.get('order_number', None)
        context.update(order_number=order_number)
        return context

    def filter_options(self, **kwargs):
        options = super().filter_options(**kwargs)
        if kwargs.get('order_number'):
            options.update(
                {'order_number': kwargs.get('order_number')})
        return options

    def model_obj_set(self, model_obj):
        order_items = super().model_obj_set(model_obj)
        prf_obj = self.purchase_requisition(prf_number=model_obj.prf_number)
        order_items.extend(list(prf_obj.purchaserequisitionitem_set.all()))
        return order_items

    @property
    def pdf_template(self):
        return self.get_template_from_context(self.report_template)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            purchase_invoice = self.purchase_invoice(
                    order_number=kwargs.get('order_number'))
            if request.POST.get('publish'):
                if purchase_invoice:
                    purchase_invoice.published = True
                    purchase_invoice.save()
            elif request.POST.get('_update'):
                invoice_status = request.POST.get('invoice_status')
                if invoice_status == 'Paid':
                    purchase_invoice.paid = True
                else:
                    purchase_invoice.paid = False
                purchase_invoice.save()
            try:
                url_name = request.url_name_data['purchase_order_report_url']
            except KeyError as e:
                raise ReportViewError(
                    f'Invalid action \'post_action_url\'. Got {e}. See {repr(self)}.')
            url = reverse(url_name, kwargs=kwargs)
            return HttpResponseRedirect(url)
