from django import forms
from django.forms import modelformset_factory
from sale.models import Sample

class SampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = ['product', 'client', 'quantity', 'lead_time', 'note']

# 一次创建多个样品（比如默认5条）
SampleFormSet = modelformset_factory(Sample, form=SampleForm, extra=5)