from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import CommentField
from adestis_netbox_plugin_account_management.models import *

__all__ = (
    'PersonForm',
    'PersonFilterForm',
)


class PersonForm(NetBoxModelForm):
    comments = CommentField()

    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'mail_address', 'person_status', 'comments', 'tags')


class PersonFilterForm(NetBoxModelFilterSetForm):
    model = Person

    index = forms.IntegerField(
        required=False
    )

    person_status = forms.MultipleChoiceField(
        choices=PersonStatusChoices,
        required=False
    )
