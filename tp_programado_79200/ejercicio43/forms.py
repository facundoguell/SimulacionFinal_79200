from django import forms
from crispy_forms.helper import FormHelper

class ParametersForm(forms.Form):

    mesas = forms.IntegerField(label='Cantidad de mesas disponibles', initial=10, min_value=1)
    min_fin = forms.IntegerField(label='Llegada Exponencial-Media', initial=10, min_value=1)
    min_inicio = forms.IntegerField(label='Llegada Exponencial-Desviacion', initial=6, min_value=1)
    cant_reloj= forms.IntegerField(label='Cantidad de minutos a simular', initial=120, min_value=1)


    def __init__(self, *args, **kwargs):
        super(ParametersForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_show_labels = False
        self.helper.form_tag = False