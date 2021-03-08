import re

from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import ListboardFilterViewMixin, SearchFormViewMixin
from edc_dashboard.views import ListboardView
from edc_navbar import NavbarViewMixin

# from ...filters import ListboardViewFilters
from ....model_wrappers import CreditCardPurchaseModelWrapper


class ListboardView(EdcBaseViewMixin, NavbarViewMixin,
                    ListboardFilterViewMixin, SearchFormViewMixin,
                    ListboardView):

    listboard_template = 'credit_card_listboard_template'
    listboard_url = 'credit_card_listboard_url'
    listboard_panel_style = 'default'
    listboard_fa_icon = ''

    model_wrapper_cls = CreditCardPurchaseModelWrapper
#     listboard_view_filters = ListboardViewFilters()
    model = 'procurement.creditcardpurchase'
    navbar_name = 'procurement_dashboard'
    navbar_selected_item = 'credit_card'
    search_form_url = 'credit_card_listboard_url'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            cc_purchase_add_url=self.model_cls().get_absolute_url())
        return context

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        if kwargs.get('ccp_number'):
            options.update(
                {'ccp_number': kwargs.get('ccp_number')})
        options.update({'request_by': get_user(request)})
        return options

    def extra_search_options(self, search_term):
        q = Q()
        if re.match('^[A-Z]+$', search_term):
            q = Q(first_name__exact=search_term)
        return q
