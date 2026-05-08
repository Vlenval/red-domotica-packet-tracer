"""
Controlador Python para la red domotica simulada en Cisco Packet Tracer.

El mismo flujo puede copiarse al Editor Python3 del Smartphone0. Packet Tracer
no expone una API publica estable para controlar todos los Things desde codigo,
por eso DeviceBus actua como capa de salida verificable: registra exactamente
que accion debe aplicar cada regla automatica sobre los dispositivos IoT.
"""


TEMPERATURA_COOLING_C = 24.0
TEMPERATURA_ALTA_C = 28.0
TEMPERATURA_CONFORT_C = 23.0


DISPOSITIVOS = {
    "luz": "IoT0 Light",
    "sirena": "IoT4 Siren",
    "ventilador": "IoT6 Ceiling Fan",
    "termostato": "IoT7 Thermostat",
    "puerta": "door1 Door",
}


class Lecturas:
    def __init__(self, temperatura_c, movimiento, ventana_abierta, puerta_abierta, modo_ausente):
        self.temperatura_c = temperatura_c
        self.movimiento = movimiento
        self.ventana_abierta = ventana_abierta
        self.puerta_abierta = puerta_abierta
        self.modo_ausente = modo_ausente


class DeviceBus:
    """Salida de control reemplazable por llamadas IoT reales si el entorno las expone."""

    def __init__(self):
        self.estado = {}
        self.eventos = []

    def iniciar_ciclo(self, lecturas):
        self.eventos = [
            "Lecturas: temp={:.1f}C movimiento={} ventana={} puerta={} ausente={}".format(
                lecturas.temperatura_c,
                lecturas.movimiento,
                lecturas.ventana_abierta,
                lecturas.puerta_abierta,
                lecturas.modo_ausente,
            )
        ]

    def set_estado(self, regla, dispositivo, estado):
        self.estado[dispositivo] = estado
        self.eventos.append("{} -> {} = {}".format(regla, dispositivo, estado))


class ControlDomotico:
    def __init__(self, bus):
        self.bus = bus

    def evaluar(self, lecturas):
        self.bus.iniciar_ciclo(lecturas)
        self._control_luz(lecturas)
        self._control_clima(lecturas)
        self._control_seguridad(lecturas)
        self._control_puerta(lecturas)
        return list(self.bus.eventos)

    def _control_luz(self, lecturas):
        estado = "On" if lecturas.movimiento else "Off"
        self.bus.set_estado("Movimiento controla iluminacion", DISPOSITIVOS["luz"], estado)

    def _control_clima(self, lecturas):
        if lecturas.temperatura_c >= TEMPERATURA_ALTA_C and not lecturas.ventana_abierta:
            fan_estado = "High"
        else:
            fan_estado = "Off"
        self.bus.set_estado("Temperatura/ventana controla ventilacion", DISPOSITIVOS["ventilador"], fan_estado)

        if lecturas.temperatura_c > TEMPERATURA_COOLING_C:
            thermostat_estado = "Cooling"
        else:
            thermostat_estado = "Off"
        self.bus.set_estado("Temperatura controla climatizacion", DISPOSITIVOS["termostato"], thermostat_estado)

    def _control_seguridad(self, lecturas):
        intrusion = lecturas.movimiento or lecturas.ventana_abierta or lecturas.puerta_abierta
        estado = "On" if lecturas.modo_ausente and intrusion else "Off"
        self.bus.set_estado("Modo ausente controla alarma", DISPOSITIVOS["sirena"], estado)

    def _control_puerta(self, lecturas):
        estado = "Unlock" if lecturas.puerta_abierta else "Lock"
        self.bus.set_estado("Estado de puerta principal replica cerradura", DISPOSITIVOS["puerta"], estado)


def demo():
    escenarios = [
        Lecturas(30.5, True, False, False, False),
        Lecturas(31.0, True, True, False, True),
        Lecturas(22.0, False, False, True, True),
    ]

    controlador = ControlDomotico(DeviceBus())
    for numero, escenario in enumerate(escenarios, start=1):
        print("Ciclo automatico {}".format(numero))
        for evento in controlador.evaluar(escenario):
            print("  - {}".format(evento))


if __name__ == "__main__":
    demo()
