from django.urls import path
from . import views
urlpatterns = [
    path('', views.list_view, name='list'),
    path('detail/', views.detail_view, name='detail'),
    path('create/', views.create_view, name='create'),
]