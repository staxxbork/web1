import json
import os
import sys
from colorama import init, Fore, Style

# Inicializa colorama
init(autoreset=True)

def obtener_ruta_archivo(nombre_archivo):
    if getattr(sys, 'frozen', False):  # Ejecutable PyInstaller
        carpeta = os.path.dirname(sys.executable)
    else:
        carpeta = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(carpeta, nombre_archivo)

ARCHIVO = obtener_ruta_archivo("trabajo.json")

PAGO_POR_HORA = 17
DIAS_POR_SEMANA = 6

# Defino colores personalizados para "niña princesa"
COLOR_TITULO = Fore.MAGENTA + Style.BRIGHT
COLOR_SEPARADOR = Fore.LIGHTMAGENTA_EX
COLOR_OPCION = Fore.LIGHTMAGENTA_EX + Style.BRIGHT
COLOR_INPUT = Fore.MAGENTA
COLOR_EXITO = Fore.LIGHTMAGENTA_EX
COLOR_ERROR = Fore.LIGHTRED_EX + Style.BRIGHT
COLOR_INFO = Fore.LIGHTMAGENTA_EX
COLOR_DIA = Fore.LIGHTMAGENTA_EX + Style.BRIGHT
COLOR_MENSAJE = Fore.LIGHTMAGENTA_EX

def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")

def cargar_datos():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r") as f:
            return json.load(f)
    else:
        return {"semanas": []}

def guardar_datos(datos):
    with open(ARCHIVO, "w") as f:
        json.dump(datos, f, indent=4)

def separador(titulo=""):
    print(COLOR_SEPARADOR + "\n" + "=" * 50)
    if titulo:
        print(COLOR_TITULO + f"  {titulo}")
        print(COLOR_SEPARADOR + "=" * 50 + Style.RESET_ALL)
    else:
        print(Style.RESET_ALL)

def mostrar_semanas(datos):
    limpiar_pantalla()
    separador("🗓 HORAS POR SEMANA")
    print()
    for i, semana in enumerate(datos["semanas"], start=1):
        horas_semana = sum(semana)
        print(COLOR_OPCION + f"  Semana {i:<2} → {horas_semana:>4} hrs  |  ${horas_semana * PAGO_POR_HORA:>7.2f}")
    print()
    input(COLOR_INPUT + "> Presiona Enter para volver..." + Style.RESET_ALL)

def mostrar_quincenas(datos):
    limpiar_pantalla()
    separador("📅 HORAS POR QUINCENA")
    print()
    quincena_num = 1
    for i in range(0, len(datos["semanas"]), 2):
        horas_quincena = sum(sum(datos["semanas"][j]) for j in range(i, min(i+2, len(datos["semanas"])) ))
        print(COLOR_OPCION + f"  Quincena {quincena_num} → {horas_quincena:>4} hrs  |  ${horas_quincena * PAGO_POR_HORA:>7.2f}")
        for semana_idx in range(i, min(i+2, len(datos["semanas"]))):
            horas_semana = sum(datos["semanas"][semana_idx])
            print(Fore.MAGENTA + f"     Semana {semana_idx + 1} → {horas_semana:>4} hrs  |  ${horas_semana * PAGO_POR_HORA:>7.2f}")
        print()
        quincena_num += 1
    input(COLOR_INPUT + "> Presiona Enter para volver..." + Style.RESET_ALL)

def mostrar_meses(datos):
    limpiar_pantalla()
    separador("📆 HORAS POR MES")
    print()
    for i in range(0, len(datos["semanas"]), 4):
        horas_mes = sum(sum(datos["semanas"][j]) for j in range(i, min(i+4, len(datos["semanas"])) ))
        print(COLOR_OPCION + f"  Mes {i//4 + 1:<2} → {horas_mes:>4} hrs  |  ${horas_mes * PAGO_POR_HORA:>7.2f}")
    print()
    input(COLOR_INPUT + "> Presiona Enter para volver..." + Style.RESET_ALL)

