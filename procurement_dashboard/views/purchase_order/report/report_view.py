import base64
from io import BytesIO
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import TemplateRequestContextMixin
from edc_navbar import NavbarViewMixin
from pdf2image import convert_from_path


from ..view_mixin import PdfResponseMixin, PurchaseOrderCalcMixin


class ReportView(PdfResponseMixin, PurchaseOrderCalcMixin, NavbarViewMixin,
                 EdcBaseViewMixin, TemplateRequestContextMixin, TemplateView):

    template_name = 'procurement_dashboard/purchase_order/dashboard.html'
    report_template = 'purchase_order_report_template'
    pdf_name = 'purchase_orders'
    model = 'procurement.purchaseorder'
    navbar_name = 'procurement_dashboard'
    navbar_selected_item = 'purchase_order'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def purchase_order(self, order_number=None):
        try:
            purchase_order = self.model_cls.objects.get(
                order_number=order_number)
        except self.model_cls.DoesNotExist:
            raise ValidationError(
                f'Purchase Order number {order_number} does not exist.')
        else:
            return purchase_order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_number = kwargs.get('order_number', None)
        purchase_order = self.purchase_order(order_number=order_number)
        pdf_images_bytes = self.pdf_images_as_bytes(purchase_order)
        context.update(
            order_number=order_number,
            result=purchase_order,
            pdf_images_bytes=pdf_images_bytes)
        return context

    def model_obj_set(self, model_obj):
        order_items = super().model_obj_set(model_obj)
        order_items.extend(list(model_obj.purchaseorderitem_set.all()))
        return order_items

    def filter_options(self, **kwargs):
        options = super().filter_options(**kwargs)
        if kwargs.get('order_number'):
            options.update(
                {'order_number': kwargs.get('order_number')})
        return options

    @property
    def pdf_template(self):
        return self.get_template_from_context(self.report_template)

    def pdf_images_as_bytes(self, model_obj):
        base_dir = settings.BASE_DIR
        pdf_path = f'{base_dir}{model_obj.file.url}'
        image_bytes = []
        pdf_images = convert_from_path(pdf_path)
        buffer = BytesIO()
        for pdf_image in pdf_images:
            pdf_image.save(buffer, "PNG")
            img_str = base64.b64encode(buffer.getvalue()).decode('ascii')
            image_bytes.append(img_str)
        return image_bytes
