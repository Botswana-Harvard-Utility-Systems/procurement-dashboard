from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from .purchase_order_model_wrapper import PurchaseOrderModelWrapper


class PurchaseOrderModelWrapperMixin:

    purchase_order_model_wrapper_cls = PurchaseOrderModelWrapper

    @property
    def purchase_order_model_obj(self):
        """Returns a purchase order model instance or None.
        """
        try:
            return self.purchase_order_cls.objects.get(
                **self.purchase_order_options)
        except ObjectDoesNotExist:
            return None

    @property
    def purchase_order(self):
        """Returns a wrapped saved or unsaved purchase order.
        """
        model_obj = self.purchase_order_model_obj or self.purchase_order_cls(
            **self.create_purchase_order_options)
        return self.purchase_order_model_wrapper_cls(model_obj=model_obj)

    @property
    def purchase_order_cls(self):
        return django_apps.get_model('procurement.purchaseorder')

    @property
    def create_purchase_order_options(self):
        """Returns a dictionary of options to create a new
        unpersisted purchase order model instance.
        """
        options = dict(
            prf_number=self.prf_number, )
        return options

    @property
    def purchase_order_options(self):
        """Returns a dictionary of options to get an existing
        purchase order instance.
        """
        options = dict(
            prf_number=self.prf_number, )
        return options

    @property
    def order_number(self):
        self.purchase_order_model_obj.order_number
