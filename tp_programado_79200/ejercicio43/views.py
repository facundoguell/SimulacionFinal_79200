from django.shortcuts import render
from .forms import ParametersForm
from django.views import generic
import numpy as np
from . import clases
from ejercicio43 import soporte

def index(request):
    return render(request, 'index.html')


class simulacion(generic.FormView):
    form_class = ParametersForm
    template_name = 'ejercicio43.html'

    def form_valid(self, form):
        numeromesas = form.cleaned_data['mesas']
        media= form.cleaned_data['min_fin']
        desv= form.cleaned_data['min_inicio']
        fin= form.cleaned_data['cant_reloj']
        matriz = [[''] * 14 for f in range(1)]
        reloj = 0
        eventos = ["Inicialización", "Llegada Cliente", "Fin Atencion", "Fin Cobro", "Fin Estadia"]
        init = True
        llegada_cliente = False
        id_cliente = 0
        listaclientes = []
        proxima_llegada = 0
        evento = ''
        cantidad_clientes_atendidos = 0
        acu_tiempo_permanencia = 0
        prom_tiempo_permanencia = 0
        estado = ''
        idtemp_clie = -1

        # seteo de objetos permanentes
        cocinero1 = clases.Cocinero(1, "L")
        cocinero2 = clases.Cocinero(2, "L")
        caja = clases.Caja(1, "L", 0)
        mesas = clases.Mesas(numeromesas, "L")
        cocina = clases.Cocina(0, cocinero1, cocinero2)

        while reloj <= fin:

            if init:
                evento = eventos[0]
                proxima_llegada = round(reloj + soporte.generar_normal(media,desv),4)
                init = False

            # inicio de los clientes
            elif llegada_cliente:
                evento = eventos[1]
                proxima_llegada = round(reloj + soporte.generar_normal(media,desv),4)
                id_cliente += 1
                estado = soporte.generar_estadoinicial()
                tempcliente = clases.Cliente(id_cliente, estado, reloj, mesas, cocina, caja)
                listaclientes.append(tempcliente)
                matriz_trabajo = [[''] * 7 for f in range(len(matriz))]
                matriz = np.hstack((matriz, matriz_trabajo))
                for clientes in listaclientes:
                    clientes.ejecutar(reloj)

            else:
                for clientes in listaclientes:
                    clientes.ejecutar(reloj)

            # logica de guardado
            matriz[-1][0] = evento
            matriz[-1][1] = reloj
            matriz[-1][2] = proxima_llegada

            matriz[-1][3] = caja.estado
            matriz[-1][4] = caja.cola

            matriz[-1][5] = cocina.estado
            matriz[-1][6] = cocina.cola
            matriz[-1][7] = cocina.cocinero1.estado
            matriz[-1][8] = cocina.cocinero2.estado

            matriz[-1][9] = mesas.cantidad
            matriz[-1][10] = mesas.estado

            matriz[-1][11] = cantidad_clientes_atendidos
            matriz[-1][12] = acu_tiempo_permanencia
            matriz[-1][13] = prom_tiempo_permanencia

            if id_cliente > 0:
                for i in range(id_cliente):
                    matriz[-1][14 + (i * 7)] = listaclientes[i].numero
                    matriz[-1][15 + (i * 7)] = listaclientes[i].estado
                    matriz[-1][16 + (i * 7)] = listaclientes[i].tiempo_inicio
                    matriz[-1][17 + (i * 7)] = listaclientes[i].tiempo_fin_cobro
                    matriz[-1][18 + (i * 7)] = listaclientes[i].tiempo_fin_preparacion
                    matriz[-1][19 + (i * 7)] = listaclientes[i].cocinero
                    matriz[-1][20 + (i * 7)] = listaclientes[i].tiempo_fin_mesa


            vector_resultado = [''] * len(matriz[0])
            vector_resultado[0] = evento
            vector_resultado[1] = reloj
            vector_resultado[2] = proxima_llegada
            vector_resultado[3] = caja.estado
            vector_resultado[4] = caja.cola
            vector_resultado[5] = cocina.estado
            vector_resultado[6] = cocina.cola
            vector_resultado[7] = cocina.cocinero1.estado
            vector_resultado[8] = cocina.cocinero2.estado
            vector_resultado[9] = mesas.cantidad
            vector_resultado[10] = mesas.estado
            vector_resultado[11] = cantidad_clientes_atendidos
            vector_resultado[12] = acu_tiempo_permanencia
            vector_resultado[13] = prom_tiempo_permanencia
            for i in range(id_cliente):
                vector_resultado[14 + (i * 7)] = listaclientes[i].numero
                vector_resultado[15 + (i * 7)] = listaclientes[i].estado
                vector_resultado[16 + (i * 7)] = listaclientes[i].tiempo_inicio
                vector_resultado[17 + (i * 7)] = listaclientes[i].tiempo_fin_cobro
                vector_resultado[18 + (i * 7)] = listaclientes[i].tiempo_fin_preparacion
                vector_resultado[19 + (i * 7)] = listaclientes[i].cocinero
                vector_resultado[20 + (i * 7)] = listaclientes[i].tiempo_fin_mesa

            vector_temporal = [''] * len(matriz[0])
            matriz = np.vstack([matriz, vector_temporal])

            # logico proximo evento
            temporal_tiempo = proxima_llegada
            llegada_cliente = True
            evento = eventos[0]
            for clientes in listaclientes:
                if clientes.tiempo_fin_cobro != '':
                    if clientes.tiempo_fin_cobro < temporal_tiempo and clientes.estado == "SC":
                        llegada_cliente = False
                        temporal_tiempo = clientes.tiempo_fin_cobro
                        evento = eventos[3]
                if clientes.tiempo_fin_preparacion != '':
                    if clientes.tiempo_fin_preparacion < temporal_tiempo and clientes.estado == "SP":
                        llegada_cliente = False
                        evento = eventos[2]
                        temporal_tiempo = clientes.tiempo_fin_preparacion
                if clientes.tiempo_fin_mesa != '':
                    if clientes.tiempo_fin_mesa < temporal_tiempo and clientes.estado == "S":
                        llegada_cliente = False
                        temporal_tiempo = clientes.tiempo_fin_mesa
                        evento = eventos[4]
                        idtemp_clie = clientes.tiempo_inicio
            reloj = temporal_tiempo
            if evento == eventos[4]:
                cantidad_clientes_atendidos += 1
                acu_tiempo_permanencia += round((reloj - idtemp_clie),4)
                prom_tiempo_permanencia = round(acu_tiempo_permanencia / cantidad_clientes_atendidos, 4)
                idtemp_clie = -1



        return render(self.request, self.template_name, {"Cantidadpersonas": cantidad_clientes_atendidos, "Promediopermanencia": prom_tiempo_permanencia ,
                                                         "vectorResultado": vector_resultado, "clientes": listaclientes, "matrizResultado": matriz})






































