def horas_totales(datos):
    while True:
        limpiar_pantalla()
        separador("📊 HORAS TOTALES - MENÚ")
        print()
        print(COLOR_OPCION + "- 1. Ver por semanas")
        print("- 2. Ver por quincenas")
        print("- 3. Ver por meses")
        print("- 4. Volver al menú principal" + Style.RESET_ALL)
        print()
        opcion = input(COLOR_INPUT + "> Elija una opción: " + Style.RESET_ALL)
        if opcion == "1":
            mostrar_semanas(datos)
        elif opcion == "2":
            mostrar_quincenas(datos)
        elif opcion == "3":
            mostrar_meses(datos)
        elif opcion == "4":
            break
        else:
            print(COLOR_ERROR + "⚠ Opción inválida." + Style.RESET_ALL)
            input(COLOR_INPUT + "> Presiona Enter para continuar..." + Style.RESET_ALL)

def horas_semana_actual(datos):
    limpiar_pantalla()
    separador("📅 HORAS ESTA SEMANA 📅")
    print()
    if datos["semanas"]:
        semana_actual = datos["semanas"][-1]
        horas = sum(semana_actual)
        ganancia = horas * PAGO_POR_HORA
        dia_actual = len(semana_actual) + 1
        if dia_actual > DIAS_POR_SEMANA:
            dia_actual = DIAS_POR_SEMANA
        print(COLOR_OPCION + f"📍 Semana actual: {len(datos['semanas'])}")
        print(f"📍 Día actual: {dia_actual} de {DIAS_POR_SEMANA}")
        print(f"⏳ Horas acumuladas: {horas} hrs")
        print(f"💵 Ganancia acumulada: ${ganancia:.2f}" + Style.RESET_ALL)
    else:
        print(COLOR_ERROR + "⚠ No hay registros aún." + Style.RESET_ALL)
    print()
    input(COLOR_INPUT + "> Presiona Enter para continuar..." + Style.RESET_ALL)

def registrar_horas(datos):
    limpiar_pantalla()
    separador("REGISTRAR HORAS ✏")
    print()
    if not datos["semanas"]:
        datos["semanas"].append([])
    semana_actual = datos["semanas"][-1]

    if len(semana_actual) >= DIAS_POR_SEMANA:
        print(COLOR_SEPARADOR + "⚠ La semana actual ya tiene los 6 días registrados.\nSe comenzará una nueva semana automáticamente." + Style.RESET_ALL)
        datos["semanas"].append([])
        semana_actual = datos["semanas"][-1]

    semana_numero = len(datos["semanas"])
    dia_actual = len(semana_actual) + 1

    print(COLOR_OPCION + f"📍 Semana actual: {semana_numero}")
    print(f"📍 Día actual: {dia_actual} de {DIAS_POR_SEMANA}")

    print()
    print(COLOR_MENSAJE + "- Para volver sin registrar, ingrese 'V'")
    print("- Para terminar la semana sin completar 6 días, ingrese 'T'" + Style.RESET_ALL)

    entrada = input(COLOR_INPUT + "\n> Ingrese horas trabajadas hoy: " + Style.RESET_ALL).strip()

    if entrada.lower() == 'v':
        print(COLOR_SEPARADOR + "⏎ Volviendo sin registrar horas..." + Style.RESET_ALL)
        print()
        input(COLOR_INPUT + "> Presiona Enter para continuar..." + Style.RESET_ALL)
        return
    if entrada.lower() == 't':
        if len(semana_actual) == 0:
            print(COLOR_ERROR + "⚠ No se puede terminar una semana sin ningún día registrado." + Style.RESET_ALL)
            print()
            input(COLOR_INPUT + "> Presiona Enter para continuar..." + Style.RESET_ALL)
            return
        print(COLOR_SEPARADOR + f"🎯 Semana {semana_numero} finalizada manualmente con {len(semana_actual)} días." + Style.RESET_ALL)
        datos["semanas"].append([])
        guardar_datos(datos)
        print()
        input(COLOR_INPUT + "> Presiona Enter para continuar..." + Style.RESET_ALL)
        return

    try:
        horas_hoy = float(entrada)
        if horas_hoy < 0:
            raise ValueError()
    except ValueError:
        print(COLOR_ERROR + "⚠ Entrada inválida. Debe ingresar un número positivo." + Style.RESET_ALL)
        print()
        input(COLOR_INPUT + "> Presiona Enter para continuar..." + Style.RESET_ALL)
        return registrar_horas(datos)

    semana_actual.append(horas_hoy)
    ganancia_dia = horas_hoy * PAGO_POR_HORA
    print(COLOR_EXITO + f"✅ Ganancia de hoy: ${ganancia_dia:.2f}" + Style.RESET_ALL)

    if len(semana_actual) == DIAS_POR_SEMANA:
        print(COLOR_SEPARADOR + "\n🎯 Semana completada. La próxima vez se comenzará una nueva." + Style.RESET_ALL)

    guardar_datos(datos)
    print()
    input(COLOR_INPUT + "> Presiona Enter para continuar..." + Style.RESET_ALL)

