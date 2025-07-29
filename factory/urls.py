from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings

from factory import views

app_name = 'factory'

urlpatterns = [
    re_path(r'^machines/(?P<pk>[-\w]+)$', views.MachineDetailView.as_view(), name='machines-detail'),
    re_path(r'^machines$', views.MachineListView.as_view(), name='machines'),
]