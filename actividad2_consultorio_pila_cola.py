"""
Actividad 2 - Consultorio odontologico del doctor "XXX"
--------------------------------------------------------
Los clientes se capturan UNA sola vez y con ellos se resuelven las dos
partes de la actividad:

PARTE A (PILA):  plan de contingencia para los clientes con extraccion
                 pendiente y prioridad Urgente.
                 - Solo entran los clientes de EXTRACCION con prioridad URGENTE.
                 - La pila queda en orden de fecha: la cita mas cercana en
                   el tope, que es la primera en llamarse.
                 - Se genera un informe de la pila (pantalla y archivo .txt).

PARTE B (COLA):  agenda diaria. Los clientes con cita en el dia se encolan
                 segun el orden de la agenda y se atienden en estricto
                 orden (el primero en entrar es el primero en atenderse).
                 Se genera el informe de la agenda (pantalla y archivo .txt).
"""

from datetime import datetime
from collections import deque

FORMATO_FECHA = "%d/%m/%Y"
ARCHIVO_INFORME = "informe_pila_extracciones.txt"
ARCHIVO_AGENDA = "agenda_del_dia.txt"


# ---------------------------------------------------------------
# TABLA DE PRECIOS (la misma de la actividad 1)
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

TIPOS_CLIENTE = list(PRECIOS.keys())
TIPOS_ATENCION = ["Limpieza", "Calzas", "Extraccion", "Diagnostico"]
PRIORIDADES = ["Normal", "Urgente"]


# ---------------------------------------------------------------
# ESTRUCTURA DE DATOS: PILA (LIFO)
# ---------------------------------------------------------------
class Pila:
    """
    Pila: el ultimo elemento que entra es el primero que sale (LIFO).
    Solo se puede agregar y sacar por un extremo: el TOPE.
    """

    def __init__(self):
        self._elementos = []

    def apilar(self, elemento):            
        self._elementos.append(elemento)

    def desapilar(self):                   
        if self.esta_vacia():
            return None
        return self._elementos.pop()

    def ver_tope(self):                   
        if self.esta_vacia():
            return None
        return self._elementos[-1]

    def esta_vacia(self):
        return len(self._elementos) == 0

    def tamano(self):
        return len(self._elementos)

    def elementos_desde_el_tope(self):
        """Copia de la pila leida desde el tope hasta el fondo (no la modifica)."""
        return list(reversed(self._elementos))


# ---------------------------------------------------------------
# ESTRUCTURA DE DATOS: COLA (FIFO)
# ---------------------------------------------------------------
class Cola:
    """
    Cola: el primer elemento que entra es el primero que sale (FIFO).
    Se agrega por el FINAL y se saca por el FRENTE.
    """

    def __init__(self):
        self._elementos = deque()

    def encolar(self, elemento):           
        self._elementos.append(elemento)

    def desencolar(self):                 
        if self.esta_vacia():
            return None
        return self._elementos.popleft()

    def ver_frente(self):                  
        if self.esta_vacia():
            return None
        return self._elementos[0]

    def esta_vacia(self):
        return len(self._elementos) == 0

    def tamano(self):
        return len(self._elementos)

    def elementos_desde_el_frente(self):
        """Copia de la cola leida desde el frente hasta el final (no la modifica)."""
        return list(self._elementos)


# ---------------------------------------------------------------
# CAPTURA DE CLIENTES
# ---------------------------------------------------------------
def calcular_valor(tipo_cliente, tipo_atencion, cantidad):
    """valor_a_pagar = valor_de_la_cita + (valor_de_la_atencion * cantidad)"""
    valor_cita = PRECIOS[tipo_cliente]["cita"]
    valor_atencion = PRECIOS[tipo_cliente]["atencion"][tipo_atencion]
    return valor_cita + (valor_atencion * cantidad)


def texto_fecha(fecha):
    return fecha.strftime(FORMATO_FECHA)


def pedir_texto_valido(mensaje, opciones_validas):
    while True:
        valor = input(mensaje).strip()
        for opcion in opciones_validas:
            if valor.lower() == opcion.lower():
                return opcion
        print(f"  -> Dato invalido. Opciones validas: {', '.join(opciones_validas)}")


def pedir_cantidad(tipo_atencion):
    """Limpieza y Diagnostico: siempre 1. Calzas y Extraccion: entero > 0."""
    if tipo_atencion in ("Limpieza", "Diagnostico"):
        print("  (Para Limpieza/Diagnostico la cantidad siempre es 1)")
        return 1
    while True:
        texto = input("Cantidad de piezas (numero entero mayor que 0): ").strip()
        if texto.isdigit() and int(texto) > 0:
            return int(texto)
        print("  -> La cantidad debe ser un numero entero mayor que 0.")


