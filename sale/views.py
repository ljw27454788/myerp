import os

from django import forms
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import generic
from django.urls import reverse_lazy
from django.utils import timezone


from sale.models import Sample
from factory.models import Client


# Create your views here.
class SampleListView(generic.ListView):
    model = Sample
    template_name = "samples.html"

    def get_queryset(self):
        return Sample.objects.filter(complete=False)


class AllSampleListView(generic.ListView):
    model = Sample
    template_name = "all_samples.html"


class SampleCreateView(generic.CreateView):
    model = Sample
    fields = ["product", "client", "quantity", "lead_time", "note"]
    template_name = "samples_create.html"
    success_url = reverse_lazy("sale:samples")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # form.fields['client'].queryset = Client.objects.filter(user=self.request.user)
        form.fields["lead_time"].widget = forms.DateTimeInput(
            attrs={"type": "date"}, format="%Y-%m-%d"
        )
        return form

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class SampleUpdateView(generic.UpdateView):
    model = Sample
    fields = ["product", "client", "quantity", "lead_time", "note"]
    template_name = "samples_update.html"
    success_url = reverse_lazy("sale:samples")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["lead_time"].widget = forms.DateTimeInput(
            attrs={"type": "date"}, format="%Y-%m-%d"
        )
        return form

    def post(self, request, *args, **kwargs):
        send = self.request.POST.get("send")
        if send:
            self.object = self.get_object()
            self.object.complete = True
            self.object.send_at = timezone.now()
            self.object.save()
            return redirect(self.get_success_url())
        return super().post(request, *args, **kwargs)


class SampleDeleteView(generic.DeleteView):
    model = Sample
    success_url = reverse_lazy("sale:samples")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.complete:
            return HttpResponseForbidden("禁止删除已完成的记录")
        return super().delete(request, *args, **kwargs)
