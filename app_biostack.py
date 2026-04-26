import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os

# 1. CONFIGURACIÓN DE LA PÁGINA (Estilo Profesional)
st.set_page_config(page_title="Bio-Stack | Control de Bioprocesos", layout="wide")

# Estilo Global Personalizado
st.markdown("""
    <style>
        .main { background-color: #0e1117; }
        .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #2e7d32; }
        .stButton>button {
            width: 100%;
            border-radius: 20px;
            height: 3.5em;
            background-color: #2E7D32;
            color: white;
            border: none;
            font-weight: bold;
            font-size: 18px;
            transition: all 0.3s;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
        }
        .stButton>button:hover {
            background-color: #1B5E20;
            border: 1px solid #C8E6C9;
            transform: scale(1.02);
        }
    </style>
""", unsafe_allow_html=True)

st.title("Bio-Stack: Sistema de Gestión Epigenética")
st.markdown("### Nodo de Monitoreo Predictivo - Puebla, MX")

# 2. FUNCIÓN PARA CARGAR DATOS
def cargar_datos():
    if os.path.exists("bitacora_biostack.json"):
        with open("bitacora_biostack.json", "r") as f:
            lineas = f.readlines()
            datos = [json.loads(linea) for linea in lineas]
        return pd.DataFrame(datos)
    return pd.DataFrame()

df = cargar_datos()

if not df.empty:
    # Procesamiento de fechas
    df['Fecha'] = pd.to_datetime(df['Fecha'], format='mixed')
    
    # 3. MÉTRICAS CLAVE (KPIs)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Temperatura Actual", f"{df['Temp_C'].iloc[-1]} °C")
    with col2:
        st.metric("Estado del Sistema", df['Accion_Biotech'].iloc[-1])
    with col3:
        st.metric("Humedad Relativa", f"{df['Hum_Porcentaje'].iloc[-1]} %")

    st.divider()

    # 4. GRÁFICA DE IMPACTO TÉRMICO
    st.subheader("Análisis de Estrés Térmico en Tiempo Real")
    fig = px.line(df, x='Fecha', y='Temp_C', title='Variación Térmica del Cultivo',
                  line_shape='spline', markers=True, template="plotly_dark")
    fig.add_hline(y=28, line_dash="dash", line_color="red", annotation_text="Umbral de Riesgo")
    st.plotly_chart(fig, use_container_width=True)

    # 5. RESUMEN DE INTERVENCIONES (Pie Chart)
    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.subheader("Intervenciones")
        fig_pie = px.pie(df, names='Accion_Biotech', hole=0.4, 
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col_b:
        # 6. TABLA DE LOGS
        st.subheader("Bitácora de Aplicaciones")
        st.dataframe(df.sort_values(by='Fecha', ascending=False), use_container_width=True, height=300)

    # 7. ASISTENTE DE CULTIVO PREMIUM (EL NUEVO APARTADO)
    st.divider()
    with st.container():
        st.subheader("Consultoría Bio-Inteligente")
        st.info("El sistema analizará los datos del nodo para emitir una recomendación técnica basada en IA.")

        if st.button(" GENERAR DIAGNÓSTICO ESTRATÉGICO"):
            ultima_temp = df['Temp_C'].iloc[-1]
            ultima_hum = df['Hum_Porcentaje'].iloc[-1]

            st.markdown("---")
            
            if ultima_temp > 28:
                st.error("###  ALERTA DE ESTRÉS TÉRMICO")
                st.markdown(f"""
                    <div style="background-color:#ffebee; padding:20px; border-radius:10px; border-left: 8px solid #c62828;">
                        <h4 style="color:#c62828; margin:0;">Diagnóstico Clínico:</h4>
                        <p style="color:black; font-size:16px;">La temperatura de <b>{ultima_temp}°C</b> supera el umbral de seguridad. 
                        Se observa riesgo de desnaturalización enzimática y cierre estomático.</p>
                        <h4 style="color:#c62828; margin-top:10px;">Plan de Acción Sugerido:</h4>
                        <ul style="color:black; font-size:15px;">
                            <li><b>Intervención:</b> Activar riego por nebulización para enfriamiento evaporativo.</li>
                            <li><b>Bio-Protocolo:</b> Aplicar inductores de proteínas HSP y protectores osmóticos.</li>
                            <li><b>Monitoreo:</b> Verificar turgencia celular en las próximas 2 horas.</li>
                        </ul>
                    </div>
                """, unsafe_allow_html=True)
            
            elif ultima_hum < 40:
                st.warning("###  ALERTA DE DÉFICIT HÍDRICO")
                st.markdown(f"""
                    <div style="background-color:#fff8e1; padding:20px; border-radius:10px; border-left: 8px solid #f9a825;">
                        <h4 style="color:#f9a825; margin:0;">Diagnóstico Clínico:</h4>
                        <p style="color:black; font-size:16px;">Humedad crítica detectada (<b>{ultima_hum}%</b>). Alta tasa de transpiración en tejidos.</p>
                        <h4 style="color:#f9a825; margin-top:10px;">Plan de Acción Sugerido:</h4>
                        <ul style="color:black; font-size:15px;">
                            <li><b>Intervención:</b> Reducir ventilación forzada para conservar el microclima foliar.</li>
                            <li><b>Bio-Protocolo:</b> Incrementar niveles de Potasio (K+) para regular el potencial hídrico.</li>
                            <li><b>Riesgo:</b> Posible marchitamiento temporal si no se compensa el déficit.</li>
                        </ul>
                    </div>
                """, unsafe_allow_html=True)
            
            else:
                st.success("###  CONDICIONES DE BIOPROCESO ÓPTIMAS")
                st.markdown(f"""
                    <div style="background-color:#e8f5e9; padding:20px; border-radius:10px; border-left: 8px solid #2e7d32;">
                        <h4 style="color:#2e7d32; margin:0;">Diagnóstico Clínico:</h4>
                        <p style="color:black; font-size:16px;">Equilibrio homeostático detectado. El metabolismo se encuentra en su punto máximo de eficiencia fotosintética.</p>
                        <h4 style="color:#2e7d32; margin-top:10px;">Plan de Acción Sugerido:</h4>
                        <ul style="color:black; font-size:15px;">
                            <li><b>Estatus:</b> Continuar con el régimen de fertirriego estándar.</li>
                            <li><b>Recomendación:</b> Excelente momento para aplicaciones de nutrición avanzada.</li>
                            <li><b>Nota:</b> No se detectan señales de estrés abiótico.</li>
                        </ul>
                    </div>
                """, unsafe_allow_html=True)

else:
    st.warning("Esperando datos del sistema autónomo...")
    st.info("Asegúrate de que el proceso de captura de datos esté activo en la terminal.")