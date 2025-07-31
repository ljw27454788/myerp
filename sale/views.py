import os

from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy

from sale.models import Sample
from factory.models import Client


# Create your views here.
class SampleListView(generic.ListView):
    model = Sample
    template_name = "samples.html"

    def get_queryset(self):
        show_all = self.request.GET.get("show_all")
        if show_all:
            return Sample.objects.all()
        return Sample.objects.filter(complete=False)

    def get_context_data(self, *args, **kwargs):
        context = super(SampleListView, self).get_context_data(*args, **kwargs)
        return context


class SampleCreateView(generic.CreateView):
    model = Sample
    fields = ["product", "client", "quantity", "note"]
    template_name = "samples_create.html"
    success_url = reverse_lazy("sale:samples")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # form.fields['client'].queryset = Client.objects.filter(user=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class SampleUpdateView(generic.UpdateView):
    model = Sample
    fields = ["product", "client", "quantity", "note"]
    template_name = "samples_update.html"
    success_url = reverse_lazy("sale:samples")


class SampleDeleteView(generic.DeleteView):
    model = Sample
    success_url = reverse_lazy("sale:samples")
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        print(self.object)
        if self.object.complete:
            return HttpResponseForbidden("禁止删除已完成的记录")
        return super().delete(request, *args, **kwargs)
