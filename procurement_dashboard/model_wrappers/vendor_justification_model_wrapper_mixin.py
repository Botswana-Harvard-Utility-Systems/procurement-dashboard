from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .vendor_justification_model_wrapper import VendorJustificationModelWrapper


class VendorJustificationModelWrapperMixin:

    vendor_justification_model_wrapper_cls = VendorJustificationModelWrapper

    @property
    def vendor_justification_model_obj(self):
        """Returns a vendor justification model instance or None.
        """
        try:
            return self.vendor_justification_cls.objects.get(
                **self.vendor_justification_options)
        except ObjectDoesNotExist:
            return None

    @property
    def vendor_justification(self):
        """Returns a wrapped saved or unsaved vendor justification.
        """
        model_obj = self.vendor_justification_model_obj or self.vendor_justification_cls(
            **self.create_vendor_justification_options)
        return self.vendor_justification_model_wrapper_cls(
            model_obj=model_obj, request_type=self.request_type)

    @property
    def vendor_justification_cls(self):
        return django_apps.get_model('procurement.vendorjustification')

    @property
    def create_vendor_justification_options(self):
        """Returns a dictionary of options to create a new
        unpersisted vendor justification model instance.
        """
        options = dict(
            prf_number=self.prf_number,
            selected_vendor=self.object.selected_vendor, )
        return options

    @property
    def vendor_justification_options(self):
        """Returns a dictionary of options to get an existing
        vendor justification instance.
        """
        options = dict(
            prf_number=self.prf_number)
        return options
