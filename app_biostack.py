import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os

# Configuración de la página (Profesional)
st.set_page_config(page_title="Bio-Stack | Control de Bioprocesos", layout="wide")

st.title(" Bio-Stack: Sistema de Gestión Epigenética")
st.markdown("### Nodo de Monitoreo Predictivo - Puebla, MX")

# Función para cargar datos de la bitácora
def cargar_datos():
    if os.path.exists("bitacora_biostack.json"):
        with open("bitacora_biostack.json", "r") as f:
            lineas = f.readlines()
            datos = [json.loads(linea) for linea in lineas]
        return pd.DataFrame(datos)
    return pd.DataFrame()

df = cargar_datos()

if not df.empty:
    # Convertir fecha a formato entendible
   # Cambia la línea vieja por esta:
    df['Fecha'] = pd.to_datetime(df['Fecha'], format='mixed')
    
    # 1. MÉTRICAS CLAVE (KPIs) en la parte superior
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Temperatura Actual", f"{df['Temp_C'].iloc[-1]} °C")
    with col2:
        st.metric("Estado del Sistema", df['Accion_Biotech'].iloc[-1])
    with col3:
        st.metric("Humedad Relativa", f"{df['Hum_Porcentaje'].iloc[-1]} %")

    st.divider()

    # 2. GRÁFICA DE IMPACTO (Tendencia de Temperatura vs Umbrales)
    st.subheader("Análisis de Estrés Térmico en Tiempo Real")
    fig = px.line(df, x='Fecha', y='Temp_C', title='Variación Térmica del Cultivo',
                 line_shape='spline', markers=True, template="plotly_dark")
    
    # Añadir línea roja de umbral de peligro
    fig.add_hline(y=28, line_dash="dash", line_color="red", annotation_text="Umbral de Estrés")
    st.plotly_chart(fig, use_container_width=True)

    # 3. DISTRIBUCIÓN DE ACCIONES (Gráfica de Pastel)
    st.subheader(" Resumen de Intervenciones Biotecnológicas")
    fig_pie = px.pie(df, names='Accion_Biotech', hole=0.4, 
                     color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_pie)

    # 4. TABLA DE LOGS PROFESIONAL
    st.subheader("Bitácora Histórica de Aplicaciones")
    st.dataframe(df.sort_values(by='Fecha', ascending=False), use_container_width=True)

else:
    st.warning("Esperando datos del sistema autónomo...")