from django.urls import path
from . import views
urlpatterns = [
    path('', views.list_view, name='list'),
    path('meter/<int:pk>', views.detail_view, name='detail'),
    path('meter/create/', views.create_meter_view, name='create'),
]