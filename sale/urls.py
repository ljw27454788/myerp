from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings

from factory import views

urlpatterns = [
    re_path(r'^samples$', views.MachineListView.as_view(), name='samples'),
]