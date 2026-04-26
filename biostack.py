# -*- coding: utf-8 -*-
import requests
import datetime
import json
import os

# --- CONFIGURACION ---
API_KEY = "2cff0d03c3c21fb8f16a51f03a27101c"
CIUDAD = "Puebla,MX"

def ejecutar_biostack():
    # 1. Pedir clima actual (Formato compatible y limpio)
    url = "http://api.openweathermap.org/data/2.5/weather?q=" + CIUDAD + "&appid=" + API_KEY + "&units=metric"
    
    try:
        respuesta = requests.get(url)
        datos = respuesta.json()
        
        if 'main' in datos:
            temp = datos['main']['temp']
            hum = datos['main']['humidity']
            fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 2. Logica Predictiva
            if temp > 28:
                accion = "Modulo B (Escudo de dsRNA)"
                justificacion = "Proteccion contra golpe de calor detectado."
            elif hum < 30:
                accion = "Modulo A (Estimulante Radicular)"
                justificacion = "Baja humedad, expandiendo raices."
            else:
                accion = "Monitoreo"
                justificacion = "Clima optimo, planta en equilibrio."

            # 3. Crear el Reporte
            reporte = {
                "Fecha": fecha,
                "Temp_C": temp,
                "Hum_Porcentaje": hum,
                "Accion_Biotech": accion,
                "Motivo": justificacion
            }

            # 4. Guardar los datos
            with open("bitacora_biostack.json", "a") as f:
                f.write(json.dumps(reporte) + "\n")

            print("--- SISTEMA BIO-STACK EJECUTADO CON EXITO ---")
        else:
            print("Error: No se pudieron obtener datos del clima.")
            
    except Exception as e:
        print("Error de conexion: " + str(e))

if __name__ == "__main__":
    ejecutar_biostack()