def modificar_horas(datos):
    if not datos["semanas"]:
        limpiar_pantalla()
        print(COLOR_ERROR + "⚠ No hay registros para modificar." + Style.RESET_ALL)
        print()
        input(COLOR_INPUT + "> Presiona Enter para continuar..." + Style.RESET_ALL)
        return

    while True:
        limpiar_pantalla()
        separador("🛠 MODIFICAR HORAS REGISTRADAS 🛠")
        print()
        print(COLOR_OPCION + f"Hay {len(datos['semanas'])} semanas registradas." + Style.RESET_ALL)
        print()
        try:
            semana_num = int(input(COLOR_INPUT + "> Ingrese número de semana (1-" + str(len(datos['semanas'])) + ")\n  (0 para salir): " + Style.RESET_ALL))
        except ValueError:
            print(COLOR_ERROR + "⚠ Entrada inválida." + Style.RESET_ALL)
            print()
            input(COLOR_INPUT + "> Presiona Enter para continuar..." + Style.RESET_ALL)
            continue
        if semana_num == 0:
            break
        if not (1 <= semana_num <= len(datos['semanas'])):
            print(COLOR_ERROR + "⚠ Semana fuera de rango." + Style.RESET_ALL)
            print()
            input(COLOR_INPUT + "> Presiona Enter para continuar..." + Style.RESET_ALL)
            continue

        semana = datos["semanas"][semana_num - 1]
        print()
        print(COLOR_OPCION + f"Semana {semana_num} tiene {len(semana)} días registrados." + Style.RESET_ALL)
        print()

        for i in range(1, DIAS_POR_SEMANA + 1):
            horas = semana[i - 1] if i <= len(semana) else 0
            print(COLOR_DIA + f"  Día {i} → {horas} hrs" + Style.RESET_ALL)

        print()
        try:
            dia_num = int(input(COLOR_INPUT + "> Ingrese número de día a modificar (1-" + str(DIAS_POR_SEMANA) + ")\n  (0 para volver): " + Style.RESET_ALL))
        except ValueError:
            print(COLOR_ERROR + "⚠ Entrada inválida." + Style.RESET_ALL)
            print()
            input(COLOR_INPUT + "> Presiona Enter para continuar..." + Style.RESET_ALL)
            continue
        if dia_num == 0:
            continue
        if not (1 <= dia_num <= DIAS_POR_SEMANA):
            print(COLOR_ERROR + "⚠ Día fuera de rango." + Style.RESET_ALL)
            print()
            input(COLOR_INPUT + "> Presiona Enter para continuar..." + Style.RESET_ALL)
            continue

        nuevo_valor = input(COLOR_INPUT + f"> Ingrese nuevas horas para Semana {semana_num} Día {dia_num}: " + Style.RESET_ALL).strip()
        try:
            nuevo_horas = float(nuevo_valor)
            if nuevo_horas < 0:
                raise ValueError()
        except ValueError:
            print(COLOR_ERROR + "⚠ Horas inválidas. Debe ingresar un número positivo." + Style.RESET_ALL)
            print()
            input(COLOR_INPUT + "> Presiona Enter para continuar..." + Style.RESET_ALL)
            continue

        if dia_num > len(semana):
            while len(semana) < dia_num - 1:
                semana.append(0)
            semana.append(nuevo_horas)
        else:
            semana[dia_num - 1] = nuevo_horas

        guardar_datos(datos)
        print(COLOR_EXITO + f"✅ Registro actualizado: Semana {semana_num} Día {dia_num} → {nuevo_horas} hrs" + Style.RESET_ALL)
        print()
        input(COLOR_INPUT + "> Presiona Enter para continuar..." + Style.RESET_ALL)
        break

