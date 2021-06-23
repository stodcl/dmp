from django import forms
from django.contrib.auth import models
from django.forms import BaseFormSet, fields, widgets
from django.forms import (formset_factory, modelformset_factory)
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User

from .models import Tarea, Respuesta

from panel_carga.models import Documento


class TareaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user_list = []
        self.usuario = kwargs.pop('usuario')
        self.participantes = kwargs.pop('participantes')
        current_rol = self.usuario.perfil.rol_usuario
        #### recorre a todos los participantes e incluye en un listado solo el equipo de la empresa
        for user in self.participantes:
            rol = user.perfil.rol_usuario
            if current_rol >= 1 and current_rol <= 3:
                if rol == 2:
                    user_list.append(user.pk)
                elif rol == 3:
                    user_list.append(user.pk)
            elif current_rol <= 6 and current_rol >= 4:
                if rol == 5:
                    user_list.append(user.pk)
                elif rol == 6:
                    user_list.append(user.pk)

        qs = self.participantes.filter(pk__in=user_list)
        super(TareaForm, self).__init__(**kwargs)
        self.fields["encargado"] = forms.ModelChoiceField(queryset=qs)

    class Meta:
        model = Tarea
        exclude = ["estado"]
        widgets = {
            'plazo': forms.DateInput(attrs={'type':'date'}),
        }
class RespuestaForm(forms.ModelForm):
    class Meta:
        model = Respuesta
        exclude = ["tarea", "sent"]