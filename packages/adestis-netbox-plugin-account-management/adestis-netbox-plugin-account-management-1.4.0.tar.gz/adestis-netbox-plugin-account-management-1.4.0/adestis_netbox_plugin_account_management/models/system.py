from django.db import models
from django.urls import reverse

from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet

from adestis_netbox_plugin_account_management.models import *

__all__ = (
    'SystemStatusChoices',
    'System',
)


class SystemStatusChoices(ChoiceSet):
    key = 'System.status'

    STATUS_OFFLINE = 'offline'
    STATUS_ACTIVE = 'active'
    STATUS_PLANNED = 'planned'
    STATUS_STAGED = 'staged'
    STATUS_FAILED = 'failed'
    STATUS_INVENTORY = 'inventory'
    STATUS_DECOMMISSIONING = 'decommissioning'

    CHOICES = [
        (STATUS_ACTIVE, 'Active', 'green'),
        (STATUS_OFFLINE, 'Offline', 'gray'),
        (STATUS_PLANNED, 'Planned', 'cyan'),
        (STATUS_STAGED, 'Staged', 'blue'),
        (STATUS_FAILED, 'Failed', 'red'),
        (STATUS_INVENTORY, 'Inventory', 'purple'),
        (STATUS_DECOMMISSIONING, 'Decommissioning', 'yellow'),
    ]


class System(NetBoxModel):
    name = models.CharField(
        max_length=130
    )

    system_url = models.CharField(
        max_length=2048,
        verbose_name='URL/Identification',
        blank=True
    )

    system_status = models.CharField(
        max_length=50,
        choices=SystemStatusChoices,
        verbose_name='Status'
    )

    comments = models.TextField(
        blank=True
    )

    class Meta:
        verbose_name_plural = "Systems"
        verbose_name = 'System'
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(
                fields=['system_url'],
                name='%(app_label)s_%(class)s_unique_system_url'
            )
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:adestis_netbox_plugin_account_management:system', args=[self.pk])

    def get_system_status_color(self):
        return SystemStatusChoices.colors.get(self.system_status)
