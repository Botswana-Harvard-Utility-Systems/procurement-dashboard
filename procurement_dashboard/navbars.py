from django.conf import settings
from edc_navbar import NavbarItem, site_navbars, Navbar


no_url_namespace = True if settings.APP_NAME == 'procurement_dashboard' else False

procurement_dashboard = Navbar(name='procurement_dashboard')

procurement_dashboard.append_item(
    NavbarItem(
        name='procurement',
        label='Dashboard',
        fa_icon='fa fa-home',
        url_name=settings.DASHBOARD_URL_NAMES.get('procurement_url')))

# procurement_dashboard.append_item(
#     NavbarItem(
#         name='purchase_order',
#         title='Purchase Order',
#         label='Purchase Order',
#         fa_icon='fa fa-list-alt',
#         url_name=settings.DASHBOARD_URL_NAMES[
#             'purchase_order_listboard_url'],
#         no_url_namespace=no_url_namespace))
# 
# procurement_dashboard.append_item(
#     NavbarItem(
#         name='purchase_requisition',
#         title='Purchase Requisition',
#         label='Purchase Requisition',
#         fa_icon='fa fa-list-alt',
#         url_name=settings.DASHBOARD_URL_NAMES[
#             'purchase_req_listboard_url'],
#         no_url_namespace=no_url_namespace))

site_navbars.register(procurement_dashboard)
