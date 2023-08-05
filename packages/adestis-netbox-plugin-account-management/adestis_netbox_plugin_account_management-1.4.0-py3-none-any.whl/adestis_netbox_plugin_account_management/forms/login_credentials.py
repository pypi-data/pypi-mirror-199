from django import forms
from django.core.exceptions import ValidationError
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField
from utilities.forms import DatePicker
from adestis_netbox_plugin_account_management.models import *

__all__ = (
    'LoginCredentialsForm',
    'LoginCredentialsFilterForm',
)


class LoginCredentialsForm(NetBoxModelForm):
    comments = CommentField()

    person = DynamicModelChoiceField(
        queryset=Person.objects.all()
    )

    system = DynamicModelChoiceField(
        queryset=System.objects.all()
    )

    class Meta:
        model = LoginCredentials
        fields = ['logon_name', 'person', 'system', 'valid_from', 'valid_to',
                  'login_credentials_status', 'comments', 'tags']
        widgets = {
            'valid_from': DatePicker(),
            'valid_to': DatePicker()
        }
        help_texts = {
            'logon_name': "Logon name",
        }

    def clean(self):
        cleaned_data = super().clean()
        valid_from_data = cleaned_data.get("valid_from")
        valid_to_data = cleaned_data.get("valid_to")

        if valid_from_data and valid_to_data:
            # Only do something if both fields are valid so far.
            if valid_to_data < valid_from_data:
                raise ValidationError(
                    "Invalid date range! Field 'Valid to' must be older than field 'Valid from'"
                )


class LoginCredentialsFilterForm(NetBoxModelFilterSetForm):
    model = LoginCredentials

    index = forms.IntegerField(
        required=False
    )

    person = forms.ModelMultipleChoiceField(
        queryset=Person.objects.all(),
        required=True
    )

    system = forms.ModelMultipleChoiceField(
        queryset=System.objects.all(),
        required=True
    )

    login_credentials_status = forms.MultipleChoiceField(
        choices=LoginCredentialsStatusChoices,
        required=False
    )
