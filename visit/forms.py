from django import forms
from clinicmodels.models import Visit
from clinicmodels.models import Patient


class VisitForm(forms.ModelForm):

    class Meta:
        model = Visit
        fields = ['patient', 'status']
