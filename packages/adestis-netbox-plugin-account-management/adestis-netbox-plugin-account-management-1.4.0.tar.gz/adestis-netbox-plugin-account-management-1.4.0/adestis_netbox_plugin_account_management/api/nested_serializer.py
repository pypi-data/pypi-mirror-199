from rest_framework import serializers
from adestis_netbox_plugin_account_management.models import *
from netbox.api.serializers import WritableNestedSerializer

__all__ = (
    'NestedSystemSerializer',
    'NestedPersonSerializer',
)


class NestedPersonSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:adestis_netbox_plugin_account_management-api:person-detail'
    )

    class Meta:
        model = Person
        fields = '__all__'


class NestedSystemSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:adestis_netbox_plugin_account_management-api:system-detail'
    )

    class Meta:
        model = System
        fields = ('id', 'url', 'display', 'name')
