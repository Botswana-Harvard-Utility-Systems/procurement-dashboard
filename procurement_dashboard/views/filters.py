from edc_dashboard.listboard_filter import ListboardFilter, ListboardViewFilters


class ListboardViewFilters(ListboardViewFilters):

    def __init__(self, departments=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

    all = ListboardFilter(
        name='all',
        label='All',
        lookup={})

    pending = ListboardFilter(
        name='pending',
        label='Pending Approval',
        lookup={'status__is': 'pending'})

    approved = ListboardFilter(
        name='approved',
        label='Approved',
        lookup={'status__is': 'approved'})

    new = ListboardFilter(
        name='new',
        label='New Requisitions',
        lookup={'status__is': 'new'})
