from django.shortcuts import render
from django.contrib.auth.models import User
from django.urls import (reverse_lazy, reverse)
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic.base import TemplateView, RedirectView, View
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView, FormView)
from panel_carga.views import ProyectoMixin
from django.contrib import messages
from django.utils import timezone
from panel_carga.choices import TYPES_REVISION
# from .filters import DocFilter
from panel_carga.models import Documento
from bandeja_es.models import Version, Paquete
from .filters import DocFilter
from tools.objects import StaffViewMixin, SuperUserViewMixin, is_staff_check, is_superuser_check

# Create your views here.

class StatusIndex(ProyectoMixin, TemplateView):
    template_name = 'status/index.html'
    
    def get_queryset(self):
        listado_versiones_doc = DocFilter(self.request.GET, queryset=Documento.objects.filter(proyecto=self.proyecto))
        return listado_versiones_doc.qs.order_by('Codigo_documento')
    

    def get_context_data(self, **kwargs):
        #Listar documentos
        lista_inicial = []
        lista_final = []
        semana_actual = timezone.now()
        version_documento = 0
        transmital = 0
        context = super().get_context_data(**kwargs)
        documentos = self.get_queryset()
        for doc in documentos:
            version = Version.objects.filter(documento_fk=doc).last()
            version_first = Version.objects.filter(documento_fk=doc).first()
            if version:
                paquete = version.paquete_set.all()
                paquete_first = version_first.paquete_set.all()
                version_documento = version.revision
                transmital = paquete[0].fecha_creacion - paquete_first[0].fecha_creacion
                for revision in TYPES_REVISION[1:4]:
                    if version_documento == revision[0]:
                        lista_inicial =[doc, [version, paquete, semana_actual, '70%', transmital.days, paquete_first[0].fecha_creacion]]
                        lista_final.append(lista_inicial)

                for revision in TYPES_REVISION[5:]:
                    if version_documento == revision[0]:
                        lista_inicial = [doc, [version, paquete, semana_actual, '100%', transmital.days, paquete_first[0].fecha_creacion]]
                        lista_final.append(lista_inicial)
                #print('documento: ', doc, ' version: ', version, ' paquete:', paquete, ' listado final: ', lista_final)                
            else: 
                lista_inicial = [doc, []]
                lista_final.append(lista_inicial)
                
        context['Listado'] = lista_final
        context['filter'] = DocFilter(self.request.GET, queryset=documentos)
        return context