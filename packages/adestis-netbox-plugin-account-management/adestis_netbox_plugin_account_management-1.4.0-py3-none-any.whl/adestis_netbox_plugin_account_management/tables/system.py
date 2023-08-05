import django_tables2 as tables

from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from adestis_netbox_plugin_account_management.models import *


class SystemTable(NetBoxTable):
    name = tables.Column(
        linkify=True,
    )

    system_status = ChoiceFieldColumn()

    comments = columns.MarkdownColumn()

    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        model = System
        fields = (
        'pk', 'id', 'name', 'system_url', 'system_status', 'comments', 'actions', 'tags', 'created', 'last_updated')
        default_columns = ('name', 'system_url', 'system_status')
