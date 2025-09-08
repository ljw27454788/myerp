from django.urls import path, re_path
from django.conf.urls.static import static

from sale import views

app_name = 'sale'

urlpatterns = [
    re_path(r'^samples$', views.SampleListView.as_view(), name='samples'),
    re_path(r'^all-samples$', views.AllSampleListView.as_view(), name='all-samples'),
    re_path(r'^samples-create$', views.samples_create, name='samples-create'),
    re_path(r'^samples-update/(?P<pk>[-\w]+)/edit$', views.SampleUpdateView.as_view(), name='samples-update'),
    re_path(r'^samples-update/(?P<pk>[-\w]+)/delete$', views.SampleDeleteView.as_view(), name='samples-delete'),
    
    path("product-autocomplete/", views.ProductAutocomplete.as_view(), name="product-autocomplete"),
]