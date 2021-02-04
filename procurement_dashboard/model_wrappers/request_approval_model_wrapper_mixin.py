from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .request_approval_model_wrapper import RequestApprovalModelWrapper
from .request_model_wrapper import RequestModelWrapper


class RequestApprovalModelWrapperMixin:

    request_approval_model_wrapper_cls = RequestApprovalModelWrapper
    request_model_wrapper_cls = RequestModelWrapper

    @property
    def request_model_cls(self):
        return django_apps.get_model('procurement.request')

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
    def request_model_obj(self):
        return self.request_approval_model_obj.request_set.all().order_by(
            '-date_reviewed').first() if self.request_approval_model_obj else None

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
        request_by = self.object.request_by if self.object.request else None
        options = dict(
            document_id=self.document_id,
            request_by=request_by,)
        return options

    @property
    def request_approval_options(self):
        """Returns a dictionary of options to get an existing
        request approval instance.
        """
        options = dict(
            document_id=self.document_id)
        return options

    @property
    def requests(self):
        wrapped_entries = []
        requests = self.request_model_cls.objects.filter(
            request_approval=self.request_approval_model_obj)
        request_type = self.request_type if self.request_type else None
        for request in requests:
            wrapped_entries.append(
                self.request_model_wrapper_cls(request, request_type=request_type))
        return wrapped_entries

    @property
    def request_by_approver(self):
        try:
            request_by_approver = self.request_model_cls.objects.get(
                request_approval=self.request_approval_model_obj,
                request_to=self.request_to)
        except self.request_model_cls.DoesNotExist:
            return None
        else:
            request_type = self.request_type if self.request_type else None
            order_number = self.order_number if self.order_number else None
            return self.request_model_wrapper_cls(
                request_by_approver, request_type=request_type, order_number=order_number)

    @property
    def approval_request(self):
        request = self.request_model_cls(
            request_approval=self.request_approval_model_obj)
        request_type = self.request_type if self.request_type else None
        order_number = self.order_number if self.order_number else None
        return self.request_model_wrapper_cls(
            request, request_type=request_type, order_number=order_number)

    @property
    def request_approved(self):
        return self.request_approval_model_obj.approved

    def request_to_user(self, user):
        request = self.request_approval_model_obj.request_set.filter(
            request_to__id=user.id)
        if request and len(request) == 1:
            request_type = self.request_type if self.request_type else None
            return self.request_model_wrapper_cls(request[0], request_type=request_type)
