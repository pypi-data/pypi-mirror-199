from netbox.views import generic
from adestis_netbox_plugin_account_management.forms import *
from adestis_netbox_plugin_account_management.models import *
from adestis_netbox_plugin_account_management.filtersets import *
from adestis_netbox_plugin_account_management.tables import *

__all__ = (
    'PersonView',
    'PersonListView',
    'PersonEditView',
    'PersonDeleteView',
)


class PersonView(generic.ObjectView):
    queryset = Person.objects.all()

    def get_extra_context(self, request, instance):
        filtered_data = LoginCredentials.objects.filter(
            person=instance
        )
        person_filtered_table = LoginCredentialsTable(filtered_data, )

        return {
            'person_filtered_table': person_filtered_table,
        }


class PersonListView(generic.ObjectListView):
    queryset = Person.objects.all()
    table = PersonTable
    filterset = PersonFilterSet
    filterset_form = PersonFilterForm


class PersonEditView(generic.ObjectEditView):
    queryset = Person.objects.all()
    form = PersonForm


class PersonDeleteView(generic.ObjectDeleteView):
    queryset = Person.objects.all()
