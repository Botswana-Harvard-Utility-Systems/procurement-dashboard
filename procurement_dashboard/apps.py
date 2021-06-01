from django.apps import AppConfig as DjangoAppConfig
from edc_base.apps import AppConfig as BaseEdcBaseAppConfig


class AppConfig(DjangoAppConfig):
    name = 'procurement_dashboard'
    admin_site_name = 'procurement_admin'


class EdcBaseAppConfig(BaseEdcBaseAppConfig):
    project_name = 'Procurement Dashboard'
    institution = 'Botswana Harvard'
    disclaimer = 'BHP Procurement'
