from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import CommentField
from adestis_netbox_plugin_account_management.models import *

__all__ = (
    'SystemForm',
    'SystemFilterForm',
)


class SystemForm(NetBoxModelForm):
    comments = CommentField()

    class Meta:
        model = System
        fields = ('name', 'system_url', 'system_status', 'comments', 'tags')


class SystemFilterForm(NetBoxModelFilterSetForm):
    model = System

    index = forms.IntegerField(
        required=False
    )
    
    system_url = forms.CharField(
        required=False
    )

    system_status = forms.MultipleChoiceField(
        choices=SystemStatusChoices,
        required=False
    )
