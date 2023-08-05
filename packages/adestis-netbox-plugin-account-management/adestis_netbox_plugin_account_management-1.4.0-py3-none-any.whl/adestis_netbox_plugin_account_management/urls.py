from django.urls import path

from netbox.views.generic import ObjectChangeLogView
from adestis_netbox_plugin_account_management.models import *
from adestis_netbox_plugin_account_management.views import *

urlpatterns = (

    # System lists
    path('systems/', SystemListView.as_view(), name='system_list'),
    path('systems/add/', SystemEditView.as_view(), name='system_add'),
    path('systems/<int:pk>/', SystemView.as_view(), name='system'),
    path('systems/<int:pk>/edit/', SystemEditView.as_view(), name='system_edit'),
    path('systems/<int:pk>/delete/', SystemDeleteView.as_view(), name='system_delete'),
    path('systems/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='system_changelog', kwargs={
        'model': System
    }),

    # Person Lists
    path('persons/', PersonListView.as_view(), name='person_list'),
    path('persons/add/', PersonEditView.as_view(), name='person_add'),
    path('persons/<int:pk>/', PersonView.as_view(), name='person'),
    path('persons/<int:pk>/edit/', PersonEditView.as_view(), name='person_edit'),
    path('persons/<int:pk>/delete/', PersonDeleteView.as_view(), name='person_delete'),
    path('persons/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='person_changelog', kwargs={
        'model': Person
    }),

    # Login Credentials
    path('login-credentials/', LoginCredentialsListView.as_view(), name='logincredentials_list'),
    path('login-credentials/add/', LoginCredentialsEditView.as_view(), name='logincredentials_add'),
    path('login-credentials/<int:pk>/', LoginCredentialsView.as_view(), name='logincredentials'),
    path('login-credentials/<int:pk>/edit/', LoginCredentialsEditView.as_view(), name='logincredentials_edit'),
    path('login-credentials/<int:pk>/delete/', LoginCredentialsDeleteView.as_view(), name='logincredentials_delete'),
    path('login-credentials/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='logincredentials_changelog',
         kwargs={
             'model': LoginCredentials
         }),

)
