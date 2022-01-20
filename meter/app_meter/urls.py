from django.urls import path
from . import views
urlpatterns = [
    path('', views.ListMetersView.as_view(), name='list'),
    path('meter/<int:pk>', views.DetailMeterView.as_view(), name='detail'),
    path('meter/<int:pk>/update', views.UpdateMeterView.as_view(), name='update'),
    path('meter/<int:pk>/delete', views.DeleteMeterView.as_view(), name='detail'),
    path('meter/<int:pk>/file-upload', views.ReadingsFileFormView.as_view(), name='file-upload'),
    path('meter/<int:pk>/readings-delete', views.ReadingsDeleteView.as_view(), name='readings-delete'),
    path('meter/create/', views.CreateMeterView.as_view(), name='create'),
]