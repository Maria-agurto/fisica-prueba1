# motor_calculo.py

def calcular_modelos(datos_circuito):
    """
    Corazón matemático del simulador. 
    Recibe los datos de la UI y devuelve los cálculos de ambos modelos.
    """
    
    # 1. Extraer datos del diccionario de entrada. 
    # Usamos .get() para evitar errores si la UI omite algún valor.
    vcc = datos_circuito.get("Vcc", 0.0)
    beta = datos_circuito.get("Beta", 0.0)
    
    # Resistencias (las convertimos a Ohmios internamente si es necesario, 
    # pero asumimos que la UI ya las manda en Ohmios)
    r1 = datos_circuito.get("R1", 1e9)  # Valor muy alto por defecto (circuito abierto)
    r2 = datos_circuito.get("R2", 1e9)
    rb = datos_circuito.get("Rb", 0.0)
    rl = datos_circuito.get("Rl", 0.0)  # Equivalente a Rc en el colector

    # 2. Calcular el Equivalente de Thévenin en la base (divisor de voltaje)
    # Vth = Vcc * (R2 / (R1 + R2))
    # Rth = (R1 * R2) / (R1 + R2)
    if r1 == 0:  # Prevención de división por cero si no hay R1
        vth = vcc
        rth = 0
    else:
        vth = vcc * (r2 / (r1 + r2))
        rth = (r1 * r2) / (r1 + r2)
    
    # Resistencia total conectada a la base
    rt_base = rth + rb

    # 3. Función interna para calcular según el voltaje Base-Emisor (Vbe) asumido
    def calcular_estado(vbe_asumido):
        # Condición 1: Transistor en CORTE (El voltaje no supera al Vbe)
        if vth <= vbe_asumido:
            return {
                "Vbe": 0.0 if vth <= 0 else round(vth, 4),
                "Ib": 0.0,
                "Ic": 0.0,
                "Vce": round(vcc, 4),
                "estado": "Corte"
            }
        
        # Condición 2: Transistor en región ACTIVA
        ib = (vth - vbe_asumido) / rt_base
        ic = beta * ib
        vce = vcc - (ic * rl)
        estado = "Activa"

        # Condición 3: Diagnóstico de SATURACIÓN
        # Si Vce cae por debajo de 0.2V, el transistor se satura
        vce_sat = 0.2 
        if vce < vce_sat:
            vce = vce_sat
            ic = (vcc - vce_sat) / rl if rl > 0 else ic
            estado = "Saturada"
        
        # Formateamos el diccionario de salida exacto que pide el documento
        return {
            "Vbe": vbe_asumido,
            "Ib": round(ib, 6),  # Redondeado a 6 decimales para Amperios (microamperios)
            "Ic": round(ic, 6),
            "Vce": round(vce, 4),
            "estado": estado
        }

    # 4. Generar y retornar el diccionario de salida unificado
    resultados = {
        "ideal": calcular_estado(vbe_asumido=0.0),      # Modelo Ideal: Vbe = 0V
        "segunda_aprox": calcular_estado(vbe_asumido=0.7) # 2da Aprox: Vbe = 0.7V
    }

    return resultados


# =====================================================================
# ZONA DE PRUEBAS (Puedes borrar esto luego, es solo para probar tu rol)
# =====================================================================
if __name__ == "__main__":
    # Simulamos el diccionario que te enviará el Arquitecto UI
    datos_prueba = {
        "Vcc": 9.0,     # 9 Voltios
        "R1": 10000.0,  # 10k Ohmios
        "R2": 2200.0,   # 2.2k Ohmios
        "Rb": 1000.0,   # 1k Ohmios
        "Rl": 100.0,    # 100 Ohmios
        "Beta": 100.0   # Ganancia
    }

    print("Calculando modelos...")
    resultados_finales = calcular_modelos(datos_prueba)
    
    import pprint
    pprint.pprint(resultados_finales)