from django import forms
from clinicmodels.models import Vitals


class VitalsForm(forms.ModelForm):
    class Meta:
        model = Vitals
        fields = ['visit', 'height', 'weight', 'systolic', 'diastolic',
                  'temperature', 'hiv_positive', 'ptb_positive', 'hepc_positive',
                  'heart_rate']