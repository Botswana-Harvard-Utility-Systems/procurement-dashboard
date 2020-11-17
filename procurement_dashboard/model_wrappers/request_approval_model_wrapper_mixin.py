from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .request_approval_model_wrapper import RequestApprovalModelWrapper


class RequestApprovalModelWrapperMixin:

    request_approval_model_wrapper_cls = RequestApprovalModelWrapper

    @property
    def request_approval_model_obj(self):
        """Returns a request approval model instance or None.
        """
        try:
            return self.request_approval_cls.objects.get(
                **self.request_approval_options)
        except ObjectDoesNotExist:
            return None

    @property
    def request_approval(self):
        """Returns a wrapped saved or unsaved request approval.
        """
        model_obj = self.request_approval_model_obj or self.request_approval_cls(
            **self.create_request_approval_options)
        return self.request_approval_model_wrapper_cls(model_obj=model_obj)

    @property
    def request_approval_cls(self):
        return django_apps.get_model('procurement.requestapproval')

    @property
    def create_request_approval_options(self):
        """Returns a dictionary of options to create a new
        unpersisted request approval model instance.
        """
        options = dict(
            document_id=self.document_id,
            request_by=self.object.request_by,
            status='new', )
        return options

    @property
    def request_approval_options(self):
        """Returns a dictionary of options to get an existing
        request approval instance.
        """
        options = dict(
            document_id=self.document_id)
        return options

    def current_user(self):
        import pdb; pdb.set_trace()
