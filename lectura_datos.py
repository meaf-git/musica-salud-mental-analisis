# -*- coding: utf-8 -*-
"""
Created on Sat Feb 28 15:26:34 2026

@author: Principal
"""

#Lectura de datos y limpieza de dataset 

import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib as mp


df = pd.read_csv (r"C:\Users\Principal\Desktop\UNI\COMPUTACIÓN I\musica.csv")

print(df.head(6))

# Tamaño del dataset
print(f"Filas: {df.shape}")
print(f"\nColumnas :{df.columns}")
df.head()

#Removiendo las columnas innecesarias ("Timestamp", "Permissions")

df.drop(columns=["Timestamp", "Permissions"], inplace=True)

#Identificación de las variables, sus tipos, los datos faltantes por columna y el porcentaje de los mismos

print("Tipos de variables")
nombre_fila = df.index[0] 
dict_tipos = df.dtypes.to_dict()
tipos_de_datos = df.dtypes 
print(tipos_de_datos)


print("Datos faltantes por columna")
datos_faltantes =df.isnull().sum()
porcentaje_faltantes = df.isnull().mean() * 100
resumen_nulos = pd.DataFrame({'Total': datos_faltantes, "Porcentaje": porcentaje_faltantes})

print(resumen_nulos)

if (porcentaje_faltantes >= 50.00).any():
    print("\nHay columnas con un exceso de datos faltantes (> 50%).")
else:
    print("\nLa calidad de los datos es aceptable (Ninguna columna supera el 50% de registros nulos).")

#Sustituyendo los valores faltantes para cada columna float (numérica):
#1. Columna "Age":

for i in df.index:
    edad = df.at[i, 'Age']
    # Si es nulo, se salta
    if pd.isna(edad):
        continue
    
    #Verificación de rango y sustitución por mediana 
    if edad > 110 or edad < 0:
        df.at[i, 'Age'] = np.nan

mediana_age = df["Age"].median()
for i in df.index:
    if pd.isna(df.at[i, 'Age']):
       df.at[i, "Age"] = mediana_age

df["Age"]= df["Age"].astype(int) 

#2. Columna "Hours per day":

df.loc[(df["Hours per day"] > 24) | (df["Hours per day"] < 0), "Hours per day"] = np.nan
mediana_hours = df["Hours per day"].median()
df["Hours per day"] = df["Hours per day"].fillna(mediana_hours)

#3. Columna "BPM":
for i in df.index:
    bpm = df.at[i, "BPM"]
    if pd.isna(bpm):
        continue

    if bpm > 500 or bpm < 40:
        df.at[i, "BPM"] = np.nan

mediana_bpm = df["BPM"].median()
for i in df.index:
    if pd.isna(df.at[i, "BPM"]):
        df.at[i, "BPM"] = mediana_bpm


#Para variables cualitativas
#Asignación de valores enteros a las columnas de Frecuencia ("Frequency")

columnas_frecuencia = df.columns[10:26]

dicc_frecuencia = {
    'Very frequently': 4,
    'Sometimes': 3,
    'Rarely': 2,
    'Never': 1
}
for col in columnas_frecuencia:
    df[col] = df[col].replace(dicc_frecuencia)
    df[col] = df[col].astype(int)       
    df[col] = pd.to_numeric(df[col], errors='coerce')   

#Asignación de valores enteros a las columnas con datos booleanos (YES = 1, NO = 0)

rango1 = df.columns[3:6]
rango2 = df.columns[7:9]
datos_dicotomicos = list(rango1) + list(rango2) 

for col in datos_dicotomicos:
    print(f"Analizando columna: {col}")
    moda_col = df[col].mode()[0]
    df[col] = df[col].fillna(moda_col)
    df[col] = df[col].replace({'Yes': 1, 'No': 0})
    df[col] = df[col].astype(int)
       

#Para columna "Music Effects" (Improve = 1, No Effect = 0, Worsen = -1):

moda_me = df['Music effects'].mode()[0]
df['Music effects'] = df['Music effects'].fillna(moda_me)
diccionario_efectos = {
    'Improve': 1,
    'No effect': 0,
    'Worsen': -1
}
df['Music effects'] = df['Music effects'].replace(diccionario_efectos)
df['Music effects'] = pd.to_numeric(df['Music effects'], errors='coerce')
print(df['Music effects'].value_counts())


#Para columna Género Favorito ("Fav Genre"). No tiene vacíos ni registros mal escritos. Únicamente cálculo de moda (Rock).
moda_genre = df["Fav genre"].mode()

#Para columna Servicio de Streaming Principal ("Primary streaming service"). Hay vacíos.

primary_ss_moda = df["Primary streaming service"].mode()[0]    #Spotify
df["Primary streaming service"] = df["Primary streaming service"].fillna(primary_ss_moda)

#Las columnas de salud mental no presentan vacíos.

df.to_csv('limpieza_final_python.csv', index=False)

















               


