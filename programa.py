"""
Programa del consultorio odontologico del doctor "XXX"
--------------------------------------------------------
Captura datos de clientes, calcula el valor de cada cita,
guarda todo en memoria, calcula totales, ordena por valor
de la atencion y permite buscar un cliente por cedula.
"""

# ---------------------------------------------------------------
# PARTE 1: TABLA DE PRECIOS
# ---------------------------------------------------------------

PRECIOS = {
    "Particular": {
        "cita": 80000,
        "atencion": {
            "Limpieza": 60000,
            "Calzas": 80000,
            "Extraccion": 100000,
            "Diagnostico": 50000,
        },
    },
    "EPS": {
        "cita": 5000,
        "atencion": {
            "Limpieza": 0,
            "Calzas": 40000,
            "Extraccion": 40000,
            "Diagnostico": 0,
        },
    },
    "Prepagada": {
        "cita": 30000,
        "atencion": {
            "Limpieza": 0,
            "Calzas": 10000,
            "Extraccion": 10000,
            "Diagnostico": 0,
        },
    },
}

# Listas de valores validos, las usamos mas adelante para
# validar lo que el usuario escribe por teclado.
TIPOS_CLIENTE = list(PRECIOS.keys())              # ["Particular", "EPS", "Prepagada"]
TIPOS_ATENCION = ["Limpieza", "Calzas", "Extraccion", "Diagnostico"]


DOCTORES = {
    "Doctor. Juan perez gonzales": ["Limpieza", "Diagnostico"],
    "Doctora. Maria lopez": ["Calzas", "Extraccion"],
    "Doctor. Carlos ruiz alzate": ["Limpieza", "Calzas", "Extraccion", "Diagnostico"],
}


def obtener_doctores_disponibles(tipo_atencion):
    """
    Recorre el diccionario DOCTORES y devuelve una lista con los
    nombres de los doctores que SI pueden hacer ese tipo de atencion.
    """
    disponibles = []
    for nombre_doctor, atenciones_que_hace in DOCTORES.items():
        if tipo_atencion in atenciones_que_hace:
            disponibles.append(nombre_doctor)
    return disponibles


# ---------------------------------------------------------------
# PARTE 2: CALCULAR EL VALOR DE UNA CITA
# ---------------------------------------------------------------
def calcular_valor(tipo_cliente, tipo_atencion, cantidad):
    """
    Recibe el tipo de cliente, el tipo de atencion y la cantidad,
    y devuelve el valor total a pagar.

    Regla del taller:
    valor_a_pagar = valor_de_la_cita + (valor_de_la_atencion * cantidad)
    """
    valor_cita = PRECIOS[tipo_cliente]["cita"]
    valor_atencion_unitario = PRECIOS[tipo_cliente]["atencion"][tipo_atencion]

    valor_total = valor_cita + (valor_atencion_unitario * cantidad)
    return valor_total


# ---------------------------------------------------------------
# PARTE 3: CAPTURAR LOS DATOS DE UN CLIENTE
# ---------------------------------------------------------------
def pedir_texto_valido(mensaje, opciones_validas):
    """
    Pide un texto por teclado y no deja continuar hasta que el
    usuario escriba una de las opciones validas (sin importar
    mayusculas/minusculas). Esto evita que el programa se caiga
    por un dato mal escrito.
    """
    while True:
        valor = input(mensaje).strip()          # strip() quita espacios de mas
        # Comparamos ignorando mayusculas/minusculas:
        for opcion in opciones_validas:
            if valor.lower() == opcion.lower():
                return opcion                     # devolvemos la version "oficial"
        print(f"  -> Dato invalido. Opciones validas: {', '.join(opciones_validas)}")


def pedir_cantidad(tipo_atencion):
    """
    Pide la cantidad de la atencion, aplicando la regla del taller:
    - Limpieza y Diagnostico: la cantidad siempre es 1.
    - Calzas y Extraccion: cualquier numero mayor que cero.
    """
    if tipo_atencion in ("Limpieza", "Diagnostico"):
        print("  (Para Limpieza/Diagnostico la cantidad siempre es 1)")
        return 1

    while True:
        texto = input("Cantidad (numero entero mayor que 0): ").strip()
        if texto.isdigit() and int(texto) > 0:
            return int(texto)
        print("  -> La cantidad debe ser un numero entero mayor que 0.")


