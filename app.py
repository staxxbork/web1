from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import json
import os
import sys
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Cambia esto por una clave más segura

def obtener_ruta_archivo(nombre_archivo):
    if getattr(sys, 'frozen', False):  # Ejecutable PyInstaller
        carpeta = os.path.dirname(sys.executable)
    else:
        carpeta = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(carpeta, nombre_archivo)

ARCHIVO = obtener_ruta_archivo("trabajo.json")
PAGO_POR_HORA = 17
DIAS_POR_SEMANA = 6

def cargar_datos():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r") as f:
            return json.load(f)
    else:
        return {"semanas": []}

def guardar_datos(datos):
    with open(ARCHIVO, "w") as f:
        json.dump(datos, f, indent=4)

@app.route('/')
def index():
    datos = cargar_datos()
    total_horas = sum(sum(semana) for semana in datos["semanas"])
    total_ganancia = total_horas * PAGO_POR_HORA
    
    # Datos para la semana actual
    semana_actual_horas = 0
    semana_actual_ganancia = 0
    semana_numero = 0
    dia_actual = 1
    
    if datos["semanas"]:
        semana_actual = datos["semanas"][-1]
        semana_actual_horas = sum(semana_actual)
        semana_actual_ganancia = semana_actual_horas * PAGO_POR_HORA
        semana_numero = len(datos["semanas"])
        dia_actual = len(semana_actual) + 1
        if dia_actual > DIAS_POR_SEMANA:
            dia_actual = DIAS_POR_SEMANA
    
    return render_template('index.html', 
                         total_horas=total_horas,
                         total_ganancia=total_ganancia,
                         semana_actual_horas=semana_actual_horas,
                         semana_actual_ganancia=semana_actual_ganancia,
                         semana_numero=semana_numero,
                         dia_actual=dia_actual,
                         dias_por_semana=DIAS_POR_SEMANA)

@app.route('/registrar', methods=['GET', 'POST'])
def registrar_horas():
    if request.method == 'POST':
        datos = cargar_datos()
        
        if not datos["semanas"]:
            datos["semanas"].append([])
        
        semana_actual = datos["semanas"][-1]
        
        if len(semana_actual) >= DIAS_POR_SEMANA:
            datos["semanas"].append([])
            semana_actual = datos["semanas"][-1]
        
        accion = request.form.get('accion')
        
        if accion == 'terminar':
            if len(semana_actual) == 0:
                flash('No se puede terminar una semana sin ningún día registrado.', 'error')
            else:
                datos["semanas"].append([])
                guardar_datos(datos)
                flash(f'Semana {len(datos["semanas"])-1} finalizada manualmente con {len(semana_actual)} días.', 'success')
            return redirect(url_for('registrar_horas'))
        
        try:
            horas_hoy = float(request.form['horas'])
            if horas_hoy < 0:
                raise ValueError()
        except (ValueError, KeyError):
            flash('Entrada inválida. Debe ingresar un número positivo.', 'error')
            return redirect(url_for('registrar_horas'))
        
        semana_actual.append(horas_hoy)
        ganancia_dia = horas_hoy * PAGO_POR_HORA
        
        guardar_datos(datos)
        flash(f'✅ Ganancia de hoy: ${ganancia_dia:.2f}', 'success')
        
        if len(semana_actual) == DIAS_POR_SEMANA:
            flash('🎯 Semana completada. La próxima vez se comenzará una nueva.', 'info')
        
        return redirect(url_for('registrar_horas'))
    
    # GET request
    datos = cargar_datos()
    if not datos["semanas"]:
        datos["semanas"].append([])
    
    semana_actual = datos["semanas"][-1]
    semana_numero = len(datos["semanas"])
    dia_actual = len(semana_actual) + 1
    
    if len(semana_actual) >= DIAS_POR_SEMANA:
        dia_actual = "Nueva semana"
    
    return render_template('registrar.html', 
                         semana_numero=semana_numero,
                         dia_actual=dia_actual,
                         dias_por_semana=DIAS_POR_SEMANA,
                         semana_completa=len(semana_actual) >= DIAS_POR_SEMANA)

@app.route('/semanas')
def ver_semanas():
    datos = cargar_datos()
    semanas_info = []
    
    for i, semana in enumerate(datos["semanas"], start=1):
        horas_semana = sum(semana)
        ganancia_semana = horas_semana * PAGO_POR_HORA
        semanas_info.append({
            'numero': i,
            'horas': horas_semana,
            'ganancia': ganancia_semana
        })
    
    return render_template('semanas.html', semanas=semanas_info)

