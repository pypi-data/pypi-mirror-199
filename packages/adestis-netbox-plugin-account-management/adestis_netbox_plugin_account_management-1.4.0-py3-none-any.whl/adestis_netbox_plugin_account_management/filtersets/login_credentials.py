from adestis_netbox_plugin_account_management.models import *
from netbox.filtersets import NetBoxModelFilterSet
from django.db.models import Q
from utilities.forms import DatePicker
from django import forms

__all__ = (
    'LoginCredentialsFilterSet',
)


class LoginCredentialsFilterSet(NetBoxModelFilterSet):
    valid_from = forms.DateField(
        required=False,
        widget=DatePicker
    )

    valid_to = forms.DateField(
        required=False,
        widget=DatePicker
    )

    class Meta:
        model = LoginCredentials
        fields = ['id', 'logon_name', 'login_credentials_status', 'person', 'system', 'valid_from',
                  'valid_to']

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(logon_name__icontains=value) |
            Q(login_credentials_status__icontains=value)
        )
