from ejercicio43 import soporte


class Cocina:
    def __init__(self, cola, cocinero1, cocinero2):
        self.cocinero1 = cocinero1
        self.cocinero2 = cocinero2
        self.cola = cola
        self.estado = "L"

    def asignar_cocinero(self):
        if self.cocinero1.estado == "L" and self.cocinero2.estado == "O":
            self.cocinero1.estado = "O"
            self.estado = "O"
            return 1
        elif self.cocinero1.estado == "O" and self.cocinero2.estado == "L":
            self.cocinero2.estado = "O"
            self.estado = "O"
            return 2
        else:
            self.cocinero1.estado = "O"
            return 1

    def liberar(self, cocinero):
        if self.cola > 0:
            self.cola -= 1
            self.estado = "L"
            if cocinero == 1:
                self.cocinero1.estado = "L"
            else:
                self.cocinero2.estado = "L"
        else:
            self.estado = "L"
            if cocinero == 1:
                self.cocinero1.estado = "L"
            else:
                self.cocinero2.estado = "L"


class Mesas:
    def __init__(self, cantidad, estado):
        self.cantidad = cantidad
        self.estado = estado

    def ocupar(self):
        self.cantidad -= 1
        if self.cantidad > 0:
            self.estado = "L"
        else:
            self.estado = "O"

    def liberar(self):
        self.cantidad += 1
        self.estado = "L"


class Cocinero:
    def __init__(self, id, estado):
        self.id = id
        self.estado = estado


class Caja:
    def __init__(self, id, estado, cola):
        self.id = id
        self.estado = estado
        self.cola = cola

    def liberar(self):
        if self.cola > 0:
            self.cola -= 1
            self.estado = "L"
        else:
            self.estado = "L"


class Cliente:

    def __init__(self, numero, estado, tiempo_inicio, mesas, cocina, caja):
        self.numero = numero
        self.estado = estado
        self.tiempo_fin_cobro = ''
        self.tiempo_inicio = tiempo_inicio
        self.tiempo_fin_preparacion = ''
        self.mesas = mesas
        self.tiempo_fin_mesa = ''
        self.banderap = False
        self.cocina = cocina
        self.caja = caja
        self.cocinero = ''
        self.primera_espera_cobro = False
        self.primera_espera_pedido = False



    def ejecutar(self, reloj):

        if self.banderap == True:  # cliente que esta de paso sig linea
            self.estado = "D"
            return
        if self.estado == "P":  # cliente que esta de paso
            self.banderap = True
            return
        if reloj == self.tiempo_fin_cobro:  # termino de pagar el ticket y pasa a esperar el pedido
            self.caja.liberar()
            self.estado = "EP"
        if reloj == self.tiempo_fin_preparacion:  # termino la preparacion y pasa a ver si se puede sentar
            self.cocina.liberar(self.cocinero)
            self.estado = "ES"
        if reloj == self.tiempo_fin_mesa:  # termino de usar la mesa y se va
            self.estado = "D"
            self.mesas.liberar()
        if self.estado == "ES" and self.mesas.estado == "O":  # cliente que va a sentarse y esta ocupado las mesas
            self.estado = "D"
        if self.estado == "ES" and self.mesas.estado != "O":  # cliente que va a sentarse y hay mesas disponibles
            self.estado = "S"
            self.tiempo_fin_mesa = round(reloj+soporte.generar_uniforme(),4)
            self.mesas.ocupar()
        if self.estado == "EC" and self.caja.estado == "L":  # cliente que esperaba cobro en caja pasa a siendo cobrado
            self.tiempo_fin_cobro = round(reloj + round((20 / 60),4),4) #reloj+1.25 ----descomentar para hacer mas rapido el cobro-------
            self.estado = "SC"
            self.caja.estado = "O"
            return
        if self.estado == "EC" and self.caja.estado == "O":  # cliente que esperaba en caja y esta ocupada sigue esperando
            if self.primera_espera_cobro == False:
                self.primera_espera_cobro = True
                self.caja.cola += 1
            return
        if self.estado == "EP" and self.cocina.estado == "L":  # cliente que esperaba atencion de preparacion del pedido y esta libre un cocinero
            self.tiempo_fin_preparacion = round(reloj + soporte.generar_exponencial(),4) #+10 -----descomentar para atascar la cocina-----------
            self.estado = "SP"
            self.cocinero = self.cocina.asignar_cocinero()
            return
        if self.estado == "EP" and self.cocina.estado == "O":  # cliente que esperaba atencion de preparacion del pedido y no hay cocineros libres
            if self.primera_espera_pedido == False:
                self.primera_espera_pedido = True
                self.cocina.cola += 1
            return
        else:
            return