import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Bio-Stack | Control de Bioprocesos", layout="wide")

# --- REDISEÑO DE ESTILO (NUEVO Y MÁS BONITO) ---
# He cambiado el fondo de las métricas a blanco con sombra y borde verde.
st.markdown("""
    <style>
        /* Fondo principal ligeramente más claro para contraste */
        .main { background-color: #f4f7f6; }
        
        /* Títulos en verde oscuro */
        h1, h2, h3 { color: #1B5E20 !important; }

        /* --- TARJETAS DE MÉTRICAS (KPIs) REDISEÑADAS --- */
        /* Fondo blanco, sombra suave y bordes redondeados */
        [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
            color: #1B5E20 !important;
        }
        div[data-testid="metric-container"] {
            background-color: #FFFFFF;
            border: 2px solid #2E7D32;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }
        div[data-testid="metric-container"]:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 15px rgba(46, 125, 50, 0.2);
        }

        /* --- BOTÓN DE DIAGNÓSTICO ESTILIZADO --- */
        .stButton>button {
            width: 100%;
            border-radius: 25px;
            height: 3.5em;
            background-color: #2E7D32;
            color: white;
            border: none;
            font-weight: bold;
            font-size: 18px;
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .stButton>button:hover {
            background-color: #1B5E20;
            box-shadow: 0 6px 20px rgba(27, 94, 32, 0.4);
            transform: scale(1.01);
        }
    </style>
""", unsafe_allow_html=True)

st.title("Bio-Stack: Sistema de Gestión Epigenética")
st.markdown("### 📡 Nodo de Monitoreo Predictivo - Puebla, MX")
st.divider()

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
    
    # 3. MÉTRICAS CLAVE (KPIs) - AHORA CON DISEÑO BONITO
    st.subheader("Estado Actual del Cultivo")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Temperatura", value=f"{df['Temp_C'].iloc[-1]} °C")
    with col2:
        st.metric(label="Última Acción", value=df['Accion_Biotech'].iloc[-1])
    with col3:
        st.metric(label="Humedad Relativa", value=f"{df['Hum_Porcentaje'].iloc[-1]} %")

    st.divider()

    # 4. GRÁFICA DE IMPACTO TÉRMICO
    st.subheader("Análisis de Estrés Térmico (Tiempo Real)")
    # Cambié el template a 'plotly_white' para que combine con el nuevo diseño limpio
    fig = px.line(df, x='Fecha', y='Temp_C', title='Variación Térmica del Cultivo',
                  line_shape='spline', markers=True, template="plotly_white")
    fig.add_hline(y=28, line_dash="dash", line_color="#c62828", annotation_text="Umbral de Riesgo")
    # Personalización de colores de la gráfica
    fig.update_traces(line_color='#2E7D32', marker=dict(size=8, color='#1B5E20'))
    st.plotly_chart(fig, use_container_width=True)

    # 5. RESUMEN DE INTERVENCIONES Y TABLA
    st.divider()
    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.subheader("Resumen de Intervenciones")
        fig_pie = px.pie(df, names='Accion_Biotech', hole=0.5, template="plotly_white",
                         color_discrete_sequence=px.colors.sequential.Greens_r)
        fig_pie.update_layout(showlegend=False) # Quitamos la leyenda para limpiar espacio
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col_b:
        # 6. TABLA DE LOGS
        st.subheader("Bitácora de Aplicaciones")
        # Estilizado sutil de la tabla
        st.dataframe(df.sort_values(by='Fecha', ascending=False), use_container_width=True, height=350)

    # 7. ASISTENTE DE CULTIVO PREMIUM (CON DISEÑO ACTUALIZADO)
    st.divider()
    with st.container():
        st.subheader("Consultoría Bio-Inteligente")
        st.info("Diagnóstico técnico de parámetros en tiempo real para la optimización del cultivo.")

        if st.button("GENERAR DIAGNÓSTICO ESTRATÉGICO"):
            ultima_temp = df['Temp_C'].iloc[-1]
            ultima_hum = df['Hum_Porcentaje'].iloc[-1]

            st.markdown("---")
            
            if ultima_temp > 28:
                st.error("### ALERTA DE ESTRÉS TÉRMICO")
                st.markdown(f"""
                    <div style="background-color:#ffebee; padding:25px; border-radius:15px; border-left: 10px solid #c62828; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                        <h4 style="color:#c62828; margin:0; font-weight:bold;">Diagnóstico Técnico:</h4>
                        <p style="color:black; font-size:16px; margin-top:10px;">La temperatura de <b>{ultima_temp}°C</b> supera el umbral de seguridad operativa.</p>
                        <h4 style="color:#c62828; margin-top:15px;">Plan de Acción Sugerido:</h4>
                        <ul style="color:black; font-size:15px;">
                            <li><b>Intervención:</b> Activar sistemas de enfriamiento evaporativo (nebulización).</li>
                            <li><b>Bio-Protocolo:</b> Priorizar la protección de fotosistemas y turgencia celular.</li>
                        </ul>
                    </div>
                """, unsafe_allow_html=True)
            
            elif ultima_hum < 40:
                st.warning("### ALERTA DE DÉFICIT HÍDRICO")
                st.markdown(f"""
                    <div style="background-color:#fff8e1; padding:25px; border-radius:15px; border-left: 10px solid #f9a825; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                        <h4 style="color:#f9a825; margin:0; font-weight:bold;">Diagnóstico Técnico:</h4>
                        <p style="color:black; font-size:16px; margin-top:10px;">Humedad crítica detectada (<b>{ultima_hum}%</b>). Riesgo de deshidratación tisular.</p>
                        <h4 style="color:#f9a825; margin-top:15px;">Plan de Acción Sugerido:</h4>
                        <ul style="color:black; font-size:15px;">
                            <li><b>Intervención:</b> Regular ventilación para estabilizar microclima foliar.</li>
                            <li><b>Monitoreo:</b> Verificar estado hídrico de tejidos conductores.</li>
                        </ul>
                    </div>
                """, unsafe_allow_html=True)
            
            else:
                st.success("### CONDICIONES DE BIOPROCESO ÓPTIMAS")
                st.markdown(f"""
                    <div style="background-color:#e8f5e9; padding:25px; border-radius:15px; border-left: 10px solid #2e7d32; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                        <h4 style="color:#2e7d32; margin:0; font-weight:bold;">Diagnóstico Técnico:</h4>
                        <p style="color:black; font-size:16px; margin-top:10px;">Equilibrio homeostático detectado. Parámetros dentro del rango de máxima eficiencia.</p>
                        <h4 style="color:#2e7d32; margin-top:15px;">Plan de Acción Sugerido:</h4>
                        <ul style="color:black; font-size:15px;">
                            <li><b>Estatus:</b> Mantener régimen de monitoreo pasivo.</li>
                            <li><b>Recomendación:</b> Excelente momento para el desarrollo vegetativo.</li>
                        </ul>
                    </div>
                """, unsafe_allow_html=True)

else:
    st.warning("Esperando datos del sistema autónomo...")
    st.info("Asegúrate de que el proceso de captura de datos esté activo.")