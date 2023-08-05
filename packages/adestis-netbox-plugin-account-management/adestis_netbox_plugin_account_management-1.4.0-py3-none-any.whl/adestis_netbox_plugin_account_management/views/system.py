from netbox.views import generic
from adestis_netbox_plugin_account_management.forms import *
from adestis_netbox_plugin_account_management.models import *
from adestis_netbox_plugin_account_management.filtersets import *
from adestis_netbox_plugin_account_management.tables import *

__all__ = (
    'SystemView',
    'SystemListView',
    'SystemEditView',
    'SystemDeleteView',
)


class SystemView(generic.ObjectView):
    queryset = System.objects.all()

    def get_extra_context(self, request, instance):
        filtered_data = LoginCredentials.objects.filter(
            system=instance
        )
        person_filtered_table = LoginCredentialsTable(filtered_data, )

        return {
            'person_filtered_table': person_filtered_table,
        }


class SystemListView(generic.ObjectListView):
    queryset = System.objects.all()
    table = SystemTable
    filterset = SystemFilterSet
    filterset_form = SystemFilterForm


class SystemEditView(generic.ObjectEditView):
    queryset = System.objects.all()
    form = SystemForm


class SystemDeleteView(generic.ObjectDeleteView):
    queryset = System.objects.all()
