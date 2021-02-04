from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist


class PurchaseRequisitionModelWrapperMixin:

    @property
    def purchase_req_model_obj(self):
        """Returns a purchase requisition model instance or None.
        """
        try:
            return self.purchase_requisition_cls.objects.get(
                **self.purchase_requisition_options)
        except ObjectDoesNotExist:
            return None

    @property
    def purchase_requisition_cls(self):
        return django_apps.get_model('procurement.purchaserequisition')

    @property
    def create_purchase_requisition_options(self):
        """Returns a dictionary of options to create a new
        unpersisted purchase requisition model instance.
        """
        options = dict(
            prf_number=self.prf_number, )
        return options

    @property
    def purchase_requisition_options(self):
        """Returns a dictionary of options to get an existing
        purchase order instance.
        """
        options = dict(
            prf_number=self.prf_number, )
        return options
