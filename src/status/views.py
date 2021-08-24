from datetime import tzinfo
from django.shortcuts import render
from django.contrib.auth.models import User
from django.urls import (reverse_lazy, reverse)
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic.base import TemplateView, RedirectView, View
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView, FormView)
from panel_carga.views import ProyectoMixin
from django.contrib import messages
from django.utils import timezone
from panel_carga.choices import TYPES_REVISION, ESTADOS_CLIENTE
# from .filters import DocFilter
from panel_carga.models import Documento
from bandeja_es.models import Version, Paquete
from .filters import DocFilter

# Create your views here.

class StatusIndex(ProyectoMixin, TemplateView):
    template_name = 'status/index.html'
    
    def get_queryset(self):
        listado_versiones_doc = DocFilter(self.request.GET, queryset=Documento.objects.filter(proyecto=self.proyecto))
        return listado_versiones_doc.qs.order_by('Codigo_documento')

    def get_versiones_last(self):
        qs1 = self.get_queryset()
        qs2 = Version.objects.select_related('documento_fk').filter(documento_fk__in=qs1) #.select_related("owner").filter(owner__in=users)
        return qs2
    
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        documentos = self.get_queryset()

        context['Listado'] = self.tabla()
        context['filter'] = DocFilter(self.request.GET, queryset=documentos)
        return context

    def tabla(self):

        #Listar documentos
        lista_inicial = []
        lista_final = []
        semana_actual = timezone.now()
        documentos = self.get_queryset()
        version_documento = 0
        transmital = 0
        dias_revision = 0
        fecha_emision_b = 0
        versiones_documento = self.get_versiones_last()

        for doc in documentos:
            fecha_emision_b = doc.fecha_Emision_B
            comprobacion_first = 0
            version_first = 0
            version = 0
            for versiones in versiones_documento:
                if str(doc.Codigo_documento) == str(versiones.documento_fk) and comprobacion_first == 0:
                    version_first = versiones
                if str(doc.Codigo_documento) == str(versiones.documento_fk):
                    version = versiones

            if version:
                paquete = version.paquete_set.first()
                paquete_first = version_first.paquete_set.first()
                if version.estado_cliente == 5:
                    transmital = abs((paquete.fecha_creacion - paquete_first.fecha_creacion).days)
                    dias_revision = 0
                else:
                    transmital = abs((semana_actual - paquete_first.fecha_creacion).days)
                    fecha_version = paquete.fecha_creacion
                    dias_revision = abs((semana_actual - fecha_version).days)

                version_documento = version.revision

                for revision in TYPES_REVISION[1:4]:
                    if version_documento == revision[0]:
                        if dias_revision < 0:
                            dias_revision = 0
                            lista_inicial =[doc, [version, paquete, semana_actual, '70%', transmital, paquete_first.fecha_creacion, dias_revision]]
                            lista_final.append(lista_inicial)
                        else:
                            lista_inicial =[doc, [version, paquete, semana_actual, '70%', transmital, paquete_first.fecha_creacion, dias_revision]]
                            lista_final.append(lista_inicial)

                for revision in TYPES_REVISION[5:]:
                    if version_documento == revision[0]:
                        lista_inicial = [doc, [version, paquete, semana_actual, '100%', transmital, paquete_first.fecha_creacion, dias_revision]]
                        lista_final.append(lista_inicial)
                        
            else: 
                if semana_actual >= fecha_emision_b:
                    lista_inicial = [doc, ['no version','Atrasado']]
                    lista_final.append(lista_inicial)
                else:
                    lista_inicial = [doc, ['no version','Pendiente']]
                    lista_final.append(lista_inicial)
    
        return lista_final