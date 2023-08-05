from adestis_netbox_plugin_account_management.models import *
from netbox.filtersets import NetBoxModelFilterSet
from django.db.models import Q

__all__ = (
    'SystemFilterSet',
)


class SystemFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = System
        fields = ('id', 'name', 'system_url', 'system_status')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(system_url__icontains=value) |
            Q(system_status__icontains=value)
        )
