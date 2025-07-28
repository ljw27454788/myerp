import os

from django.shortcuts import render
from django.views import generic

from sale.models import Sample

# Create your views here.
class SampleListView(generic.ListView):
    model = Sample
    template_name = "samples.html"

    def get_queryset(self):
        return Sample.objects.filter(complete==False)

    def get_context_data(self, *args, **kwargs):
        context = super(SampleListView, self).get_context_data(*args, **kwargs)
        return context