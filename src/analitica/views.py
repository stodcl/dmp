from django.shortcuts import render
from django.urls import (reverse_lazy, reverse)
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import TemplateView, RedirectView, View
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView, FormView)
from panel_carga.views import ProyectoMixin
from bandeja_es.models import Version
from panel_carga.models import Documento
from panel_carga.choices import ESTADO_CONTRATISTA, ESTADOS_CLIENTE, TYPES_REVISION
from datetime import datetime, timedelta
from django.utils import timezone

# Create your views here.


class IndexAnalitica(ProyectoMixin, TemplateView):
    template_name =  'analitica/index.html'
    ###################################################
    #                                                 #
    #                                                 #
    #   PRIMER GRÁFICO DE ESTADOS DE LOS DOCUMENTOS   #
    #                                                 #
    #                                                 #
    ###################################################
    
    def reporte_general(self):

        lista_final = []
        lista_actual = []

        documentos = Documento.objects.filter(proyecto=self.request.session.get('proyecto'))

        #lista_final.append(lista_actual)

        #Obtener lista de las últimas versiones de cada documento
        for doc in documentos:
            versiones = Version.objects.filter(documento_fk=doc).last()
            lista_actual = [versiones, doc] 
            lista_final.append(lista_actual)

        #Obtener lista de cantidad de documentos por tipo de versión
        estados_documento = []
        estados_final = []

        for estado in TYPES_REVISION[1:]:
            cont = 0

            for lista in lista_final:

                try:
                    estado_documento = lista[0].revision
                    
                    if estado_documento == estado[0] :
                        cont = cont + 1
                
                except IndexError:
                    pass

                except AttributeError:
                    pass
            
            if cont != 0:
                estados_documentos = [cont, estado[1]]
                estados_final.append(estados_documentos)

        return estados_final

    ###################################################
    #                                                 #
    #                                                 #
    #   SEGUNDO GRÁFICO DE EMITIDOS POR SUBESTACION   #
    #                                                 #
    #                                                 #
    ###################################################

    def reporte_emisiones(self):
        
        lista_actual = []
        lista_final = []

        documentos = Documento.objects.filter(proyecto=self.request.session.get('proyecto'))

        especialidad_list = tuple()

        #Obtener versiones que no poseen un estado de revisión
        for doc in documentos:
            cont = 0
            versiones = Version.objects.filter(documento_fk=doc).last()

            for revision in TYPES_REVISION[1:]:
                
                try:
                    
                    #Comparar que la versión no posea ningón estado de revisión
                    if revision[0] == versiones.revision:
                        cont = 1

                except AttributeError:

                    pass
            
            #Almacena la versión que no posee estado de revisión
            if cont == 0:

                lista_actual = [versiones, doc] 
                lista_final.append(lista_actual)

        #Obtener lista de todas las especialidades
        for lista in lista_final: 
            for special in documentos:
                especialidad_actual = special.Especialidad
                if not especialidad_actual in especialidad_list:
                    especialidad_list = especialidad_list + (str(especialidad_actual),)

        #Obtener lista final de cantidad de versiones/documentos por especialidad pendientes
        aprobados_final = []
        aprobados_inicial = []

        for especialidad in especialidad_list:
            cont = 0 
            
            for lista in lista_final: 

                try:
                    mi_especialidad = lista[1].Especialidad

                    if mi_especialidad == especialidad:
                        cont = cont + 1

                except AttributeError:
                    pass

            aprobados_inicial = [cont, especialidad]
            aprobados_final.append(aprobados_inicial) 

        return aprobados_final      

        ###################################################
        #                                                 #
        #                                                 #
        #   TERCER GRÁFICO DE STATUS POR ESPECIALIDAD     #
        #                                                 #
        #                                                 #
        ###################################################

    def reporte_total_documentos_emitidos(self):
        
        lista_actual = []
        lista_final = []

        documentos = Documento.objects.filter(proyecto=self.request.session.get('proyecto'))

        especialidad_list = tuple()

        #Obtener lista de versiones que poseen un estado de revisión
        for doc in documentos:
            cont = 0
            versiones = Version.objects.filter(documento_fk=doc).last()

            for revision in TYPES_REVISION[1:]:
                
                try:

                    #Comparar versiones que si poseen un estado de revisión
                    if revision[0] == versiones.revision:
                        cont = 1

                except AttributeError:

                    pass
            
            #Almacena las versiones que poseen un estado de revisión
            if cont == 1:

                lista_actual = [versiones, doc] 
                lista_final.append(lista_actual)

        #Obtener lista de todas las especialidades
        for lista in lista_final: 
            for special in documentos:
                especialidad_actual = special.Especialidad
                if not especialidad_actual in especialidad_list:
                    especialidad_list = especialidad_list + (str(especialidad_actual),)

        #Obtener lista final de cantidad de versiones/documentos por especialidad emitidos
        aprobados_final = []
        aprobados_inicial = []

        for especialidad in especialidad_list:
            cont = 0 
            
            for lista in lista_final: 

                try:
                    mi_especialidad = lista[1].Especialidad

                    if mi_especialidad == especialidad:
                        cont = cont + 1

                except AttributeError:
                    pass

            aprobados_inicial = [cont, especialidad]
            aprobados_final.append(aprobados_inicial) 

        return aprobados_final

    def reporte_total_documentos(self):

        lista_actual = []
        lista_final = []

        documentos = Documento.objects.filter(proyecto=self.request.session.get('proyecto'))

        especialidad_list = tuple()

        #Obtener lista de todas las especialidades 
        for special in documentos:
            especialidad_actual = special.Especialidad
            if not especialidad_actual in especialidad_list:
                especialidad_list = especialidad_list + (str(especialidad_actual),)

        for especialidad in especialidad_list:
            cont = 0 
            
            for lista in documentos: 

                try:
                    mi_especialidad = lista.Especialidad

                    if mi_especialidad == especialidad:
                        cont = cont + 1

                except AttributeError:
                    pass

            lista_actual = [cont, especialidad]
            lista_final.append(lista_actual)
        
        return lista_final

        ###################################################
        #                                                 #
        #                                                 #
        #   CUARTO GRÁFICO DE CURVA S                     #
        #                                                 #
        #                                                 #
        ###################################################
    
    def reporte_curva_s_avance_esperado(self):
                
        lista_actual = []
        lista_final = []

        valor_ganado = Documento.objects.filter(proyecto=self.request.session.get('proyecto')).count()

        if valor_ganado !=0:

            valor_ganado = (100 / valor_ganado)
            documentos = Documento.objects.filter(proyecto=self.request.session.get('proyecto'))

            #Obtener la primera fecha de Emision en B y la última fecha en Emisión 0
            cont = 1
            fecha_final_b = 0
            fecha_final_0 = 0

            for lista in documentos:

                if cont == 1:
                    fecha_final_b = lista.fecha_Emision_B
                    fecha_final_0 = lista.fecha_Emision_0
                    cont = 0

                else:
                    fecha_actual_b = lista.fecha_Emision_B
                    fecha_actual_0 = lista.fecha_Emision_0

                    if abs((lista.fecha_Emision_B - fecha_final_b).days) <= 0:

                        fecha_final_b = lista.fecha_Emision_B

                    if abs((lista.fecha_Emision_0 - fecha_final_0).days) >= 0:

                        fecha_final_0 = lista.fecha_Emision_0

            #Se alamacena la primera fecha de Emisión en B en la Lista de Controles
            fechas_controles = []
            fechas_controles.append(fecha_final_b)
            fecha_actual = fecha_final_b
            
            #Se almacenan semana a semana hasta curbrir la última fecha de Emisión en 0
            while fecha_actual < fecha_final_0:
                
                fecha_actual = fecha_actual + timedelta(days=7)
                fechas_controles.append(fecha_actual)
            
            #Calculo del avance esperado por fecha de control
            avance_esperado = []
            lista_final_esperado = []

            for controles in fechas_controles:
                calculo_avanceEsperado = 0

                for doc in documentos:
                    
                    fecha_emision_b = doc.fecha_Emision_B
                    fecha_emision_0 = doc.fecha_Emision_0

                    #Se calcula el avance esperado mediante la comparación de la fecha de control y la fecha de emisión en B - 0
                    if fecha_emision_b <= controles and fecha_emision_0 > controles:
                        calculo_avanceEsperado = valor_ganado * 0.7 + calculo_avanceEsperado
                        
                    if fecha_emision_0 <= controles and fecha_emision_b < controles:
                        calculo_avanceEsperado = valor_ganado * 1 + calculo_avanceEsperado

                #Se almacena el avance esperado hasta la fecha de control
                avance_esperado = [format(calculo_avanceEsperado, '.2f')]
                lista_final_esperado.append(avance_esperado)

        else:

            avance_esperado = [valor_ganado]
            lista_final_esperado.append(avance_esperado)

        return lista_final_esperado

    def reporte_curva_s_avance_real(self):

        lista_actual = []
        lista_final = []
        valor_ganado = Documento.objects.filter(proyecto=self.request.session.get('proyecto')).count()

        if valor_ganado !=0:

            valor_ganado = (100 / valor_ganado)
            documentos = Documento.objects.filter(proyecto=self.request.session.get('proyecto'))

            #Obtener la primera fecha de Emision en B y la última fecha en Emisión 0
            cont = 1
            fecha_emision_b = 0
            fecha_emision_0 = 0

            for lista in documentos:

                if cont == 1:
                    fecha_final_b = lista.fecha_Emision_B
                    fecha_final_0 = lista.fecha_Emision_0
                    cont = 0

                else:
                    fecha_actual_b = lista.fecha_Emision_B
                    fecha_actual_0 = lista.fecha_Emision_0

                    if abs((lista.fecha_Emision_B - fecha_final_b).days) <= 0:

                        fecha_final_b = lista.fecha_Emision_B

                    if abs((lista.fecha_Emision_0 - fecha_final_0).days) >= 0:

                        fecha_final_0 = lista.fecha_Emision_0

            #Se alamacena la primera fecha de Emisión en B en la Lista de Controles
            fechas_controles = []
            fechas_controles.append(fecha_final_b)
            fecha_actual = fecha_final_b
            
            #Se almacenan semana a semana hasta curbrir la última fecha de Emisión en 0
            while fecha_actual < fecha_final_0:
                
                fecha_actual = fecha_actual + timedelta(days=7)
                fechas_controles.append(fecha_actual)
            
            #Calculo del avance real por fecha de control
            avance_real = []
            lista_final_real = []
            semana_actual = timezone.now()

            for controles in fechas_controles:
                calculo_avanceReal_0 = 0
                calculo_avanceReal_b = 0
                calculo_avanceReal = 0

                if semana_actual >= controles:

                    for doc in documentos:
                        try:   
                            fecha_emision_b = doc.fecha_Emision_B
                            fecha_emision_0 = doc.fecha_Emision_0
                            versiones = Version.objects.filter(documento_fk=doc).last()
                            revision_documento = versiones.revision

                            for revision in TYPES_REVISION[1:]:
                                
                                #Se verífica que el documento posea una revisión en Emisión B o en Emisión 0
                                if revision_documento == revision[0]:

                                    #Se calcula el avance esperado mediante la comparación de la fecha de control y la fecha de emisión en B - 0
                                    if fecha_emision_b <= controles:
                                        #print('entrando primera iteración')

                                        if revision[0] <= 4 and revision_documento == revision[0]:
                                            #print('entrando primeraaaaaa iteración') 

                                            calculo_avanceReal_0 = valor_ganado * 0.7 + calculo_avanceReal_0
                                            #print('calculando')
                                            #print(calculo_avanceReal)
                                    
                                    if fecha_emision_0 <= controles:
                                        #print('entrando segunda iteración') 

                                        if revision[0] > 4 and revision_documento == revision[0]:
                                            #print('entrando segundaaaaaaaaaa iteración') 
                                            calculo_avanceReal_b = valor_ganado * 1 + calculo_avanceReal_b
                                            #print('calculando')
                                            #print(calculo_avanceReal)

                            if calculo_avanceReal_0 > calculo_avanceReal_b:

                                calculo_avanceReal = calculo_avanceReal + calculo_avanceReal_0

                            if calculo_avanceReal_0 < calculo_avanceReal_b:

                                calculo_avanceReal = calculo_avanceReal + calculo_avanceReal_b
                        
                        except AttributeError:
                            pass

                    #Se almacena el avance esperado hasta la fecha de control
                    avance_real = [calculo_avanceReal]
                    lista_final_real.append(avance_real)
            #print(lista_final_real)

        else: 
                
               avance_real = []
               lista_final_real = []

               avance_real = [valor_ganado]
               lista_final_real.append(avance_real)

            
        return lista_final_real

    def reporte_curva_s_fechas(self):
        
        lista_actual = []
        lista_final = []
        valor_ganado = Documento.objects.filter(proyecto=self.request.session.get('proyecto')).count()
        
        if valor_ganado != 0:
        
            valor_ganado = (100 / valor_ganado)
            documentos = Documento.objects.filter(proyecto=self.request.session.get('proyecto'))
            
            #Obtener la primera fecha de Emision en B y la última fecha en Emisión 0
            cont = 1
            fecha_emision_b = 0
            fecha_emision_0 = 0

            for lista in documentos:

                if cont == 1:
                    fecha_final_b = lista.fecha_Emision_B
                    fecha_final_0 = lista.fecha_Emision_0
                    cont = 0

                else:
                    fecha_actual_b = lista.fecha_Emision_B
                    fecha_actual_0 = lista.fecha_Emision_0

                    if abs((lista.fecha_Emision_B - fecha_final_b).days) <= 0:

                        fecha_final_b = lista.fecha_Emision_B

                    if abs((lista.fecha_Emision_0 - fecha_final_0).days) >= 0:

                        fecha_final_0 = lista.fecha_Emision_0

            #Se alamacena la primera fecha de Emisión en B en la Lista de Controles
            fechas_controles = []
            fechas_controles.append(fecha_final_b)
            fecha_actual = fecha_final_b
            
            #Se almacenan semana a semana hasta curbrir la última fecha de Emisión en 0
            while fecha_actual < fecha_final_0:
                
                fecha_actual = fecha_actual + timedelta(days=7)
                fechas_controles.append(fecha_actual)

            #semana_actual = timezone.now()

        else:
                
            fechas_controles = []
            fechas_controles.append('Sin registros')


        return fechas_controles

        ###################################################
        #                                                 #
        #                                                 #
        #   OBTENER VALORES DE LOS EJES                   #
        #                                                 #
        #                                                 #
        ###################################################

    def valor_eje_x_grafico_uno(self):

        #Llamado para un método definido anteriormente
        lista_grafico_uno = self.reporte_general()
        lista_inicial = []
        lista_final = []
        espacios = 0
        maximo = 0
        cont = 0

        #Se obtiene el valor máximo del gráfico
        for lista in lista_grafico_uno:
            if cont == 0:
                maximo = lista[0]
                cont = 1
            
            else:
                if maximo < lista[0]:
                    maximo = lista[0]
        
        # #Se verífica que el maximo sea divisible por 10, para el caso de un maximo superior a 20
        # division_exacta = 0

        # if maximo > 20:  
            
        #     division_exacta = maximo % 10

        #     while division_exacta != 0:
        #         maximo = maximo + 1
        #         division_exacta = maximo % 10

        #Se busca la potencia de 10 que cubra al numero maximo, en caso de ser superior a 1 unidad
        resto = 9999999
        dividendo = 1
        cont = 0

        while resto > 1:
            if cont == 0:
                resto = maximo / dividendo
                cont = 1
            
            else:
                dividendo = dividendo * 10
                resto = maximo / dividendo

        # #Si el dividendo es distinto a 1, se secciona en 5 eslabones 
        # if dividendo != 1:
        #     espacios = dividendo/5
        #     lista_inicial = [dividendo,espacios]

        # #Si el dividendo es igual a 1, se establece como eslabones unitarios
        # else:
        #     lista_inicial = [dividendo, maximo]

        # lista_final.append(lista_inicial)

        #en caso de elegir la opcion de ajustar a numero divisible por 10, retornar maximo
        return dividendo

    def espacios_eje_x_grafico_uno(self):

        #Llamado para un método definido anteriormente
        dividendo = self.valor_eje_x_grafico_uno()
        espacios = 0

        # #Se secciona el eje en 10 partes iguales
        # if dividendo > 20:
        #     espacios = espacios / 10

        # else:
        #     espacio = 1

        #Si el dividendo es distinto a uno, se secciona 5 eslabones iguales
        if dividendo != 1:
                espacios = dividendo/5

        #Si el dividendo es igual a uno, se secciona en eslabones unitarios
        else:
            espacios = 1

        return int(espacios)

    def valor_eje_x_grafico_tres(self):

        #Llamado para un método definido anteriormente
        lista_grafico_tres = self.reporte_total_documentos()
        lista_inicial = []
        lista_final = []
        espacios = 0
        maximo = 0
        cont = 0

        for lista in lista_grafico_tres:
            if cont == 0:
                maximo = lista[0]
                cont = 1
            
            else:
                if maximo < lista[0]:
                    maximo = lista[0]

        resto = 9999999
        dividendo = 1
        cont = 0

        while resto > 1:
            if cont == 0:
                resto = maximo / dividendo
                cont = 1
            
            else:
                dividendo = dividendo * 10
                resto = maximo / dividendo

        if dividendo != 1:
            espacios = dividendo/5
            lista_inicial = [dividendo,espacios]

        else:
            lista_inicial = [dividendo, maximo]

        lista_final.append(lista_inicial)

        return dividendo

    def espacios_eje_x_grafico_tres(self):

        #Llamado para un método definido anteriormente
        dividendo = self.valor_eje_x_grafico_tres()
        espacios = 0

        if dividendo != 1:
                espacios = dividendo/5

        else:
            espacios = 1

        return int(espacios)
            


        ###################################################
        #                                                 #
        #                                                 #
        #   METODO PARA EXPLAYAR INFO                     #
        #                                                 #
        #                                                 #
        ###################################################

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['lista_final'] = self.reporte_general()
        context['lista_final_largo'] = len(self.reporte_general())
        context['lista_emisiones'] = self.reporte_emisiones()
        context['lista_total_documentos_emitidos'] = self.reporte_total_documentos_emitidos()
        context['lista_total_documentos'] = self.reporte_total_documentos()
        context['lista_curva_s_avance_real'] = self.reporte_curva_s_avance_real()
        context['lista_curva_s_avance_esperado'] = self.reporte_curva_s_avance_esperado()
        context['lista_curva_s_fechas'] = self.reporte_curva_s_fechas()
        context['tamano_grafico_uno'] = self.valor_eje_x_grafico_uno()
        context['espacios_grafico_uno'] = self.espacios_eje_x_grafico_uno()
        context['tamano_grafico_tres'] = self.valor_eje_x_grafico_tres()
        context['espacios_grafico_tres'] = self.espacios_eje_x_grafico_tres()

        return context