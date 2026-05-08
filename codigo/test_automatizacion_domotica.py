from automatizacion_domotica import ControlDomotico, DeviceBus, DISPOSITIVOS, Lecturas


def ejecutar(lecturas):
    bus = DeviceBus()
    ControlDomotico(bus).evaluar(lecturas)
    return bus.estado


def test_movimiento_enciende_luz_y_clima_alto():
    estado = ejecutar(Lecturas(30.5, True, False, False, False))
    assert estado[DISPOSITIVOS["luz"]] == "On"
    assert estado[DISPOSITIVOS["ventilador"]] == "High"
    assert estado[DISPOSITIVOS["termostato"]] == "Cooling"
    assert estado[DISPOSITIVOS["sirena"]] == "Off"
    assert estado[DISPOSITIVOS["puerta"]] == "Lock"


def test_ventana_abierta_apaga_ventilador_y_activa_alarma_si_ausente():
    estado = ejecutar(Lecturas(31.0, True, True, False, True))
    assert estado[DISPOSITIVOS["luz"]] == "On"
    assert estado[DISPOSITIVOS["ventilador"]] == "Off"
    assert estado[DISPOSITIVOS["termostato"]] == "Cooling"
    assert estado[DISPOSITIVOS["sirena"]] == "On"
    assert estado[DISPOSITIVOS["puerta"]] == "Lock"


def test_puerta_abierta_en_modo_ausente_activa_alarma_y_desbloquea():
    estado = ejecutar(Lecturas(22.0, False, False, True, True))
    assert estado[DISPOSITIVOS["luz"]] == "Off"
    assert estado[DISPOSITIVOS["ventilador"]] == "Off"
    assert estado[DISPOSITIVOS["termostato"]] == "Off"
    assert estado[DISPOSITIVOS["sirena"]] == "On"
    assert estado[DISPOSITIVOS["puerta"]] == "Unlock"


if __name__ == "__main__":
    pruebas = [
        test_movimiento_enciende_luz_y_clima_alto,
        test_ventana_abierta_apaga_ventilador_y_activa_alarma_si_ausente,
        test_puerta_abierta_en_modo_ausente_activa_alarma_y_desbloquea,
    ]
    for prueba in pruebas:
        prueba()
        print("OK - {}".format(prueba.__name__))
