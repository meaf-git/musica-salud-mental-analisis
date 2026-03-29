import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import os

# Configuracion de la pagina 
st.set_page_config(page_title="Musica y Salud Mental", page_icon="🎵", layout="wide")

# Titulo y metricas
st.title("Análisis estadístico de la Correlación entre Hábitos Auditivos y Perfiles de Salud Mental 🧠")
st.write("Visualizacion entre los hábitos de consumo musical y diferentes indicadores de salud mental mediante el uso de técnicas de análisis estadístico.")
st.markdown("---")

# Ruta del archivo
FILE_PATH = "datos_musica_limpios_FINAL.csv"

@st.cache_data
def load_data(path):
    data = pd.read_csv(path)
    cols_salud = ['anxiety', 'depression', 'insomnia', 'ocd']
    for col in cols_salud:
        data[col] = pd.to_numeric(data[col], errors='coerce')
    return data

try:
    df =load_data(FILE_PATH)
except Exception as e:
    st.error(f"Error al cargar datos: {e}")
    st.stop()
