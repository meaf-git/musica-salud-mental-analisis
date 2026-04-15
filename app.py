import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib as mp
import matplotlib.pyplot as plt
import seaborn as sb
import random


# Configuracion de la pagina 
st.set_page_config(page_title="Musica y Salud Mental", page_icon="🎵", layout="wide")

# Titulo y descripcion de la app
col_titulo, col_imagen = st.columns([8, 1])
with col_titulo:
    st.header("Análisis estadístico de la Correlación entre Hábitos Auditivos y Perfiles de Salud Mental.")
    st.write("Visualización entre los hábitos de consumo musical y diferentes indicadores de salud mental mediante el uso de técnicas de análisis estadístico.")
with col_imagen:
    st.image("assets/316752.png", width=200)
st.markdown("---")

# Paleta de colores
color_palette = {
    "claro": "#D6BBC0",
    "medio": "#C585B3",
    "principal": "#BC69AA",
    "fuerte": "#AF42AE",
    "oscuro": "#8A2E8F",}


# Carga de Datos

FILE_PATH = "datos_musica_limpios_FINAL.csv"

@st.cache_data
def load_data(path):
    data = pd.read_csv(path)
    return data
df =load_data(FILE_PATH)

# column_labels para que las columnas del dataset sean legibles
column_labels = {
    "age": "Edad",
    "primary_streaming_service":"Servicio de streaming principal",
    "hours_per_day": "Horas de musica al día",
    "while_working": "Escucha música mientras trabaja",
    "instrumentalist": "Toca algun instrumento",
    "composer": "Es compositor/a",
    "fav_genre": "Género musical favorito",
    "exploratory": "Explora nuevos géneros",
    "foreign_languages": "Escucha música en otros idiomas",
    "bpm": "Ritmo musical (BPM)",
    "frequency_classical": "Frecuencia de escucha - Clásica",
    "frequency_country": "Frecuencia de escucha - Country",
    "frequency_edm": "Frecuencia de escucha - EDM",
    "frequency_folk": "Frecuencia de escucha - Folk",
    "frequency_gospel": "Frecuencia de escucha - Gospel",
    "frequency_hip_hop": "Frecuencia de escucha - Hip Hop",
    "frequency_jazz": "Frecuencia de escucha - Jazz",
    "frequency_k_pop": "Frecuencia de escucha - K-Pop",
    "frequency_latin": "Frecuencia de escucha - Latina",
    "frequency_lofi": "Frecuencia de escucha - LoFi",
    "frequency_metal": "Frecuencia de escucha - Metal",
    "frequency_pop": "Frecuencia de escucha - Pop",
    "frequency_r_b": "Frecuencia de escucha - R&B",
    "frequency_rap": "Frecuencia de escucha - Rap",
    "frequency_rock": "Frecuencia de escucha - Rock",
    "frequency_video_game_music": "Frecuencia de escucha - Música de Videojuegos",
    "anxiety": "Ansiedad",
    "depression":"Depresión",
    "insomnia": "Insomnio",
    "ocd": "TOC",
    "music_effects":"Efectos percibido de la Música",
    "total_salud": "Puntaje Total de Salud",
    "rango_salud": "Nivel de Impacto"}

# Para traducir los generos
genero_español = {
    "Latin": "Latina",
    "Rock": "Rock",
    "Video game music": "Música de Videojuegos",
    "Jazz": "Jazz",
    "R&B": "R&B",
    "K pop": "K-Pop",
    "Country": "Country",
    "EDM": "EDM",
    "Hip hop": "Hip Hop",
    "Pop": "Pop",
    "Rap": "Rap",
    "Classical": "Clásica",
    "Metal": "Metal",
    "Folk": "Folk",
    "Lofi": "Lo-Fi",
    "Gospel": "Gospel",}

# Filtros para la interactividad

# Columnas para mover el titulo a un lado y la imagen a otro
col_tit, col_image = st.sidebar.columns([3, 1])
with col_tit:
    st.header("Filtros de Interactividad")
