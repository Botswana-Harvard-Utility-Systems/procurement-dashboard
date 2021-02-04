from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from .purchase_invoice_model_wrapper import PurchaseInvoiceModelWrapper


class PurchaseInvoiceModelWrapperMixin:

    purchase_invoice_model_wrapper_cls = PurchaseInvoiceModelWrapper

    @property
    def purchase_invoice_model_obj(self):
        """Returns a purchase invoice model instance or None.
        """
        try:
            return self.purchase_invoice_cls.objects.get(
                **self.purchase_invoice_options)
        except ObjectDoesNotExist:
            return None

    @property
    def purchase_invoice(self):
        """Returns a wrapped saved or unsaved purchase invoice.
        """
        model_obj = self.purchase_invoice_model_obj or self.purchase_invoice_cls(
            **self.create_purchase_invoice_options)
        return self.purchase_invoice_model_wrapper_cls(model_obj=model_obj)

    @property
    def purchase_invoice_cls(self):
        return django_apps.get_model('procurement.purchaseinvoice')

    @property
    def create_purchase_invoice_options(self):
        """Returns a dictionary of options to create a new
        unpersisted purchase invoice model instance.
        """
        options = dict(
            order_number=self.order_number,
            vendor=self.vendor, )
        return options

    @property
    def purchase_invoice_options(self):
        """Returns a dictionary of options to get an existing
        purchase invoice instance.
        """
        options = dict(
            order_number=self.order_number, )
        return options