def pedir_fecha(mensaje):
    """Pide una fecha dd/mm/aaaa y la devuelve como objeto datetime (asi se puede ordenar)."""
    while True:
        texto = input(mensaje).strip()
        try:
            return datetime.strptime(texto, FORMATO_FECHA)
        except ValueError:
            print("  -> Fecha invalida. Use el formato dd/mm/aaaa (ejemplo: 15/10/2026).")


def armar_cliente(cedula, nombre, telefono, tipo_cliente, tipo_atencion,
                  cantidad, prioridad, fecha_cita):
    """Crea el diccionario de un cliente y le calcula el valor a pagar."""
    return {
        "cedula": cedula,
        "nombre": nombre,
        "telefono": telefono,
        "tipo_cliente": tipo_cliente,
        "tipo_atencion": tipo_atencion,
        "cantidad": cantidad,
        "prioridad": prioridad,
        "fecha_cita": fecha_cita,
        "valor_a_pagar": calcular_valor(tipo_cliente, tipo_atencion, cantidad),
    }


def pedir_cliente():
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
    prioridad = pedir_texto_valido(
        f"Prioridad de atencion ({'/'.join(PRIORIDADES)}): ", PRIORIDADES
    )
    fecha_cita = pedir_fecha("Fecha de la cita (dd/mm/aaaa): ")
    return armar_cliente(cedula, nombre, telefono, tipo_cliente, tipo_atencion,
                         cantidad, prioridad, fecha_cita)


def capturar_clientes():
    """Los clientes se guardan en la lista en el mismo orden en que se registran."""
    while True:
        texto = input("\n¿Cuantos clientes va a registrar?: ").strip()
        if texto.isdigit() and int(texto) > 0:
            cantidad_clientes = int(texto)
            break
        print("  -> Escriba un numero entero mayor que 0.")

    clientes = []
    for i in range(cantidad_clientes):
        print(f"\n=== Cliente {i + 1} de {cantidad_clientes} ===")
        clientes.append(pedir_cliente())
    return clientes


def cargar_datos_ejemplo():
    """Datos de prueba para no tener que digitar todo cada vez que se ejecuta."""
    # cedula, nombre, telefono, tipo_cliente, tipo_atencion, cantidad, prioridad, fecha
    datos = [
        ("1001", "Ana Gomez", "3101111111",
         "Particular", "Extraccion", 2, "Urgente", "15/10/2026"),
        ("1002", "Carlos Ruiz", "3102222222",
         "EPS", "Limpieza", 1, "Normal", "08/10/2026"),
        ("1003", "Luisa Perez", "3103333333",
         "Prepagada", "Extraccion", 1, "Urgente", "09/10/2026"),
        ("1004", "Jorge Mejia", "3104444444",
         "Particular", "Calzas", 3, "Urgente", "08/10/2026"),
        ("1005", "Marta Rios", "3105555555",
         "EPS", "Extraccion", 3, "Normal", "08/10/2026"),
        ("1006", "Pedro Salazar", "3106666666",
         "Particular", "Extraccion", 1, "Urgente", "12/10/2026"),
        ("1007", "Sofia Londono", "3107777777",
         "EPS", "Extraccion", 2, "Urgente", "08/10/2026"),
        ("1008", "Andres Castro", "3108888888",
         "Prepagada", "Diagnostico", 1, "Normal", "08/10/2026"),
        ("1009", "Valentina Ospina", "3109999999",
         "Particular", "Extraccion", 1, "Urgente", "20/10/2026"),
    ]

    clientes = []
    for fila in datos:
        fecha = datetime.strptime(fila[7], FORMATO_FECHA)
        clientes.append(armar_cliente(*fila[:7], fecha))
    return clientes


def obtener_clientes():
    while True:
        print("\n1. Capturar clientes por teclado")
        print("2. Cargar datos de ejemplo")
        opcion = input("Elija una opcion (1/2): ").strip()
        if opcion == "1":
            return capturar_clientes()
        if opcion == "2":
            clientes = cargar_datos_ejemplo()
            mostrar_clientes(clientes, "Clientes cargados")
            return clientes
        print("  -> Opcion invalida.")


def mostrar_clientes(clientes, titulo):
    print(f"\n--- {titulo} ---")
    for c in clientes:
        print(
            f"  Cedula: {c['cedula']:<8} "
            f"Nombre: {c['nombre']:<17} "
            f"Atencion: {c['tipo_atencion']:<12} "
            f"Prioridad: {c['prioridad']:<8} "
            f"Fecha: {texto_fecha(c['fecha_cita'])}"
        )


