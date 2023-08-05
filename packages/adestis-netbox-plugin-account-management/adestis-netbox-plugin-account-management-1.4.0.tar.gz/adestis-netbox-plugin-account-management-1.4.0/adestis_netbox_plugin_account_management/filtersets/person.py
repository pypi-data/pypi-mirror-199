from adestis_netbox_plugin_account_management.models import *
from netbox.filtersets import NetBoxModelFilterSet
from django.db.models import Q

__all__ = (
    'PersonFilterSet',
)


class PersonFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = Person
        fields = ('id', 'first_name', 'last_name', 'mail_address', 'person_status')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(first_name__icontains=value) |
            Q(last_name__icontains=value) |
            Q(mail_address__icontains=value) |
            Q(person_status__icontains=value)
        )
