from edc_dashboard.listboard_filter import ListboardFilter, ListboardViewFilters


class ListboardViewFilters(ListboardViewFilters):

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

    rejected = ListboardFilter(
        name='rejected',
        label='Rejected',
        lookup={'status__is': 'rejected'})


class POListboardFilters(ListboardViewFilters):

    all = ListboardFilter(
        name='all',
        label='All',
        lookup={})

    authorised = ListboardFilter(
        name='authorised',
        label='Authorised',
        lookup={'authorised': True})

    unathorised = ListboardFilter(
        name='unathorised',
        label='Unauthorised',
        lookup={'authorised': False})

    paid = ListboardFilter(
        name='paid',
        label='Paid',
        lookup={'invoicepaid__is': True})

    unpaid = ListboardFilter(
        name='unpaid',
        label='Not Paid',
        lookup={'invoicepaid__is': False})

    due = ListboardFilter(
        name="due",
        label='Due Payment',
        lookup={'invoicepaid__is': 'due'})
