import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib as mp
import matplotlib.pyplot as plt
import seaborn as sb



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
df =load_data(FILE_PATH)

# Filtros para la interactividad
# Columnas para mover el titulo a un lado y la imagen a otro
col_tit, col_gif = st.sidebar.columns([3, 1])
with col_tit:
    st.header("Filtros de Interactividad")
with col_gif:
    st.image("assets/63 sin título_20260411153136.png", width=100)

# Rango de edad
age_min, age_max = st.sidebar.slider(
    "Edad", 
    int(df["age"].min()), 
    int(df["age"].max()), 
    (int(df["age"].min()), int(df["age"].max()))
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
    (df["age"] >= age_min) & (df["age"] <= age_max) &
    (df["primary_streaming_service"].isin(selected_streaming)) &
    (df["fav_genre"].isin(selected_genres)) &
    (df["hours_per_day"].between(hours_min, hours_max)) &
    (df["music_effects"].isin(selected_effect_values))
]

# Filtro para "While Working" (Si/No)
if selected_while_working:
    while_map = {"Sí": 1, "No": 0}
    selected_values = [while_map[w] for w in selected_while_working]
    filtered_df = filtered_df[filtered_df["while_working"].isin(selected_values)]


# Seccion desplegable para datos generales del estudio (visualizacion del dataset limpio y bonitico):
with st.expander("Ver Datos filtrados", expanded=False):
    # Solo se mostraran las primeros 14 filas 
    preview = filtered_df.head(14)
# Tabla
    st.dataframe(
        preview,
        use_container_width=True,
        hide_index=True
    )

    st.caption(f"Mostrando 15 de {len(filtered_df):,} registros • Total de columnas: {filtered_df.shape[1]}")



# Tabs Principales
tab_inicio, tab_salud, tab_habitos, tab_avanzado = st.tabs([
    "🏠 Inicio",
    "🧠 Salud Mental",
    "🎵 Hábitos Musicales",
    "📊 Análisis Avanzado"
])

# tab_inicio:
with tab_inicio:
    st.subheader("Metricas Principales")                          

    # Creacion de columnas
    col1, col2, col3 = st.columns(3)

    with col1.container(border=True):
        st.metric(
            label="Total de Participantes.",
            value=len(filtered_df)
        )

    with col2.container(border=True):
        improve_pct = (filtered_df["music_effects"] == 1).mean() * 100
        st.metric(
            label="% que dice que la música mejora",
            value=f"{improve_pct:.1f}%",
            help="Porcentaje de participantes que perciben mejora en su bienestar con la música"
        )
    
    with col3.container(border=True):
        score_promedio = filtered_df[["anxiety", "depression", "insomnia", "ocd"]].mean(axis=1).mean()
        st.metric(
            label="Promedio General de Salud Mental",
            value=f"{score_promedio:.2f}",
            help="Promedio combinado de ansiedad, depresión, insomnio y OCD (0-10). Mayor valor = peor salud mental reportada."
        )
    
    st.subheader("Perfil basico de la muestra")
    # Asegurar que haya datos antes de calcular
    if not filtered_df.empty:
        top_service = filtered_df['primary_streaming_service'].mode()[0]
        top_genre = filtered_df['fav_genre'].mode()[0]
        avg_hours = filtered_df['hours_per_day'].mean()

    # Columnas de highlights(cual es laplataforma mas usada en el filtro?)
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        with st.container(border=True):
            st.markdown(f"**🎧 Plataforma Líder**\n\n{top_service}")
    with col_b:
        with st.container(border=True):
            st.markdown(f"**🎸 Género Favorito**\n\n{top_genre}")
    with col_c:
        with st.container(border=True):
            st.markdown(f"**⏰ Promedio de Escucha**\n\n{avg_hours:.1f} horas/día")

