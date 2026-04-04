import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import os

# Configuracion de la pagina 
st.set_page_config(page_title="Musica y Salud Mental", page_icon="🎵", layout="wide")

# Titulo y descripcion de la app
st.title("Análisis estadístico de la Correlación entre Hábitos Auditivos y Perfiles de Salud Mental.")
st.write("Visualizacion entre los hábitos de consumo musical y diferentes indicadores de salud mental mediante el uso de técnicas de análisis estadístico.")
st.markdown("---")

# Carga de Datos

FILE_PATH = "datos_musica_limpios_FINAL.csv"

@st.cache_data
def load_data(path):
    data = pd.read_csv(path)
    return data

try:
    df =load_data(FILE_PATH)
    st.success(f"Datos cargados correctamente: **{df.shape[0]}** participantes y **{df.shape[1]}** columnas.")
except Exception as e:
    st.error(f"Error al cargar datos: {e}")
    st.stop()

# Filtros para la interactividad
st.sidebar.header("Filtros de Interactividad")

# Rango de edad
age_min, age_max = st.sidebar.slider(
    "Edad", 
    int(df['age'].min()), 
    int(df['age'].max()), 
    (int(df['age'].min()), int(df['age'].max()))
)

# Servicio de streaming
streaming_options = sorted(df["primary_streaming_service"].unique())
selected_streaming = st.sidebar.multiselect(
    "Servicio de streaming principal", 
    options=streaming_options, 
    default=streaming_options
)

# Género musical favorito
genre_options = sorted(df["fav_genre"].unique())
selected_genres = st.sidebar.multiselect(
    "Género musical favorito", 
    options=genre_options, 
    default=genre_options
)

# Horas de música al día
hours_min, hours_max = st.sidebar.slider(
    "Horas de música al día", 
    float(df['hours_per_day'].min()), 
    float(df['hours_per_day'].max()), 
    (float(df['hours_per_day'].min()), float(df['hours_per_day'].max()))
)

# Escucha mientras trabaja
while_working_options = ["Sí", "No"]
selected_while_working = st.sidebar.multiselect(
    "Escucha música mientras trabaja", 
    options=while_working_options, 
    default=while_working_options
)

#  Efecto percibido de la música. (cambio a texto para mejor entendimiento)
effect_map = {
    "Mejora": 1,
    "Sin efecto": 0,
    "Empeora": -1
}

selected_effect_text = st.sidebar.multiselect(
    "Efecto percibido de la música",
    options=["Mejora", "Sin efecto", "Empeora"],
    default=["Mejora", "Sin efecto", "Empeora"]
)

# El texto seleccionado a los números originales del dataset
selected_effect_values = [effect_map[text] for text in selected_effect_text]

# Aplicacion de los filtros
filtered_df = df[
    (df['age'] >= age_min) & (df['age'] <= age_max) &
    (df['primary_streaming_service'].isin(selected_streaming)) &
    (df['fav_genre'].isin(selected_genres)) &
    (df['hours_per_day'].between(hours_min, hours_max)) &
    (df['music_effects'].isin(selected_effect_values))
]

# Filtro adicional para "While Working" (Sí/No)
if selected_while_working:
    while_map = {"Sí": 1, "No": 0}
    selected_values = [while_map[w] for w in selected_while_working]
    filtered_df = filtered_df[filtered_df['while_working'].isin(selected_values)]


# Tabs Principales
st.markdown("---")

tab_inicio, tab_datos, tab_salud, tab_habitos, tab_avanzado = st.tabs([
    "🏠 Inicio y KPIs",
    "📋 Datos Generales",
    "🧠 Salud Mental",
    "🎵 Hábitos Musicales",
    "📊 Análisis Avanzado"
])

# tab_inicio:
with tab_inicio:
    st.subheader("KPIs principales del estudio")                          

    # Creacion de columnas
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Total de Participantes.",
            value=len(filtered_df)
        )

    with col2:
        improve_pct = (filtered_df["music_effects"] == 1).mean() * 100
        st.metric(
            label="% que dice que la música mejora",
            value=f"{improve_pct:.1f}%",
            help="Porcentaje de participantes que perciben mejora en su bienestar con la música"
        )
    
    with col3:
        score_promedio = filtered_df[['anxiety', 'depression', 'insomnia', 'ocd']].mean(axis=1).mean()
        st.metric(
            label="Promedio General de Salud Mental",
            value=f"{score_promedio:.2f}",
            help="Promedio combinado de ansiedad, depresión, insomnio y OCD (0-10). Mayor valor = peor salud mental reportada."
        )

    st.markdown("---")

#tab_datos
with tab_datos:
    st.subheader("Estructura y características del conjunto de datos")
    
    # Información básica
    st.markdown(f"""
    **Dimensiones actuales:** {filtered_df.shape[0]:,} filas (participantes) × {filtered_df.shape[1]} columnas
    """)
    
    st.metric("Número total de participantes", f"{len(filtered_df):,}")

    st.markdown("---")

    # Resumen por categorias
    st.write("**Clasificación de las variables del dataset:**")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**📋 Datos Demográficos y Generales**")
        st.write("• age")
        st.write("• primary_streaming_service")
        st.write("• instrumentalist")
        st.write("• composer")
        st.write("• foreign_languages")

    with col2:
        st.markdown("**🎵 Hábitos y Preferencias Musicales**")
        st.write("• fav_genre")
        st.write("• hours_per_day")
        st.write("• bpm")
        st.write("• while_working")
        st.write("• music_effects")
        st.write("• frequency_... (12 géneros musicales)")

    with col3:
        st.markdown("**🧠 Indicadores de Salud Mental**")
        st.write("• anxiety")
        st.write("• depression")
        st.write("• insomnia")
        st.write("• ocd")

    st.markdown("---")

    # Tabla completa de columnas (opcional, pero útil)
    st.write("**Lista completa de columnas:**")
    columnas_df = pd.DataFrame({"Nombre de la columna": df.columns.tolist()})
    st.dataframe(columnas_df, use_container_width=True, hide_index=True)

    st.caption(f"Total de columnas: **{len(df.columns)}**")

    st.markdown("---")