# ===============================================================
# PARTE A: PILA DE CONTINGENCIA (EXTRACCIONES URGENTES)
# ===============================================================
def ordenar_por_fecha(clientes):
    """
    Ordena una copia de la lista de la fecha MAS CERCANA a la MAS LEJANA
    con el algoritmo de burbuja. Solo intercambia cuando la fecha de la
    izquierda es estrictamente mayor, asi que si dos clientes tienen la
    misma fecha conservan su orden de registro.
    """
    lista = clientes.copy()
    n = len(lista)
    for vuelta in range(n):
        hubo_intercambio = False
        for j in range(0, n - vuelta - 1):
            if lista[j]["fecha_cita"] > lista[j + 1]["fecha_cita"]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                hubo_intercambio = True
        if not hubo_intercambio:
            break
    return lista


def construir_pila_contingencia(clientes):
    """
    1) Filtra: solo Extraccion y solo prioridad Urgente.
    2) Ordena por fecha, de la mas cercana a la mas lejana.
    3) Apila recorriendo la lista al reves: como en una pila sale primero
       lo ultimo que entro, la cita MAS CERCANA debe entrar de ULTIMA para
       quedar en el tope y ser la primera en llamarse.
    """
    candidatos = []
    for c in clientes:
        if c["tipo_atencion"] == "Extraccion" and c["prioridad"] == "Urgente":
            candidatos.append(c)

    ordenados = ordenar_por_fecha(candidatos)

    pila = Pila()
    for c in reversed(ordenados):
        pila.apilar(c)
    return pila