with col_image:
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
    (df["age"] >= age_min) & 
    (df["age"] <= age_max) &
    (df["hours_per_day"].between(hours_min, hours_max))
]

if selected_streaming:
    filtered_df = filtered_df[filtered_df["primary_streaming_service"].isin(selected_streaming)]
if selected_genres:
    filtered_df = filtered_df[filtered_df["fav_genre"].isin(selected_genres)]
if selected_effect_values:
    filtered_df = filtered_df[filtered_df["music_effects"].isin(selected_effect_values)]
if selected_while_working:
    while_map = {"Sí": 1, "No": 0}
    selected_values = [while_map[w] for w in selected_while_working]
    filtered_df = filtered_df[filtered_df["while_working"].isin(selected_values)]

if len(filtered_df) == 0:
    st.warning("⚠️ No se encontraron resultados con los filtros actuales. Prueba a modificar los filtros.")
    filtered_df = df.copy()


# Seccion desplegable para datos generales del estudio (visualizacion del dataset limpio y bonitico):
with st.expander("Ver Datos filtrados", expanded=False):
    # Copia del dataframe filtrado con los nombres legibles
    df_display = filtered_df.copy()
    df_display = df_display.rename(columns=column_labels)
    
    # Mostramos 
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True
    )
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Dataset Limpio",
        data=csv,
        file_name='datos_musica_limpios.csv',
        mime='text/csv',
    )
    
    st.caption(f"**{len(df_display):,} participantes** × **{df_display.shape[1]} columnas**")



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
    col1, col2, col3 = st.columns(3,gap="small")

    with col1:
        st.markdown(f"""
        <div style="background-color: white; 
                padding: 20px; 
                border-radius: 12px; 
                box-shadow: 0 4px 15px rgba(188, 105, 170, 0.12);">
        <p style="margin:0; font-size:14px; color:#666;">Total de Participantes</p>
        <h2 style="margin:8px 0 0 0; color:#AF42AE;">{len(filtered_df):,}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        mejora_pct = (filtered_df["music_effects"] == 1).mean() * 100
        mejora_str = f"{mejora_pct:.1f}".replace(".", ",")
        st.markdown(f"""
        <div style="background-color: white; 
                padding: 20px; 
                border-radius: 12px; 
                box-shadow: 0 4px 15px rgba(175, 66, 174, 0.12);">
        <p style="margin:0; font-size:14px; color:#666;"> % Que presenta una mejoría al escuchar música</p>
        <h2 style="margin:8px 0 0 0; color:#AF42AE;">{mejora_str}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        promedio_salud = filtered_df['total_salud'].mean()
        promedio_str = f"{promedio_salud:.2f}".replace(".", ",")
        st.markdown(f"""
        <div style="background-color: white; 
                padding: 20px; 
                border-radius: 12px; 
                box-shadow: 0 4px 15px rgba(197, 133, 179, 0.12);">
        <p style="margin:0; font-size:14px; color:#666;">Puntaje Medio de Salud Mental</p>
        <h2 style="margin:8px 0 0 0; color:#AF42AE;">{promedio_str}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Highlights (Cosas a destacar)
    
    st.subheader("Perfil básico de la muestra")
    
    
# Asegurar que haya datos antes de calcular
    if not filtered_df.empty:
        top_servicio = filtered_df["primary_streaming_service"].mode()[0]
        top_genero = filtered_df["fav_genre"].mode()[0]
        horas_promedio = filtered_df["hours_per_day"].mean()

    # Columnas de highlights(cual es laplataforma mas usada en el filtro?)
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown(f"""
                <div style="background-color: white; 
                padding: 20px; 
                border-radius: 12px; 
                box-shadow: 0 4px 15px rgba(188, 105, 170, 0.12);
                <p style="margin:0; font-size:18px;">🎧 Plataforma Líder</p>
                <h3 style="margin:8px 0 0 0; color:#AF42AE;">{top_servicio}</h3>
                </div>
                """, unsafe_allow_html=True)
        with col_b:
            st.markdown(f"""
                <div style="background-color: white; 
                padding: 20px; 
                border-radius: 12px; 
                box-shadow: 0 4px 15px rgba(175, 66, 174, 0.12);
                <p style="margin:0; font-size:18px;">🎸 Género Favorito</p>
                <h3 style="margin:8px 0 0 0; color:#AF42AE;">{top_genero}</h3>
                </div>
                """, unsafe_allow_html=True)
        with col_c:
            horas_str = f"{horas_promedio:.1f}".replace(".", ",")
    
            st.markdown(f"""
                <div style="background-color: white; 
                padding: 20px; 
                border-radius: 12px; 
                box-shadow: 0 4px 15px rgba(197, 133, 179, 0.12);
                <p style="margin:0; font-size:18px;">⏰ Promedio de Escucha</p>
                <h3 style="margin:8px 0 0 0; color:#AF42AE;">{horas_str} horas/día</h3>
                </div>
                """, unsafe_allow_html=True)
    
# Boton para datos curiosos de la muestra
    # Botón personalizado con CSS
    boton = f"""
        <style>
        div.stButton > button {{
        background-color: #BC69AA;
        color: white;
        font-size: 18px;
        font-weight: 600;
        padding: 14px 24px;
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 12px rgba(188, 105, 170, 0.25);
        transition: all 0.3s ease;
    }}
    div.stButton > button:hover {{
        background-color: #AF42AE;
        box-shadow: 0 6px 16px rgba(175, 66, 174, 0.35);
        transform: translateY(-2px);
    }}
    </style>
"""
    st.markdown(boton, unsafe_allow_html=True)
    if st.button("Generar Dato Curioso", use_container_width=True):
        # Lista de datos curiosos basados en los datos filtrados
        datos_curiosos= [
            f"En este grupo, la mayoría prefiere usar **{top_servicio}**.",
            f"El género **{top_genero}** es el mas escuchado de estos filtros.",
            f"En promedio, se escuchan **{horas_promedio:.1f} horas** de música al día aquí.",
            "¿Sabías que la música puede reducir el estrés?",
            "Los usuarios que escuchan música clásica suelen reportar mayor enfoque."
        ]
        
        # Se selecciona uno al azar y se muestra como mensaje temporal
        dato_elegido = random.choice(datos_curiosos)
        st.toast(dato_elegido, icon="💡")
        st.markdown(f"**Dato del momento:** *{dato_elegido}*")

# Cita de Schopenhauer, A. (2005).
st.markdown("""
---
> “La música no es, como todas las otras artes, una representación de las ideas o grados de la objetivación de la voluntad, sino la **expresión directa de la voluntad misma**; 
>
> lo cual explica su acción inmediata sobre la voluntad, es decir, sobre los sentimientos, las pasiones y las emociones del oyente, de modo que rápidamente los exalta o los modifica.”
>
> — **Schopenhauer, A. (2005).** *El mundo como voluntad y representación (Vol. 1).*
---
""")

# tab_salud
with tab_salud:
    st.subheader("Distribución de Indicadores de Salud Mental")
    st.markdown("---")
    st.write("Comparación de distribuciones mediante daiagramas de caja")

    # Box plot  
    fig_box = px.box(                          
    filtered_df,
    y=["anxiety", "depression", "insomnia", "ocd"],
    title="Distribución de los Indicadores de Salud Mental",
    labels={"variable": "Indicador", "value": "Puntuación (0-10)"},
    color_discrete_sequence=["#8A2E8F"]
    )
   
    fig_box.update_layout(
    height=580,
    xaxis_title="Indicadores de Salud Mental",
    yaxis_title="Puntuación (0-10)",
    showlegend=False,
    title_font_size=20
    )

    st.plotly_chart(fig_box, use_container_width=True)

# Diccionario
    traducciones = {
    "anxiety": "Ansiedad",
    "depression": "Depresión",
    "insomnia": "Insomnio",
    "ocd": "TOC"
    }
    
    cols_salud = ["anxiety", "depression", "insomnia", "ocd"]

    with st.container(border=True):
        
        st.write("Medidas de tendencia central y dispersión:")
        stats = filtered_df[cols_salud].describe().round(2)
        stats = stats.rename(columns=traducciones)
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
        stats = stats.astype(str).replace(r'\.', ',', regex=True)
        st.dataframe(stats, use_container_width=True)

        st.divider()
    
        # Tema para seaborn
        sb.set_theme(style="whitegrid", palette="muted")
        # Definir variables 
        variables = cols_salud
        # Select box (para elegir la opcion)
        opcion = st.selectbox(
        "Selecciona un indicador para visualizar:", 
        variables,
        format_func=lambda x: traducciones.get(x))

        # st.columns para ajustar el tamaño del grafico
        col_izq, col_centro, col_der = st.columns([1, 2, 1])

        with col_centro:
            for col in variables:
                if col == opcion:                    
                    fig, ax = plt.subplots(figsize=(7, 6))

                    # traduccion del eje x
                    plt.xlabel(traducciones[opcion], fontsize=10)
                    plt.ylabel("Frecuencia", fontsize=10)
                    # Titulo mas pequeño
                    plt.title(f"Análisis de {traducciones[opcion]}", fontsize=12)
                    plt.xlim(0, 10)

                    sb.histplot(filtered_df[col], bins=11, kde=True, color="orchid", ax=ax) 
                    plt.title(f"Análisis de {traducciones[opcion]}")
                    plt.xlim(0, 10)
    
                    st.pyplot(fig)
                    plt.close(fig)
                    break


# tab_habitos
with tab_habitos:

    # Grafico de embudo intereactivo
    _, col_central, _= st.columns([1, 8, 1])

    with col_central:
        df_resumen = (filtered_df.groupby("rango_salud")["bpm"].mean().reset_index())
        # Nombres 
        nombre_rango = {1: "Buena (1)",0: "Regular (0)",-1: "Alarmante (-1)"}
        df_resumen["Rango"] = df_resumen["rango_salud"].map(nombre_rango)

        # Ordenar de mejor a peor salud
        orden = ["Buena (1)", "Regular (0)", "Alarmante (-1)"]
        df_resumen["Rango"] = pd.Categorical(df_resumen["Rango"], categories=orden, ordered=True)
        df_resumen = df_resumen.sort_values("Rango")

        #Grafico de embudo
        fig = px.funnel(
            df_resumen,
            x="bpm",
            y="Rango",
            orientation="h",
            title="BPM Promedio según Estado General de Salud Mental",
            labels={"bpm": "Ritmo Musical Promedio (BPM)",
                    "Rango": ""},
            color="Rango",
            color_discrete_sequence=["#E0A8E6", "#C89EC4", "#9B6A9E"],
            text="bpm")
        
        fig.update_traces(
            texttemplate="%{text:.1f} BPM",
            textposition="inside")
        
        fig.update_layout(
            height=520,
            title_font_size=20,
            margin=dict(l=40, r=30, t=70, b=40),
            xaxis_title="BPM Promedio",
            yaxis_title="",
            showlegend=False,
            plot_bgcolor="rgba(0,0,0,0)")
        
        st.plotly_chart(fig, use_container_width=True)
        with st.popover("¿Qué significa esto?"):
            st.markdown("""
                **Ritmo y Bienestar**
                * **Estabilidad:** El BPM (latidos por minuto) promedio se mantiene muy similar entre los tres grupos (121-126 BPM).
                * **Interpretación:** Esto sugiere que el **ritmo** por sí solo no es un predictor determinante del estado de salud mental; personas en estado "Alarmante" y "Bueno" escuchan ritmos similares.
                """)

    # Tabla cruzada    
    tabla = pd.crosstab(
        filtered_df["while_working"], 
        filtered_df["music_effects"]
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
        color_discrete_sequence=["#E0A8E6","#D0A3BF", "#9D52A1"],
        text_auto=True
    )
    fig_bar.update_layout(
        title_font_size=22,
        height=500,
        xaxis_title="¿Escucha música mientras trabaja?",
        yaxis_title="Cantidad de personas",
        legend_title="Efecto de la música",
        barmode='group'
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    with st.popover("¿Qué significa esto?"):
        st.markdown("""
            **Productividad Sonora**
            * **Efecto Positivo:** Existe un consenso masivo: la gran mayoría de quienes escuchan música mientras trabajan reportan que esta **mejora** su desempeño.
            * **Riesgo Mínimo:** Muy pocos participantes indican que la música "Empeora" su situación, lo que valida el uso de herramientas auditivas en entornos académicos o laborales.
            * **Dato Curioso:** Incluso quienes no escuchan música frecuentemente al trabajar, reconocen en su mayoría que tiene un potencial efecto positivo.
            """)
    
    st.divider()
    
    # Horas de musica al dia vs Insomnio
    filtered_df["Rango de horas"] = pd.cut(
    filtered_df["hours_per_day"],
    bins=[0, 1, 3, 5, 8, 24],
    labels=["0-1h", "1-3h", "3-5h", "5-8h", "Más de 8h"]
    )
    
    # Grafico de violin.
    fig_violin_hours = px.violin(
    filtered_df,
    x="Rango de horas",
    y="insomnia",
    title="Insomnio según Horas de Música al Día",
    box=True,
    points="outliers",
    color_discrete_sequence=["#7F569D"]
    )
    
    fig_violin_hours.update_layout(height=550)
    st.plotly_chart(fig_violin_hours, use_container_width=True)
    with st.popover("¿Qué significa esto?"):
        st.markdown("""
        **Distribución del Insomnio**
        * **Densidad:** El ancho del "violín" representa dónde se concentra la mayoría de las personas. Un violín más ancho en la parte superior indica que en ese grupo el insomnio es más frecuente.
        * **Tendencia:** Observamos que quienes escuchan **más de 8 horas** de música tienden a mostrar una mayor dispersión y medianas ligeramente más altas de insomnio.
        """)

#tab_avanzado
with tab_avanzado:
    st.subheader("Analisis Avanzado")
    st.caption("Correlaciones y asociaciones entre la musica y la salud mental")
    
    # Heatmap
    st.write("Correlaciones entre variables")
    cols_interes = ["anxiety", "depression", "insomnia", "ocd", "bpm", 
                    "hours_per_day", "age"]
    
    # Calculamos la matriz (especificamos pearson por si acaso) y redondeo a 2 decimales
    corr_matrix = filtered_df[cols_interes].corr(method="pearson").round(3)
    # Renombrar 
    corr_matrix = corr_matrix.rename(columns=column_labels, index=column_labels)
    # Escala de colores personalizada
    escala = [
        [0.0,"#311B92"],    #Para correlaciones negativas (-1)
        [0.5, "#F3E5F5"],   # Color neutro para el cero
        [1.0, "#BC69AA"] # Para correlaciones positivas (+1)
        ]
    fig_heatmap = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale=escala,
        title="Matriz de Correlaciones de Pearson",
        labels=dict(color="Coeficiente"),
        color_continuous_midpoint=0,
        )
    
    fig_heatmap.update_layout(height=600, title_font_size=20)
    coloraxis_colorbar=dict(title="Correlación")
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    with st.popover("¿Qué significa esto?"):
        st.markdown("""
            **Relaciones entre Variables**
            * **Correlación Fuerte:** La relación más clara se da entre **Ansiedad y Depresión (0.52)**, lo cual es estadísticamente esperado en estudios psicológicos.
            * **Correlación Débil:** La **Edad** tiene una correlación negativa casi nula con el TOC o el Insomnio, sugiriendo que estos indicadores afectan por igual a jóvenes y adultos en esta muestra.
            * **Lectura:** Cuanto más cerca esté el número de **1**, más crecen las variables juntas. Si está cerca de **0**, no hay relación lineal clara.
            """)
        
    # Grafico de caja
    
    # Grafico de caja por rangos
    # Rangos
    bins = [0, 2, 4, 6, 8, 12, 25]
    labels = ["0-2 horas", "2-4 horas", "4-6 horas", "6-8 horas","8-12 horas", "Más de 12 horas"]
    
    filtered_df["horas_rango"] = pd.cut(filtered_df["hours_per_day"], bins=bins, labels=labels, right=False)

    # Boxplot por rangos
    fig_horas = px.box(
        filtered_df,
        x="horas_rango",
        y="total_salud",
        title="Puntaje de Salud Mental según Horas de Música al Día",
        labels={
        "horas_rango": "Horas de música al día",
        "total_salud": "Índice de Carga Sintomática Acumulada (ICSA)"    },
        color="horas_rango",
        color_discrete_sequence=[              
        "#D6BBC0",   # 0-2 horas
        "#C585B3",   # 2-4 horas
        "#BC69AA",   # 4-6 horas
        "#AF42AE",   # 6-8 horas
        "#9B6A9E",   # 8-12 horas     
        "#8A2E8F"    # Más de 12 horas 
    ]
)
    fig_horas.update_xaxes(categoryorder="array", categoryarray=labels)
    fig_horas.update_layout(
        height=580,
        xaxis_tickangle=30,
        title_font_size=20,
        showlegend=False)

    st.plotly_chart(fig_horas, use_container_width=True)

    with st.popover("¿Qué significa esto?"):
            st.markdown("""
                **Carga Sintomática Acumulada**
                * **Crecimiento:** Se observa una tendencia levemente ascendente: a mayor número de horas de música, la mediana del índice ICSA tiende a subir.
                * **Outliers:** El grupo de **0-2 horas** presenta un valor atípico muy alto, lo que indica que existen casos aislados con alta carga sintomática a pesar del bajo consumo.
                * **Cuartiles:** El desplazamiento hacia arriba de las cajas en los grupos de **8-12 horas** sugiere una mayor prevalencia de síntomas en consumidores intensivos.
                """)

    # Comparacion de Ansiedad y Depresion por Genero musical favorito
    st.subheader("Comparacion de Ansiedad y Depresion por Género Musical Favorito")
    indicadores = ["anxiety","depression"]

    for indicador in indicadores: 
        nombre_indicador = column_labels.get(indicador, indicador.capitalize())
        filtered_df["fav_genre_es"]= filtered_df["fav_genre"].map(genero_español).fillna(filtered_df["fav_genre"]) 

        fig = px.box(
            filtered_df, 
            x="fav_genre_es", 
            y=indicador,
            title=f"Distribución de {nombre_indicador} por Género Musical Favorito",
            labels={"fav_genre_es": "Género Musical Favorito", indicador: nombre_indicador + " (0-10)"},
            color="fav_genre_es",
            color_discrete_sequence=[
                "#D6BBC0",   
                "#C585B3",   
                "#BC69AA",   
                "#AF42AE",   
                "#9B6A9E",       
                "#8A2E8F"
                ],
            points="outliers")
        
        fig.update_layout(
            height=550,
            xaxis_tickangle=45,
            title_font_size=18,
            yaxis_title=nombre_indicador + "(Escala 0-10)",
            showlegend=False,
            plot_bgcolor="#F8F1F4")
        
        st.plotly_chart(fig, use_container_width=True)
        with st.popover("¿Qué significa esto?"):
            st.markdown("""
                **Análisis por Género**
                * **Variabilidad:** Géneros como el **Rock** y el **K-Pop** muestran rangos intercuartílicos más amplios en ansiedad, indicando audiencias con estados de ánimo muy diversos.
                * **Niveles Bajos:** Géneros como la música **Latina** o el **Gospel** presentan medianas de depresión y ansiedad ligeramente más bajas en comparación con el promedio.
                * **Nota:** No implica causalidad; es decir, escuchar un género no causa la ansiedad, sino que personas con ciertos niveles de ansiedad podrían preferir ciertos géneros.
                """)
        
                    


