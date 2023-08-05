import django_tables2 as tables

from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from adestis_netbox_plugin_account_management.models import *


class PersonTable(NetBoxTable):
    first_name = tables.Column(
        linkify=True
    )

    last_name = tables.Column(
        linkify=True
    )

    person_status = ChoiceFieldColumn()

    comments = columns.MarkdownColumn()

    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        model = Person
        fields = ('pk', 'id', 'first_name', 'last_name', 'mail_address', 'person_status', 'comments', 'actions', 'tags',
                  'created', 'last_updated')
        default_columns = ('first_name', 'last_name', 'mail_address', 'person_status')
