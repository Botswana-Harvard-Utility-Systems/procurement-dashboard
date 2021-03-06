import re

from django.apps import apps as django_apps
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import ListboardFilterViewMixin, SearchFormViewMixin
from edc_dashboard.views import ListboardView
from edc_navbar import NavbarViewMixin

from ...filters import ListboardViewFilters
from ....model_wrappers import PurchaseRequisitionModelWrapper


class ListboardView(EdcBaseViewMixin, NavbarViewMixin,
                    ListboardFilterViewMixin, SearchFormViewMixin,
                    ListboardView):

    listboard_template = 'purchase_req_listboard_template'
    listboard_url = 'purchase_req_listboard_url'
    listboard_panel_style = 'default'
    listboard_fa_icon = ''

    model_wrapper_cls = PurchaseRequisitionModelWrapper
    listboard_view_filters = ListboardViewFilters()
    model = 'procurement.purchaserequisition'
    navbar_name = 'procurement_dashboard'
    navbar_selected_item = 'purchase_requisition'
    search_form_url = 'purchase_req_listboard_url'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request_type = self.request.GET.get('request_type', None)
        context.update(
            purchase_req_add_url=self.model_cls().get_absolute_url(),
            request_type=request_type)
        return context

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        if kwargs.get('prf_number'):
            options.update(
                {'prf_number': kwargs.get('prf_number')})
        request_type = request.GET.get('request_type')
        if request_type == 'requests':
            options.update({'request_by': get_user(request)})
        elif request_type == 'approvals':
            options.update(
                {'approval_by': get_user(request)})
        elif request_type == 'confirmfunds':
            options.update(
                {'funds_confirmed': get_user(request)})

        status_filter = options.get('status__is', '')
        if status_filter:
            options = {key: val for key, val in options.items() if key != 'status__is'}
            ids = self.requisition_ids(status_filter)
            options.update({'prf_number__in': ids})

        return options

    def extra_search_options(self, search_term):
        q = Q()
        if re.match('^[A-Z]+$', search_term):
            q = Q(first_name__exact=search_term)
        return q

    def get_wrapped_queryset(self, queryset):
        """Returns a list of wrapped model instances.
        """
        request_type = self.request.GET.get('request_type')
        object_list = []
        for obj in queryset:
            object_list.append(
                self.model_wrapper_cls(obj, request_type=request_type))
        return object_list

    def requisition_ids(self, status):
        ids = []
        request = django_apps.get_model('procurement.request')
        requests = request.objects.filter(status=status)
        if requests:
            for req in requests:
                request_type = self.request.GET.get('request_type')
                user_logged = self.request.user.id
                if request_type in ['approvals', 'confirmfunds']:
                    if req.request_to.id != user_logged:
                        continue
                ids.append(req.request_approval.document_id)
        return ids
