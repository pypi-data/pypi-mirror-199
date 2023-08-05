from netbox.views import generic
from adestis_netbox_plugin_account_management.forms import *
from adestis_netbox_plugin_account_management.models import *
from adestis_netbox_plugin_account_management.filtersets import *
from adestis_netbox_plugin_account_management.tables import *

__all__ = (
    'LoginCredentialsView',
    'LoginCredentialsListView',
    'LoginCredentialsEditView',
    'LoginCredentialsDeleteView',
)


class LoginCredentialsView(generic.ObjectView):
    queryset = LoginCredentials.objects.all()


class LoginCredentialsListView(generic.ObjectListView):
    queryset = LoginCredentials.objects.all()
    table = LoginCredentialsTable
    filterset = LoginCredentialsFilterSet
    filterset_form = LoginCredentialsFilterForm


class LoginCredentialsEditView(generic.ObjectEditView):
    queryset = LoginCredentials.objects.all()
    form = LoginCredentialsForm


class LoginCredentialsDeleteView(generic.ObjectDeleteView):
    queryset = LoginCredentials.objects.all()
