from django.urls import path
from . import views
urlpatterns = [
    path('', views.listView, name='list'),
    path('detail/', views.detailView, name='detail'),
    path('create/', views.createView, name='create'),
]