# motor_calculo.py

def calcular_modelos(datos_circuito):
    """
    Corazón matemático del simulador.
    Recibe los datos de la UI y devuelve los cálculos de ambos modelos.

    Contrato de entrada (acordado con el equipo, ver ui_arquitectura.py):
        datos_circuito = {
            "Vcc":  float,  # Voltios
            "Rb":   float,  # Ohmios (resistencia de base)
            "Rc":   float,  # Ohmios (resistencia de colector)
            "Beta": float,  # Ganancia de corriente DC (hFE)
        }

    Nota: este modelo corresponde a un circuito de POLARIZACIÓN FIJA
    (Rb conectada directamente entre Vcc y la Base), no a un divisor
    de voltaje. Por eso no se usa Rth/Vth con R1/R2 — Rb actúa como la
    resistencia total vista desde la base.
    """

    # 1. Extraer datos del diccionario de entrada.
    # Usamos .get() para evitar errores si la UI omite algún valor.
    vcc  = datos_circuito.get("Vcc", 0.0)
    beta = datos_circuito.get("Beta", 0.0)
    rb   = datos_circuito.get("Rb", 1.0)   # Ohmios — resistencia de base
    rc   = datos_circuito.get("Rc", 0.0)   # Ohmios — resistencia de colector (= Rl)

    # 2. Función interna para calcular según el voltaje Base-Emisor (Vbe) asumido
    def calcular_estado(vbe_asumido):
        # Condición 1: Transistor en CORTE (Vcc no supera al Vbe asumido)
        if vcc <= vbe_asumido:
            return {
                "Vbe":    vbe_asumido,
                "Ib":     0.0,
                "Ic":     0.0,
                "Vce":    round(vcc, 4),
                "estado": "Corte"
            }

        # Condición 2: Transistor en región ACTIVA (polarización fija)
        # Ib = (Vcc - Vbe) / Rb
        ib = (vcc - vbe_asumido) / rb if rb > 0 else 0.0
        ic = beta * ib
        vce = vcc - (ic * rc)
        estado = "Activa"

        # Condición 3: Diagnóstico de SATURACIÓN
        # Si Vce cae por debajo de 0.2V, el transistor se satura
        vce_sat = 0.2
        if vce < vce_sat:
            vce = vce_sat
            ic = (vcc - vce_sat) / rc if rc > 0 else ic
            estado = "Saturación"

        # Formateamos el diccionario de salida exacto que pide el documento
        return {
            "Vbe":    vbe_asumido,
            "Ib":     round(ib, 6),   # Amperios (redondeado para microamperios)
            "Ic":     round(ic, 6),   # Amperios
            "Vce":    round(vce, 4),
            "estado": estado
        }

    # 3. Generar y retornar el diccionario de salida unificado
    resultados = {
        "ideal":         calcular_estado(vbe_asumido=0.0),  # Modelo Ideal: Vbe = 0V
        "segunda_aprox": calcular_estado(vbe_asumido=0.7),  # 2da Aprox: Vbe = 0.7V
    }

    return resultados


# Alias público — main.py invoca `calcular()` como nombre de contrato genérico.
calcular = calcular_modelos


# =====================================================================
# ZONA DE PRUEBAS (Puedes borrar esto luego, es solo para probar tu rol)
# =====================================================================
if __name__ == "__main__":
    # Simulamos el diccionario que te enviará el Arquitecto UI
    datos_prueba = {
        "Vcc":  9.0,       # 9 Voltios
        "Rb":   75_000.0,  # 75k Ohmios
        "Rc":   700.0,     # 700 Ohmios
        "Beta": 100.0,     # Ganancia
    }

    print("Calculando modelos...")
    resultados_finales = calcular_modelos(datos_prueba)

    import pprint
    pprint.pprint(resultados_finales)