# tab_salud
with tab_salud:
    st.subheader("Distribucion de Indicadores de Salud Mental")
    st.markdown("---")
    st.write("Comparación de distribuciones mediante daiagrams de caja")

    # Box plot  
    fig_box = px.box(                          
    filtered_df,
    y=["anxiety", "depression", "insomnia", "ocd"],
    title="Distribución de los Indicadores de Salud Mental - Diagramas de Caja",
    labels={"variable": "Indicador", "value": "Puntuación (0-10)"},
    color_discrete_sequence=["#E3D0EA"]
    )

    fig_box.update_layout(
    height=580,
    xaxis_title="Indicadores de Salud Mental",
    yaxis_title="Puntuación (0-10)",
    showlegend=False,
    title_font_size=20
    )

    st.plotly_chart(fig_box, use_container_width=True)
    
    cols_salud = ["anxiety", "depression", "insomnia", "ocd"]
    # Columnas para ver el cuadro a un lado y el grafico al otro.
    col_grafico, col_tabla = st.columns([3, 2])

    with col_tabla:
        st.write("Medidas de tendencia central y dispersión:")
        stats = filtered_df[cols_salud].describe().round(2)
        
        # Renombrar índices
        stats = stats.rename(index={
            "count": "Cantidad",
            "mean": "Media",
            "std": "Desviación Estándar",
            "min": "Mínimo",
            "25%": "Percentil 25",
            "50%": "Mediana",
            "75%": "Percentil 75",
            "max": "Máximo"
        })

        st.dataframe(stats, use_container_width=True)
    
    with col_grafico:
        # Tema para seaborn
        sb.set_theme(style="whitegrid", palette="muted")
        # Definir variables 
        variables = cols_salud
        # Select box (para elegir la opcion)
        opcion = st.selectbox(
        "Selecciona un indicador para visualizar:", 
        variables,
        format_func=lambda x: x.capitalize())
    
        for col in variables:
            if col == opcion:                    
                fig, ax = plt.subplots(figsize=(8, 5))

                sb.histplot(df[col], bins=11, kde=True, color="orchid", ax=ax) 
                plt.title(f"Análisis de {col}")
                plt.xlim(0, 10)
    
                st.pyplot(fig)
                plt.close(fig)
                break
# tab_habitos
with tab_habitos:
    st.subheader("Relación entre ritmo musical (BPM) y nivel de insomnio")
    st.caption("Analizar si ritmos más acelerados tienen relación con la dificultad para dormir.")

    # Grafico de dispersion intereactivo
    _, col_central, _= st.columns([1, 8, 1])

    with col_central:
        fig = px.scatter(
            filtered_df,
            x="bpm",
            y="insomnia",
            title="Relación entre Ritmo Musical (BPM) y Insomnio",
            labels={
                "bpm": "Ritmo Musical (BPM)",
                "insomnia": "Nivel de Insomnio (0-10)"
            },
            opacity=0.8,
            color_discrete_sequence=["#A33F76"],
            hover_data=["age", "fav_genre", "hours_per_day"]
        )
        fig.update_layout(
        title_font_size=22  ,
        title_font_color="#884572",
        height=500,
    )
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    
    # Tabla cruzada
    tabla = pd.crosstab(
        filtered_df['while_working'], 
        filtered_df['music_effects']
    )
    # diccionarios de mapeo
    map_filas = {0: "No escucha mientras trabaja", 1: "Si escucha mientras trabaja"}
    map_cols = {-1: "Empeora", 0: "Nulo", 1: "Mejora"}

    # Renombramos
    tabla = tabla.rename(index=map_filas, columns=map_cols)
    fig_bar = px.bar(
        tabla,
        title="Impacto de la Música al trabajar",
        labels={"index": "Escucha música mientras trabaja", "value": "Cantidad de personas"},
        color_discrete_sequence=["#DC91AE","#B06D84", "#588F46"],
        text_auto=True
    )
    fig_bar.update_layout(
        title_font_size=22  ,
        title_font_color="#2F7A35",
        height=500,
        xaxis_title="¿Escucha música mientras trabaja?",
        yaxis_title="Cantidad de personas",
        legend_title="Efecto de la música",
        barmode='group'
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    
    st.divider()
    
    # Horas de musica al dia vs Insomnio
    filtered_df["hours_range"] = pd.cut(
    filtered_df["hours_per_day"],
    bins=[0, 1, 3, 5, 8, 24],
    labels=["0-1h", "1-3h", "3-5h", "5-8h", "Más de 8h"]
    )
    
    # Grafico de violin.
    fig_violin_hours = px.violin(
    filtered_df,
    x="hours_range",
    y="insomnia",
    title="Insomnio según Horas de Música al Día",
    box=True,
    points="outliers",
    color_discrete_sequence=["#9D5694"]
    )
    
    fig_violin_hours.update_layout(height=550)
    st.plotly_chart(fig_violin_hours, use_container_width=True)
    
    # Metricas en dos filas
    m1, m2 = st.columns(2)
    m3, m4 = st.columns(2)

    with m1.container(border=True):
        st.metric(" BPM Promedio", f"{filtered_df['bpm'].mean():.0f}")

    with m2.container(border=True):
        st.metric("Horas de música al día", f"{filtered_df['hours_per_day'].mean():.1f} h")

    with m3.container(border=True):
        pct = (filtered_df['while_working'] == 1).mean() * 100
        st.metric(" Escucha música mientras trabaja", f"{pct:.1f}%")

    with m4.container(border=True):
        genre_cols = [col for col in filtered_df.columns if col.startswith('frequency_')]
        if genre_cols:
            avg_genres = (filtered_df[genre_cols] >= 3).sum(axis=1).mean()
            st.metric(" Géneros escuchados frecuentemente", f"{avg_genres:.1f}")

