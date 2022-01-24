from django.urls import path
from . import views

urlpatterns = [
    path(
        '',
        views.MeterListView.as_view(),
        name='list'
    ),
    path(
        'meter/<int:pk>',
        views.MeterDetailView.as_view(),
        name='detail'
    ),
    path(
        'meter/<int:pk>/update',
        views.MeterUpdateView.as_view(),
        name='update'
    ),
    path(
        'meter/<int:pk>/delete',
        views.MeterDeleteView.as_view(),
        name='detail'
    ),
    path(
        'meter/<int:pk>/file-upload',
        views.ReadingsFileFormView.as_view(),
        name='file-upload'
    ),
    path(
        'meter/<int:pk>/readings-delete',
        views.ReadingsDeleteView.as_view(),
        name='readings-delete'
    ),
    path(
        'meter/create/',
        views.MeterCreateView.as_view(),
        name='create'
    ),
    path(
        'meter/create/unit-create/',
        views.UnitCreateView.as_view(),
        name='unit-create'
    ),
    path(
        'meter/create/resource-create/',
        views.ResourceCreateView.as_view(),
        name='resource-create'
    ),

]