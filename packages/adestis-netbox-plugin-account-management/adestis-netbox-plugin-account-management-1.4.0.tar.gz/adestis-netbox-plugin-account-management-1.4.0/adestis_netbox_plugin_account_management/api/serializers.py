from .nested_serializer import *
from rest_framework import serializers
from adestis_netbox_plugin_account_management.models import *
from netbox.api.serializers import NetBoxModelSerializer

__all__ = (
    'LoginCredentialsSerializer',
    'PersonSerializer',
    'SystemSerializer'
)


class LoginCredentialsSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:adestis_netbox_plugin_account_management-api:logincredentials-detail'
    )

    system = NestedSystemSerializer(many=False,
                                    read_only=False,
                                    required=True)

    person = NestedPersonSerializer(many=False,
                                    read_only=False,
                                    required=True)

    class Meta:
        model = LoginCredentials
        fields = '__all__'
        read_only_fields = ('person', 'system')


class PersonSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:adestis_netbox_plugin_account_management-api:person-detail'
    )

    class Meta:
        model = Person
        fields = (
            'id', 'url', 'display', 'first_name', 'last_name', 'mail_address', 'person_status', 'comments', 'tags',
            'custom_fields', 'created', 'last_updated')


class SystemSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:adestis_netbox_plugin_account_management-api:system-detail'
    )

    class Meta:
        model = System
        fields = ('id', 'url', 'display', 'name', 'system_url', 'system_status', 'comments', 'tags',
                  'custom_fields', 'created', 'last_updated')
