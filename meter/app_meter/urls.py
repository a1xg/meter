from django.urls import path
from . import views
urlpatterns = [
    path('', views.ListMetersView.as_view(), name='list'),
    path('meter/<int:pk>', views.DetailMeterView.as_view(), name='detail'),
    path('meter/create/', views.CreateMeterView.as_view(), name='create'),
]