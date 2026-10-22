import csv
import os
from datetime import datetime

# ============================================
# MESA DE PARTES DIGITAL - GORE CAJAMARCA
# FUNDAMENTOS DE PROGRAMACIÓN
# ============================================

ARCHIVO = "expedientes.csv"
MAX_EXPEDIENTES = 100

CAMPOS = [
    "codigo", "dni", "nombre", "asunto",
    "area", "folios", "fecha"
]

# Arreglos paralelos
codigos = []
dnis = []
nombres = []
asuntos = []
areas = []
folios = []
fechas = []

# ============================================
# GUARDAR DATOS EN CSV
# ============================================
def guardar_datos():
    try:
        with open(ARCHIVO, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(CAMPOS)
            for i in range(len(codigos)):
                escritor.writerow([
                    codigos[i],
                    dnis[i],
                    nombres[i],
                    asuntos[i],
                    areas[i],
                    folios[i],
                    fechas[i]
                ])

        print("Datos guardados correctamente.")
    except OSError as error:
        print("Error al guardar:", error)

# ============================================
# CARGAR DATOS DESDE CSV
# ============================================
def cargar_datos():
    if not os.path.exists(ARCHIVO):
        return

    try:
        with open(ARCHIVO, "r", encoding="utf-8", newline="") as archivo:
            lector = csv.DictReader(archivo)
            if not lector.fieldnames or not all(
                campo in lector.fieldnames for campo in CAMPOS
            ):
                print("El archivo CSV tiene un formato incorrecto.")
                return
            registros = list(lector)
            if len(registros) > MAX_EXPEDIENTES:
                print("El archivo supera la capacidad permitida.")
                return
            # Validar antes de incorporar registros
            for fila in registros:
                if not fila["folios"].isdigit():
                    print("Archivo CSV con folios inválidos.")
                    return
            for fila in registros:
                codigos.append(fila["codigo"])
                dnis.append(fila["dni"])
                nombres.append(fila["nombre"])
                asuntos.append(fila["asunto"])
                areas.append(fila["area"])
                folios.append(int(fila["folios"]))
                fechas.append(fila["fecha"])
        print("Expedientes cargados correctamente.")
    except (OSError, UnicodeError, csv.Error) as error:
        print("Error al cargar datos:", error)
# ============================================
# VALIDAR DNI O RUC
# ============================================
def validar_documento(documento):
    return (
        len(documento) in (8, 11)
        and documento.isascii()
        and documento.isdigit()
    )
# ============================================
# GENERAR CÓDIGO CORRELATIVO
# ============================================
def generar_codigo():
    anio = datetime.now().year
    mayor = 0
    for codigo in codigos:
        partes = codigo.split("-")
        if len(partes) == 3:
            if partes[1] == str(anio) and partes[2].isdigit():
                mayor = max(mayor, int(partes[2]))
    return f"EXP-{anio}-{mayor + 1:04d}"
# ============================================
# REGISTRAR EXPEDIENTE
# ============================================
def registrar_expediente():
    print("\n========== REGISTRAR EXPEDIENTE ==========")
    if len(codigos) >= MAX_EXPEDIENTES:
        print("Se alcanzó el máximo de 100 expedientes.")
        return
    while True:
        dni = input("Ingrese DNI (8) o RUC (11): ").strip()
        if validar_documento(dni):
            break
        print("ERROR: Ingrese 8 u 11 dígitos numéricos.")
    while True:
        nombre = input("Nombres y apellidos / Razón social: ").strip()
        if nombre:
            nombre = nombre.upper()
            break
        print("ERROR: El nombre no puede estar vacío.")
    while True:
        asunto = input("Asunto del trámite: ").strip()
        if asunto:
            break
        print("ERROR: El asunto no puede estar vacío.")
    while True:
        area = input("Área de destino: ").strip()
        if area:
            area = area.upper()
            break
        print("ERROR: El área no puede estar vacía.")
    while True:
        entrada = input("Número de folios: ").strip()
        if entrada.isascii() and entrada.isdigit() and int(entrada) > 0:
            cantidad = int(entrada)
            break
        print("ERROR: Los folios deben ser mayores a cero.")
    codigo = generar_codigo()
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    codigos.append(codigo)
    dnis.append(dni)
    nombres.append(nombre)
    asuntos.append(asunto)
    areas.append(area)
    folios.append(cantidad)
    fechas.append(fecha)

    guardar_datos()
    print("\n======================================")
    print("      REGISTRO REALIZADO")
    print("======================================")
    print("Código:", codigo)
    print("Remitente:", nombre)
    print("DNI/RUC:", dni)
    print("Asunto:", asunto)
    print("Área:", area)
    print("Folios:", cantidad)
    print("Fecha:", fecha)
    print("======================================")
# ============================================
# MOSTRAR UN EXPEDIENTE
# ============================================
def mostrar_expediente(i):
    print("--------------------------------------")
    print("Código:", codigos[i])
    print("DNI/RUC:", dnis[i])
    print("Remitente:", nombres[i])
    print("Asunto:", asuntos[i])
    print("Área:", areas[i])
    print("Folios:", folios[i])
    print("Fecha:", fechas[i])
    print("--------------------------------------")
# ============================================
# BUSCAR EXPEDIENTE - BÚSQUEDA LINEAL
# ============================================
def buscar_expediente():
    print("\n========== BUSCAR EXPEDIENTE ==========")
    if len(codigos) == 0:
        print("No hay expedientes registrados.")
        return
    busqueda = input(
        "Ingrese código de expediente o DNI/RUC: "
    ).strip().upper()
    encontrado = False
    for i in range(len(codigos)):
        if codigos[i].upper() == busqueda or dnis[i] == busqueda:
            mostrar_expediente(i)
            encontrado = True
    if not encontrado:
        print("No se encontró ningún expediente.")
# ============================================
# ORDENAR EXPEDIENTES - MÉTODO BURBUJA
# ============================================
def ordenar_expedientes():
    print("\n========== ORDENAR EXPEDIENTES ==========")

    total = len(codigos)
    if total < 2:
        print("Se necesitan al menos 2 expedientes.")
        return
    # Arreglos paralelos que deben intercambiarse juntos
    arreglos = [
        codigos, dnis, nombres, asuntos,
        areas, folios, fechas
    ]
    for i in range(total - 1):
        for j in range(total - 1 - i):
            if codigos[j] > codigos[j + 1]:
                for arreglo in arreglos:
                    arreglo[j], arreglo[j + 1] = (
                        arreglo[j + 1], arreglo[j]
                    )
    guardar_datos()
    print("Expedientes ordenados correctamente.")
    mostrar_listado()
# ============================================
# MOSTRAR LISTADO GENERAL
# ============================================
def mostrar_listado():
    print("\n========== LISTADO GENERAL ==========")
    if len(codigos) == 0:
        print("No existen expedientes registrados.")
        return
    print("Total de expedientes:", len(codigos))
    for i in range(len(codigos)):
        print("\nExpediente N°", i + 1)
        mostrar_expediente(i)
# ============================================
# MENÚ PRINCIPAL
# ============================================
def menu_principal():
    cargar_datos()
    while True:
        print("\n==========================================")
        print("        GOBIERNO REGIONAL DE CAJAMARCA")
        print("             MESA DE PARTES DIGITAL")
        print("==========================================")
        print("1. Registrar nuevo expediente")
        print("2. Buscar expediente")
        print("3. Ordenar expedientes por código")
        print("4. Mostrar listado general")
        print("5. Salir del sistema")
        print("==========================================")

        opcion = input("Seleccione una opción (1-5): ").strip()
        if opcion == "1":
            registrar_expediente()
        elif opcion == "2":
            buscar_expediente()
        elif opcion == "3":
            ordenar_expedientes()
        elif opcion == "4":
            mostrar_listado()
        elif opcion == "5":
            print("\nFinalizando el sistema...")
            print("Gracias por utilizar Mesa de Partes Digital.")
            break
        else:
            print("ERROR: Seleccione una opción válida.")
# ============================================
# INICIO DEL PROGRAMA
# ============================================
if __name__ == "__main__":
    menu_principal()
