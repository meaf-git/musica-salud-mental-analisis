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
    print("\nLa calidad de los datos es aceptable (Ninguna columna supera el 50% de nulos).")

#Sustituyendo los valores faltantes para cada columna float (numérica):
#1. Columna "Age":

for i in df.index:
    edad = df.at[i, 'Age']
    # Si es nulo, se salta
    if pd.isna(edad):
        continue
    
    #Verificación de rango y sustitución por mediana de NaN
    if edad > 110 or edad < 0:
        df.at[i, 'Age'] = np.nan

mediana_age = df["Age"].median()
for i in df.index:
    if pd.isna(df.at[i, 'Age']):
       df.at[i, "Age"] = mediana_age
    

print(mediana_age)
print(df["Age"].head(14)) #Borrar más adelante 


#2. Columna "Hours per day":
for i in df.index:
    horas = df.at[i, "Hours per day"]
    if pd.isna(horas):
        continue 

    if horas > 24 or horas < 0:
        df.at[i, "Hours per day"] = np.nan

mediana_hours = df["Hours per day"].median()
for i in df.index:
    if pd.isna(df.at[i, "Hours per day"]):
        df.at[i, "Hours per day"] = mediana_hours

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


#Una vez listas las variables float, se procede con las variables cuantitativas ordinales 
#Como no hay datos vacíos, simplemente se calculan las medidas de tendencia pertinentes 

moda_anx = df["Anxiety"].mode()
media_anx = df["Anxiety"].mean()
mediana_anx = df["Anxiety"].median()
moda_dep = df["Depression"].mode()
media_dep = df["Depression"].mean()
mediana_dep = df["Depression"].median()
moda_ins = df["Insomnia"].mode()
media_ins = df["Insomnia"].mean()
mediana_ins = df["Insomnia"].median()
moda_ocd = df["OCD"].mode()
media_ocd =df["OCD"].mean()
mediana_ocd = df["OCD"].median()

#Para variables cualitativas
#Asignación de valores enteros a las columnas de Frecuencia ("Frequency")

columnas_frecuencia = df.columns[11:27]
print(columnas_frecuencia) ###

for col in columnas_frecuencia:
    print(f"Analizando columna: {col}")
    for i in df.index:
        frecuencia = df.at[i, col]
        if frecuencia == 'Very frequently':
            df.at[i, col] = 4
        elif frecuencia == 'Sometimes':
            df.at[i, col] = 3
        elif frecuencia == 'Rarely':
            df.at[i, col] = 2
        elif frecuencia == 'Never':
            df.at[i, col] = 1
            
    df[col] = pd.to_numeric(df[col], errors='coerce')        

#Asignación de valores enteros a las columnas con datos booleanos (YES NO)

rango1 = df.columns[4:7]
rango2 = df.columns[8:10]
datos_dicotomicos = list(rango1) + list(rango2)

for col in datos_dicotomicos:
    print(f"Analizando columna: {col}")
    for i in df.index:
        frecuencia = df.at[i, col]
        if frecuencia == 'Yes':
            df.at[i, col] = 1
        elif frecuencia == 'No':
            df.at[i, col] = 0
            
    df[col] = pd.to_numeric(df[col], errors='coerce') 

#Para columna "Music Effects":
for i in df.index:
    music_efects = df.at[i, 'Music effects']
    
    if pd.isna(music_efects):
        continue
    
    if music_efects == 'No effect':
        df.at[i, 'Music effects'] = 0
    elif music_efects == 'Improve':
        df.at[i, 'Music effects'] = 1
        
    df['Music effects'] = pd.to_numeric(df['Music effects'], errors='coerce')


#Para columna Género Favorito ("Fav Genre"). Como no hay datos faltantes, simplemente se calcula la moda

moda_genre = df["Fav genre"].mode()
print(moda_genre)









               