def pedir_doctor(tipo_atencion):
    """
    Muestra solo los doctores que pueden hacer ese tipo de atencion
    (usando obtener_doctores_disponibles) y pide al usuario elegir
    uno de esa lista.
    """
    doctores_disponibles = obtener_doctores_disponibles(tipo_atencion)

    print(f"  Doctores disponibles para {tipo_atencion}:")
    for doctor in doctores_disponibles:
        print(f"    - {doctor}")

    return pedir_texto_valido("Elija el doctor: ", doctores_disponibles)


def pedir_cliente():
    """
    Pide todos los datos de UN cliente y devuelve un diccionario
    con esa informacion, incluyendo el valor ya calculado.
    """
    print("\n--- Datos del nuevo cliente ---")
    cedula = input("Cedula: ").strip()
    nombre = input("Nombre: ").strip()
    telefono = input("Telefono: ").strip()

    tipo_cliente = pedir_texto_valido(
        f"Tipo de cliente ({'/'.join(TIPOS_CLIENTE)}): ", TIPOS_CLIENTE
    )
    tipo_atencion = pedir_texto_valido(
        f"Tipo de atencion ({'/'.join(TIPOS_ATENCION)}): ", TIPOS_ATENCION
    )
    cantidad = pedir_cantidad(tipo_atencion)
    doctor = pedir_doctor(tipo_atencion)

    prioridad = pedir_texto_valido(
        "Prioridad de atencion (Normal/Urgente): ", ["Normal", "Urgente"]
    )
    fecha_cita = input("Fecha de la cita (dd/mm/aaaa): ").strip()

    valor_a_pagar = calcular_valor(tipo_cliente, tipo_atencion, cantidad)

    # Armamos el diccionario con todos los datos de este cliente:
    cliente = {
        "cedula": cedula,
        "nombre": nombre,
        "telefono": telefono,
        "tipo_cliente": tipo_cliente,
        "tipo_atencion": tipo_atencion,
        "cantidad": cantidad,
        "doctor": doctor,
        "prioridad": prioridad,
        "fecha_cita": fecha_cita,
        "valor_a_pagar": valor_a_pagar,
    }
    return cliente


# ---------------------------------------------------------------
# PARTE 4: CAPTURAR VARIOS CLIENTES (ARREGLO EN MEMORIA)
# ---------------------------------------------------------------
def capturar_clientes():
    """
    Pregunta cuantos clientes se van a registrar y va llamando a
    pedir_cliente() esa cantidad de veces. Todos los clientes se
    van guardando en una LISTA (nuestro "arreglo" en memoria).
    """
    while True:
        texto = input("\n¿Cuantos clientes va a registrar?: ").strip()
        if texto.isdigit() and int(texto) > 0:
            cantidad_clientes = int(texto)
            break
        print("  -> Escriba un numero entero mayor que 0.")

    clientes = []  # lista vacia: aqui se va a ir guardando cada cliente
    for i in range(cantidad_clientes):
        print(f"\n=== Cliente {i + 1} de {cantidad_clientes} ===")
        nuevo_cliente = pedir_cliente()
        clientes.append(nuevo_cliente)  # append agrega al final de la lista

    return clientes


# ---------------------------------------------------------------
# PARTE 5: CALCULAR TOTALES
# ---------------------------------------------------------------
def calcular_totales(clientes):
    """
    Recorre la lista de clientes y calcula:
    - total de clientes
    - ingresos totales recibidos
    - cuantos clientes van para extraccion de dientes
    """
    total_clientes = len(clientes)          # len() cuenta cuantos elementos tiene la lista

    ingresos_totales = 0
    total_extraccion = 0

    for cliente in clientes:                 # recorremos cada diccionario de la lista
        ingresos_totales += cliente["valor_a_pagar"]
        if cliente["tipo_atencion"] == "Extraccion":
            total_extraccion += 1

    return total_clientes, ingresos_totales, total_extraccion