def generar_informe_pila(pila):
    """Arma el informe de la pila (de tope a fondo) y lo devuelve como lista de lineas."""
    ancho = 82
    lineas = []
    lineas.append("=" * ancho)
    lineas.append('INFORME DE LA PILA DE CONTINGENCIA - EXTRACCIONES URGENTES')
    lineas.append('Consultorio odontologico del doctor "XXX"')
    lineas.append(f"Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    lineas.append(f"Total de clientes en la pila: {pila.tamano()}")
    lineas.append("=" * ancho)
    lineas.append(
        f"{'#':<4}{'Cedula':<12}{'Nombre':<22}{'Telefono':<12}"
        f"{'Fecha cita':<12}{'Piezas':<8}{'Tipo cliente':<12}"
    )
    lineas.append("-" * ancho)

    for orden, c in enumerate(pila.elementos_desde_el_tope(), start=1):
        lineas.append(
            f"{orden:<4}{c['cedula']:<12}{c['nombre']:<22}{c['telefono']:<12}"
            f"{texto_fecha(c['fecha_cita']):<12}{c['cantidad']:<8}{c['tipo_cliente']:<12}"
        )

    lineas.append("-" * ancho)
    lineas.append("El cliente #1 esta en el TOPE de la pila: es el primero que se debe llamar.")
    return lineas


def guardar_informe(lineas, nombre_archivo):
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write("\n".join(lineas) + "\n")


def llamar_clientes_de_la_pila(pila):
    """Saca clientes del tope (desapilar) a medida que la clinica los va llamando."""
    print("\n--- Llamado de clientes (se atiende desde el tope de la pila) ---")
    while not pila.esta_vacia():
        siguiente = pila.ver_tope()
        print(f"\nSiguiente a llamar: {siguiente['nombre']} - Tel: {siguiente['telefono']} "
              f"- Cita: {texto_fecha(siguiente['fecha_cita'])}")
        respuesta = input("¿Llamar a este cliente y sacarlo de la pila? (s/n): ").strip().lower()
        if respuesta != "s":
            print(f"  -> Llamados suspendidos. Quedan {pila.tamano()} cliente(s) en la pila.")
            return
        llamado = pila.desapilar()
        print(f"  Llamando a {llamado['nombre']}... Quedan {pila.tamano()} en la pila.")
    print("\nLa pila quedo vacia: ya se llamo a todos los clientes urgentes.")


def plan_de_contingencia(clientes):
    print("\n" + "=" * 60)
    print("PARTE A: PILA DE CONTINGENCIA (EXTRACCIONES URGENTES)")
    print("=" * 60)

    pila = construir_pila_contingencia(clientes)
    if pila.esta_vacia():
        print("\nNo hay clientes de extraccion con prioridad Urgente. La pila esta vacia.")
        return

    lineas = generar_informe_pila(pila)
    print()
    for linea in lineas:
        print(linea)
    guardar_informe(lineas, ARCHIVO_INFORME)
    print(f"\n(Informe guardado en el archivo: {ARCHIVO_INFORME})")

    llamar_clientes_de_la_pila(pila)


# ===============================================================
# PARTE B: AGENDA DEL DIA Y COLA DE ATENCION
# ===============================================================
def generar_agenda_del_dia(clientes, fecha_dia):
    """
    La agenda del dia son los clientes cuya cita cae en esa fecha. Se
    recorren en el orden en que quedaron registrados en la agenda y se
    encolan: el primero en entrar a la cola sera el primero en atenderse.
    """
    agenda = Cola()
    for c in clientes:
        if c["fecha_cita"].date() == fecha_dia.date():
            agenda.encolar(c)
    return agenda


def generar_informe_agenda(agenda, fecha_dia):
    """Arma el informe de la agenda (del frente al final de la cola) como lista de lineas."""
    ancho = 78
    lineas = []
    lineas.append("=" * ancho)
    lineas.append('AGENDA DEL DIA - CONSULTORIO ODONTOLOGICO DEL DOCTOR "XXX"')
    lineas.append(f"Fecha: {texto_fecha(fecha_dia)}")
    lineas.append(f"Total de clientes agendados: {agenda.tamano()}")
    lineas.append("=" * ancho)
    lineas.append(
        f"{'Turno':<7}{'Cedula':<10}{'Nombre':<20}{'Atencion':<14}"
        f"{'Prioridad':<11}{'Valor a pagar':<14}"
    )
    lineas.append("-" * ancho)

    for turno, c in enumerate(agenda.elementos_desde_el_frente(), start=1):
        valor = f"${c['valor_a_pagar']:,}"
        lineas.append(
            f"{turno:<7}{c['cedula']:<10}{c['nombre']:<20}{c['tipo_atencion']:<14}"
            f"{c['prioridad']:<11}{valor:<14}"
        )

    lineas.append("-" * ancho)
    lineas.append("El turno 1 esta en el FRENTE de la cola: es el primero que se atiende.")
    return lineas


def atender_agenda(agenda):
    """Atiende la agenda sacando siempre al cliente del FRENTE de la cola."""
    print("\n--- Atencion de la agenda del dia ---")
    atendidos = 0
    ingresos_dia = 0
    mensaje = "Presione Enter para atenderlo (o escriba 's' para suspender): "

    while not agenda.esta_vacia():
        siguiente = agenda.ver_frente()
        print(f"\nTurno actual: {siguiente['nombre']} (Cedula {siguiente['cedula']}) "
              f"- {siguiente['tipo_atencion']}")
        print(f"  Clientes en la cola: {agenda.tamano()}")
        respuesta = input(mensaje).strip().lower()
        if respuesta == "s":
            print(f"  -> Atencion suspendida. Quedan {agenda.tamano()} cliente(s) sin atender.")
            break

        cliente = agenda.desencolar()
        atendidos += 1
        ingresos_dia += cliente["valor_a_pagar"]
        print(f"  Atendido: {cliente['nombre']}. Valor cobrado: ${cliente['valor_a_pagar']:,}")

    print("\n--- Resumen del dia ---")
    print(f"  Clientes atendidos: {atendidos}")
    print(f"  Ingresos del dia:   ${ingresos_dia:,}")


def atender_agenda_del_dia(clientes):
    print("\n" + "=" * 60)
    print("PARTE B: COLA DE ATENCION (AGENDA DEL DIA)")
    print("=" * 60)

    fecha_dia = pedir_fecha("\nFecha del dia a atender (dd/mm/aaaa): ")
    agenda = generar_agenda_del_dia(clientes, fecha_dia)

    if agenda.esta_vacia():
        print(f"\nNo hay clientes agendados para el {texto_fecha(fecha_dia)}.")
        return

    lineas = generar_informe_agenda(agenda, fecha_dia)
    print()
    for linea in lineas:
        print(linea)
    guardar_informe(lineas, ARCHIVO_AGENDA)
    print(f"\n(Agenda guardada en el archivo: {ARCHIVO_AGENDA})")

    atender_agenda(agenda)


# ---------------------------------------------------------------
# PROGRAMA PRINCIPAL
# ---------------------------------------------------------------
def main():
    print('=== Consultorio odontologico del doctor "XXX": contingencia y agenda ===')

    # Los clientes se capturan una sola vez y se usan en las dos partes
    clientes = obtener_clientes()

    plan_de_contingencia(clientes)        # PARTE A: Pila de extracciones urgentes
    atender_agenda_del_dia(clientes)      # PARTE B: Cola de la agenda del dia

    print("\nFin del programa.")


if __name__ == "__main__":
    main()
