import os
import pandas as pd

from django.shortcuts import render
from django.conf import settings
from django.views import generic

from factory.models import Machine

# Create your views here.
class MachineListView(generic.ListView):
    model = Machine
    template_name = "machine_list.html"

    def get_queryset(self):
        return Machine.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(MachineListView, self).get_context_data(*args, **kwargs)
        return context
    
class MachineDetailView(generic.DetailView):
    model = Machine
    template_name = "machine_detail.html"

    def get_object(self, *args, **kwargs):
        obj = super(MachineDetailView, self).get_object(*args, **kwargs)
        return obj

    def get_context_data(self, **kwargs):
        context = super(MachineDetailView, self).get_context_data(**kwargs)
        file_path = os.path.join(settings.BASE_DIR, 'factory', 'data', self.object.name + '.xlsx')
        try:
            df = pd.read_excel(file_path, engine='openpyxl')
        except Exception as e:
            return context
        table_html = df.to_html(classes='table table-bordered', index=False)
        context['table_html'] = table_html
        return context