def navegar_por_semanas(datos):
    if not datos["semanas"]:
        limpiar_pantalla()
        print(COLOR_ERROR + "⚠ No hay registros para mostrar." + Style.RESET_ALL)
        print()
        input(COLOR_INPUT + "> Presiona Enter para continuar..." + Style.RESET_ALL)
        return

    indice_semana = 0
    while True:
        limpiar_pantalla()
        semana = datos["semanas"][indice_semana]
        horas_semana = sum(semana)
        print(COLOR_SEPARADOR + f"📖 Semana {indice_semana + 1} de {len(datos['semanas'])}" + Style.RESET_ALL)
        print(COLOR_OPCION + f"⏳ Total horas: {horas_semana} hrs | 💵 Total: ${horas_semana * PAGO_POR_HORA:.2f}" + Style.RESET_ALL)
        print(COLOR_SEPARADOR + "-" * 40 + Style.RESET_ALL)
        print()
        for dia_idx in range(1, DIAS_POR_SEMANA + 1):
            horas = semana[dia_idx - 1] if dia_idx <= len(semana) else 0
            print(COLOR_DIA + f"Día {dia_idx} → {horas} hrs | ${horas * PAGO_POR_HORA:.2f}" + Style.RESET_ALL)
        print()
        print(COLOR_EXITO + "[A] Anterior  |  [S] Siguiente  |  [Q] Salir" + Style.RESET_ALL)
        print()
        opcion = input(COLOR_INPUT + "> " + Style.RESET_ALL).strip().lower()
        if opcion == "a" and indice_semana > 0:
            indice_semana -= 1
        elif opcion == "s" and indice_semana < len(datos["semanas"]) - 1:
            indice_semana += 1
        elif opcion == "q":
            break

def mostrar_dibujo():
    limpiar_pantalla()
    print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT)
    print("       🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸")
    print("                                          ")
    print("         (\\_/)                           ")
    print("         ( •_•)   My Melody                 ")
    print("         / >🎀                              ")
    print("                                            ")
    print("            🌷  Stef te ama!  🌷               ")
    print("                                          ")
    print("       🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸" + Style.RESET_ALL)
    print()

def menu():
    datos = cargar_datos()
    while True:
        mostrar_dibujo()
        separador(" REGISTRO DE HORAS Y GANANCIAS ")
        print()
        print(COLOR_OPCION + "- 1. Registrar horas de hoy")
        print("- 2. Ver horas totales")
        print("- 3. Ver horas de esta semana")
        print("- 4. Navegar por semanas")
        print("- 5. Modificar horas registradas")
        print("- 6. Salir" + Style.RESET_ALL)
        print()
        opcion = input(COLOR_INPUT + "> " + Style.RESET_ALL)

        if opcion == "1":
            registrar_horas(datos)
        elif opcion == "2":
            horas_totales(datos)
        elif opcion == "3":
            horas_semana_actual(datos)
        elif opcion == "4":
            navegar_por_semanas(datos)
        elif opcion == "5":
            modificar_horas(datos)
        elif opcion == "6":
            limpiar_pantalla()
            print(COLOR_SEPARADOR + "👋 ¡Hasta la próxima!" + Style.RESET_ALL)
            break
        else:
            print(COLOR_ERROR + "⚠ Opción inválida." + Style.RESET_ALL)
            print()
            input(COLOR_INPUT + "> Presiona Enter para continuar..." + Style.RESET_ALL)

if __name__ == "__main__":
    menu()
