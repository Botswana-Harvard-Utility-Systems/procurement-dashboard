import re

from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import ListboardFilterViewMixin, SearchFormViewMixin
from edc_dashboard.views import ListboardView
from edc_navbar import NavbarViewMixin

from ....model_wrappers import PurchaseOrderModelWrapper


class ListboardView(EdcBaseViewMixin, NavbarViewMixin,
                    ListboardFilterViewMixin, SearchFormViewMixin,
                    ListboardView):

    listboard_template = 'purchase_order_listboard_template'
    listboard_url = 'purchase_order_listboard_url'
    listboard_panel_style = 'success'
    listboard_fa_icon = 'fa fa-list-alt'

    model = 'procurement.purchaseorder'
    model_wrapper_cls = PurchaseOrderModelWrapper
    navbar_name = 'procurement_dashboard'
    navbar_selected_item = 'purchase_order'
    search_form_url = 'purchase_order_listboard_url'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            purchase_order_add_url=self.model_cls().get_absolute_url())
        return context

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        if kwargs.get('order_number'):
            options.update(
                {'order_number': kwargs.get('order_number')})
        return options

    def get_queryset(self):
        qs = super().get_queryset()

        current_user = get_user(self.request)
        groups = current_user.groups.all()
        group_names = [group.name for group in groups if groups]
        if not all(group in ['Procurement', 'Finance'] for group in group_names):
            qs = qs.filter(
                Q(first_approver=current_user) | Q(second_approver=current_user))
        return qs

    def extra_search_options(self, search_term):
        q = Q()
        if re.match('^[A-Z]+$', search_term):
            q = Q(first_name__exact=search_term)
        return q
