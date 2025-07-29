from django.urls import path, re_path
from django.conf.urls.static import static

from sale import views

app_name = 'sale'

urlpatterns = [
    re_path(r'^samples$', views.SampleListView.as_view(), name='samples'),
    re_path(r'^samples-create$', views.SampleCreateView.as_view(), name='samples-create'),
    re_path(r'^samples-update/(?P<pk>[-\w]+)/edit$', views.SampleUpdateView.as_view(), name='samples-update'),
]