@app.route('/quincenas')
def ver_quincenas():
    datos = cargar_datos()
    quincenas_info = []
    
    quincena_num = 1
    for i in range(0, len(datos["semanas"]), 2):
        horas_quincena = sum(sum(datos["semanas"][j]) for j in range(i, min(i+2, len(datos["semanas"]))))
        ganancia_quincena = horas_quincena * PAGO_POR_HORA
        
        semanas_detalle = []
        for semana_idx in range(i, min(i+2, len(datos["semanas"]))):
            horas_semana = sum(datos["semanas"][semana_idx])
            ganancia_semana = horas_semana * PAGO_POR_HORA
            semanas_detalle.append({
                'numero': semana_idx + 1,
                'horas': horas_semana,
                'ganancia': ganancia_semana
            })
        
        quincenas_info.append({
            'numero': quincena_num,
            'horas': horas_quincena,
            'ganancia': ganancia_quincena,
            'semanas': semanas_detalle
        })
        quincena_num += 1
    
    return render_template('quincenas.html', quincenas=quincenas_info)

@app.route('/meses')
def ver_meses():
    datos = cargar_datos()
    meses_info = []
    
    for i in range(0, len(datos["semanas"]), 4):
        horas_mes = sum(sum(datos["semanas"][j]) for j in range(i, min(i+4, len(datos["semanas"]))))
        ganancia_mes = horas_mes * PAGO_POR_HORA
        meses_info.append({
            'numero': i//4 + 1,
            'horas': horas_mes,
            'ganancia': ganancia_mes
        })
    
    return render_template('meses.html', meses=meses_info)

@app.route('/navegar')
def navegar_semanas():
    datos = cargar_datos()
    if not datos["semanas"]:
        flash('No hay registros para mostrar.', 'error')
        return redirect(url_for('index'))
    
    semana_idx = request.args.get('semana', 0, type=int)
    if semana_idx < 0 or semana_idx >= len(datos["semanas"]):
        semana_idx = 0
    
    semana = datos["semanas"][semana_idx]
    horas_semana = sum(semana)
    ganancia_semana = horas_semana * PAGO_POR_HORA
    
    dias_info = []
    for dia_idx in range(1, DIAS_POR_SEMANA + 1):
        horas = semana[dia_idx - 1] if dia_idx <= len(semana) else 0
        ganancia = horas * PAGO_POR_HORA
        dias_info.append({
            'numero': dia_idx,
            'horas': horas,
            'ganancia': ganancia
        })
    
    return render_template('navegar.html',
                         semana_actual=semana_idx + 1,
                         total_semanas=len(datos["semanas"]),
                         horas_semana=horas_semana,
                         ganancia_semana=ganancia_semana,
                         dias=dias_info,
                         semana_idx=semana_idx)

@app.route('/modificar', methods=['GET', 'POST'])
def modificar_horas():
    datos = cargar_datos()
    
    if not datos["semanas"]:
        flash('No hay registros para modificar.', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        try:
            semana_num = int(request.form['semana'])
            dia_num = int(request.form['dia'])
            nuevas_horas = float(request.form['horas'])
            
            if not (1 <= semana_num <= len(datos['semanas'])):
                flash('Semana fuera de rango.', 'error')
                return redirect(url_for('modificar_horas'))
            
            if not (1 <= dia_num <= DIAS_POR_SEMANA):
                flash('Día fuera de rango.', 'error')
                return redirect(url_for('modificar_horas'))
            
            if nuevas_horas < 0:
                flash('Las horas deben ser un número positivo.', 'error')
                return redirect(url_for('modificar_horas'))
            
            semana = datos["semanas"][semana_num - 1]
            
            if dia_num > len(semana):
                while len(semana) < dia_num - 1:
                    semana.append(0)
                semana.append(nuevas_horas)
            else:
                semana[dia_num - 1] = nuevas_horas
            
            guardar_datos(datos)
            flash(f'✅ Registro actualizado: Semana {semana_num} Día {dia_num} → {nuevas_horas} hrs', 'success')
            
        except (ValueError, KeyError):
            flash('Entrada inválida. Verifique los datos ingresados.', 'error')
        
        return redirect(url_for('modificar_horas'))
    
    # GET request
    semanas_info = []
    for i, semana in enumerate(datos["semanas"], start=1):
        dias_info = []
        for j in range(1, DIAS_POR_SEMANA + 1):
            horas = semana[j - 1] if j <= len(semana) else 0
            dias_info.append({
                'numero': j,
                'horas': horas
            })
        
        semanas_info.append({
            'numero': i,
            'dias': dias_info,
            'total_dias': len(semana)
        })
    
    return render_template('modificar.html', semanas=semanas_info, dias_por_semana=DIAS_POR_SEMANA)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)