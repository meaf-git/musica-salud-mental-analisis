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
    "insomnia": "Insomnia",
    "ocd": "TOC",
    "music_effects":"Efectos percibido de la Música",
    "total_salud": "Puntaje Total de Salud",
    "rango_salud": "Nivel de Impacto"}

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
        <p style="margin:0; font-size:14px; color:#666;">% que dice que la música mejora</p>
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
        <p style="margin:0; font-size:14px; color:#666;">Promedio General de Salud Mental</p>
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
    st.write("Comparación de distribuciones mediante daiagrams de caja")

    # Box plot  
    fig_box = px.box(                          
    filtered_df,
    y=["anxiety", "depression", "insomnia", "ocd"],
    title="Distribución de los Indicadores de Salud Mental - Diagramas de Caja",
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
    st.subheader("Relación entre ritmo musical (BPM) y nivel de insomnio")
    st.caption("Analizar si ritmos más acelerados tienen relación con la dificultad para dormir.")

    # Grafico de dispersion intereactivo
    _, col_central, _= st.columns([1, 8, 1])

    with col_central:
        # Grafico de embudo
        filtered_df['rango_salud'] = pd.to_numeric(filtered_df['rango_salud'], errors='coerce')
    
        orden = [1, 0, -1]
        df_resumen = (filtered_df.groupby('rango_salud')['bpm']
                  .mean()
                  .reindex(orden)
                  .reset_index())
    
        # Nombres legibles
        nombre_rango = {1: "Buena Salud Mental (1)", 
                    0: "Regular (0)", 
                    -1: "Alarmante (-1)"}
    
        df_resumen['Rango'] = df_resumen['rango_salud'].map(nombre_rango)
    
        # gráfico de embudo
        fig = px.bar(
            df_resumen,
            x="bpm",
            y="Rango",
            orientation="h",
            title="BPM Promedio según Estado General de Salud Mental",
            labels={"bpm": "Ritmo Musical Promedio (BPM)", "Rango": ""},
            color="Rango",
            color_discrete_sequence=["#C585B3", "#D0A3BF", "#9D52A1"],
            text="bpm"
    )
        # Ajustes para que se vea como embudo
        fig.update_traces(texttemplate="%{text:.1f} BPM", textposition="inside")
    
        fig.update_layout(
            height=520,
            title_font_size=20,
            xaxis_title="BPM Promedio",
            yaxis_title="",
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)'
        )

        # Ordenar 
        fig.update_yaxes(categoryorder='array', 
                        categoryarray=["Alarmante (-1)", "Regular (0)", "Buena Salud Mental (1)"])

        st.plotly_chart(fig, use_container_width=True)
    
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
        color_discrete_sequence=["#AF42AE","#BC69AA", "#9D52A1"],
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

#tab_avanzado
with tab_avanzado:
    st.subheader("Analisis Avanzado")
    st.caption("Correlaciones y asociaciones entre la musica y la salud mental")
    
    # Heatmap
    st.write("Correlaciones entre variables")
    cols_interes = ["anxiety", "depression", "insomnia", "ocd", "bpm", 
                    "hours_per_day", "age"]
    corr_matrix = filtered_df[cols_interes].corr()
    custom_colors = [
    "#3A1C36",   
    "#9B71B2",
    "#E3D0EA", 
    "#A56495"  
    ]
    
    fig_heatmap = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale=custom_colors,
        title="Matriz de Correlaciones"
    )
    fig_heatmap.update_layout(height=600, title_font_size=20)
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    with st.popover("¿Qué significa esto?"):
        st.markdown("Guía Rápida")
        st.info("Los valores cercanos a **1** indican una relación fuerte, mientras que los cercanos a **0** indican que no hay relación clara.")
        st.write("En este gráfico, los tonos más claros representan las conexiones más importantes entre variables.")

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
        "total_salud": "Suma Total de Salud Mental (Ansiedad + Depresión + Insomnio + TOC)"},
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
    
    fig_horas.update_layout(
        height=580,
        xaxis_tickangle=30,
        title_font_size=20)

    st.plotly_chart(fig_horas, use_container_width=True)


# Grafico de dispersion para edad vs salud mental
    st.subheader("Edad vs Promedio de Salud Mental")

    fig_edad = px.scatter(
        filtered_df,
        x="age",
        y="total_salud",
        color=filtered_df["music_effects"].astype(str),
        size="hours_per_day",
        title="Edad vs Promedio de Salud Mental",
        labels={
            "age": "Edad",
            "total_salud": "Promedio de Salud Mental (Suma 0-40)",
            "music_effects": "Efecto de la música"},
        opacity=0.78,
        color_discrete_map={
            "-1": "#AF42AE", # Empeora
            "0": "#8A2E8F", # Nulo
            "1": "#BC69AA"}) # Mejora 
    
    fig_edad.update_layout(height=620)
    st.plotly_chart(fig_edad, use_container_width=True)

    with st.popover("¿Qué significa esto?"):
        st.markdown("""
                - **Eje X (horizontal)**: Representa la **edad** de los participantes.
                - **Eje Y (vertical)**: Representa el **Promedio de Salud Mental** (suma de ansiedad, depresión, insomnio y TOC).
                - **Cada punto**: Es un participante.
                - **Tamaño del punto**: Indica cuántas **horas de música** escucha al día (a mayor punto = más horas).
                - **Color de los puntos**: Representa el **efecto percibido de la música**:
                - Morado oscuro → Empeora
                - Morado claro → Nulo
                - Rosado → Mejora""")

# Grafico de dispersion ritmo musical vs salud mental
    fig_bpm = px.scatter(
        filtered_df,
        x="bpm",
        y="total_salud",
        color= filtered_df["music_effects"].astype(str),                
        size="hours_per_day",                     
        title="Ritmo Musical (BPM) vs Promedio de Salud Mental",
        labels={
            "bpm": "Ritmo Musical (BPM)",
            "total_salud": "Promedio de Salud Mental (Suma 0-40)",
            "music_effects": "Efecto de la música"},
        opacity=0.75,
        color_discrete_map={
            "-1": "#AF42AE", # Empeora
            "0": "#8A2E8F", # Nulo
            "1": "#BC69AA"}) # Mejora 
    
    fig_bpm.update_layout(height=620)
    st.plotly_chart(fig_bpm, use_container_width=True)

    with st.popover("¿Qué significa esto?"):
        st.markdown("""
                - **Eje X (horizontal)**: Representa el **ritmo musical en BPM** (latidos por minuto).
                - **Eje Y (vertical)**: Representa el **Promedio de Salud Mental** (suma de ansiedad, depresión, insomnio y TOC).
                - **Cada punto**: Es un participante.
                - **Tamaño del punto**: Indica cuántas **horas de música** escucha al día (a mayor punto = más horas).
                - **Color de los puntos**: Representa el **efecto percibido de la música**:
                - Morado oscuro → Empeora
                - Morado claro → Nulo
                - Rosado → Mejora""")


