from django.apps import apps as django_apps
from django.conf import settings
from edc_model_wrapper import ModelWrapper

from .goods_received_model_wrapper_mixin import GoodsReceivedNoteModelWrapperMixin
from .purchase_invoice_model_wrapper_mixin import PurchaseInvoiceModelWrapperMixin
from .purchase_requisition_model_wrapper_mixin import PurchaseRequisitionModelWrapperMixin
from .request_approval_model_wrapper_mixin import RequestApprovalModelWrapperMixin


class PurchaseOrderModelWrapper(RequestApprovalModelWrapperMixin,
                                GoodsReceivedNoteModelWrapperMixin,
                                PurchaseInvoiceModelWrapperMixin,
                                PurchaseRequisitionModelWrapperMixin,
                                ModelWrapper):

    model = 'procurement.purchaseorder'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'purchase_order_listboard_url')
    next_url_attrs = ['prf_number', 'request_type', ]
    querystring_attrs = ['prf_number', ]
    prf_model = 'procurement.purchaserequisition'

    @property
    def document_id(self):
        return self.order_number

    @property
    def prf_number(self):
        return self.object.prf_number

    @property
    def vendor(self):
        prf_model_cls = django_apps.get_model(self.prf_model)
        try:
            prf = prf_model_cls.objects.get(prf_number=self.prf_number)
        except prf_model_cls.DoesNotExist:
            return None
        else:
            return prf.selected_vendor

    @property
    def purchase_items_total(self):
        order_items = self.purchase_req_model_obj.purchaserequisitionitem_set.all()
        total = 0
        for order_item in order_items:
            total += order_item.total_price_incl
        return float(total)

    @property
    def bhp_allocation(self):
        names = []
        allocations = self.purchase_req_model_obj.allocation_set.all()
        for allocation in allocations:
            names.append(f'{allocation.bhp_allocation.name}({allocation.percentage}%)')
        return ', '.join(names)

    @property
    def invoice_status(self):
        if self.purchase_invoice_model_obj:
            if self.purchase_invoice_model_obj.paid:
                return 'Paid'
            else:
                return 'Not Paid'
        return '--'