# ---------------------------------------------------------------
# PARTE 6: ORDENAR POR VALOR DE ATENCION (MAYOR A MENOR)
# ---------------------------------------------------------------
def ordenar_por_valor_desc(clientes):
    """
    Ordena una copia de la lista de clientes de mayor a menor valor
    a pagar, usando el algoritmo de "burbuja" (bubble sort):

    La idea es ir comparando parejas de elementos vecinos y si estan
    en el orden incorrecto, los intercambiamos. Repetimos este
    barrido varias veces hasta que ya nadie se intercambia, momento
    en el que la lista queda ordenada.
    """
    lista_ordenada = clientes.copy()          
    n = len(lista_ordenada)

    for vuelta in range(n):
        hubo_intercambio = False
        for j in range(0, n - vuelta - 1):
            valor_actual = lista_ordenada[j]["valor_a_pagar"]
            valor_siguiente = lista_ordenada[j + 1]["valor_a_pagar"]
            if valor_actual < valor_siguiente:      # queremos de MAYOR a menor
                # Intercambiamos los dos elementos de posicion:
                lista_ordenada[j], lista_ordenada[j + 1] = lista_ordenada[j + 1], lista_ordenada[j]
                hubo_intercambio = True
        if not hubo_intercambio:
            break   # si en una vuelta completa no hubo cambios, ya esta ordenada

    return lista_ordenada


# ---------------------------------------------------------------
# PARTE 7: BUSCAR UN CLIENTE POR CEDULA
# ---------------------------------------------------------------
def buscar_por_cedula(lista_ordenada, cedula_buscada):
    """
    Recorre la lista ordenada por valor y busca un cliente cuya
    cedula coincida con la buscada. Como la lista esta ordenada
    por VALOR (no por cedula), la busqueda es secuencial: vamos
    mirando uno por uno hasta encontrarlo o llegar al final.
    """
    for cliente in lista_ordenada:
        if cliente["cedula"] == cedula_buscada:
            return cliente        
    return None                    


# ---------------------------------------------------------------
# FUNCIONES PARA MOSTRAR RESULTADOS EN PANTALLA
# ---------------------------------------------------------------
def mostrar_clientes(clientes, titulo):
    print(f"\n--- {titulo} ---")
    for cliente in clientes:
        print(
            f"  Cedula: {cliente['cedula']:<12} "
            f"Nombre: {cliente['nombre']:<20} "
            f"Atencion: {cliente['tipo_atencion']:<12} "
            f"Doctor: {cliente['doctor']:<20} "
            f"Valor: ${cliente['valor_a_pagar']:,}"
        )


def mostrar_totales(total_clientes, ingresos_totales, total_extraccion):
    print("\n--- Totales del consultorio ---")
    print(f"  Total de clientes atendidos: {total_clientes}")
    print(f"  Ingresos totales recibidos:  ${ingresos_totales:,}")
    print(f"  Clientes en extraccion:      {total_extraccion}")


# ---------------------------------------------------------------
# PARTE 9: PROGRAMA PRINCIPAL
# ---------------------------------------------------------------
def main():
    print("=== Sistema del consultorio odontologico ===")

    # 1) Capturar todos los clientes y guardarlos en la lista/arreglo
    clientes = capturar_clientes()
    mostrar_clientes(clientes, "Clientes registrados")

    # 2) Calcular y mostrar los totales
    total_clientes, ingresos_totales, total_extraccion = calcular_totales(clientes)
    mostrar_totales(total_clientes, ingresos_totales, total_extraccion)

    # 3) Ordenar por valor de atencion, de mayor a menor
    clientes_ordenados = ordenar_por_valor_desc(clientes)
    mostrar_clientes(clientes_ordenados, "Clientes ordenados por valor (mayor a menor)")

    # 4) Buscar un cliente especifico por cedula
    cedula_buscada = input("\nEscriba la cedula que quiere buscar: ").strip()
    resultado = buscar_por_cedula(clientes_ordenados, cedula_buscada)

    if resultado:
        print("\n--- Cliente encontrado ---")
        print(f"  Nombre: {resultado['nombre']}")
        print(f"  Telefono: {resultado['telefono']}")
        print(f"  Tipo de cliente: {resultado['tipo_cliente']}")
        print(f"  Tipo de atencion: {resultado['tipo_atencion']}")
        print(f"  Doctor: {resultado['doctor']}")
        print(f"  Fecha de la cita: {resultado['fecha_cita']}")
        print(f"  Valor a pagar: ${resultado['valor_a_pagar']:,}")
    else:
        print(f"\nNo se encontro ningun cliente con la cedula {cedula_buscada}.")


if __name__ == "__main__":
    main()