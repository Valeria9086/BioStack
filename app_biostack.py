import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Bio-Stack | Control de Bioprocesos", layout="wide")

# --- DISEÑO ADAPTATIVO PROFESIONAL (DARK & LIGHT MODE) ---
st.markdown("""
    <style>
        /* Estilo para las tarjetas de métricas que se adapta al tema */
        div[data-testid="metric-container"] {
            background-color: rgba(28, 131, 225, 0.03);
            border: 1px solid rgba(46, 125, 50, 0.3);
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        
        /* Botón con degradado tecnológico Bio */
        .stButton>button {
            width: 100%;
            border-radius: 12px;
            height: 3.2em;
            background: linear-gradient(90deg, #2E7D32 0%, #1B5E20 100%);
            color: white;
            border: none;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            opacity: 0.9;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(46, 125, 50, 0.3);
        }

        /* Ajuste de títulos para legibilidad */
        .main-title {
            font-weight: 800;
            letter-spacing: -1px;
            margin-bottom: 0px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'> Bio-Stack</h1>", unsafe_allow_html=True)
st.markdown("#### Gestión Epigenética | Nodo Puebla, MX")
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
    df['Fecha'] = pd.to_datetime(df['Fecha'], format='mixed')
    
    # 3. MÉTRICAS CLAVE (KPIs) - DISEÑO NEUTRO
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Temperatura", value=f"{df['Temp_C'].iloc[-1]} °C")
    with col2:
        st.metric(label="Estado Sistema", value=df['Accion_Biotech'].iloc[-1])
    with col3:
        st.metric(label="Humedad", value=f"{df['Hum_Porcentaje'].iloc[-1]} %")

    # 4. GRÁFICA DE IMPACTO (Usa el tema del sistema)
    st.subheader("Análisis de Estrés Térmico")
    fig = px.line(df, x='Fecha', y='Temp_C', 
                  line_shape='spline', markers=True,
                  template="plotly_dark" if st.get_option("theme.base") == "dark" else "plotly_white")
    
    fig.add_hline(y=28, line_dash="dot", line_color="#ef5350", annotation_text="Límite Crítico")
    fig.update_traces(line_color='#43a047')
    fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), height=350)
    st.plotly_chart(fig, use_container_width=True)

    # 5. BITÁCORA Y RESUMEN
    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.subheader("Intervenciones")
        fig_pie = px.pie(df, names='Accion_Biotech', hole=0.6,
                         color_discrete_sequence=px.colors.sequential.Greens_r)
        fig_pie.update_layout(showlegend=False, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col_b:
        st.subheader("Historial Técnico")
        st.dataframe(df.sort_values(by='Fecha', ascending=False), use_container_width=True, height=250)

    # 7. ASISTENTE DE CULTIVO (DISEÑO ADAPTATIVO)
    st.divider()
    st.subheader("Consultoría Bio-Inteligente")
    
    if st.button("GENERAR DIAGNÓSTICO ESTRATÉGICO"):
        ultima_temp = df['Temp_C'].iloc[-1]
        ultima_hum = df['Hum_Porcentaje'].iloc[-1]

        # Contenedores con colores que funcionan en ambos modos
        if ultima_temp > 28:
            st.error(f"**ALERTA DE ESTRÉS TÉRMICO ({ultima_temp}°C)**")
            st.markdown("""
                * **Diagnóstico:** Superación de umbral homeostático.
                * **Acción:** Activar nebulización inmediata y verificar turgencia celular.
            """)
        elif ultima_hum < 40:
            st.warning(f"**DÉFICIT HÍDRICO DETECTADO ({ultima_hum}%)**")
            st.markdown("""
                * **Diagnóstico:** Alta demanda evaporativa atmosférica.
                * **Acción:** Estabilizar microclima y reducir ventilación.
            """)
        else:
            st.success("**CONDICIONES ÓPTIMAS DETECTADAS**")
            st.markdown("""
                * **Diagnóstico:** Parámetros dentro del rango de máxima eficiencia.
                * **Acción:** Mantener régimen de monitoreo pasivo.
            """)

else:
    st.warning("Esperando conexión con el nodo autónomo...")