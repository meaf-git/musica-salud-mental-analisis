##
import pandas as pd
import numpy as np
import matplotlib as mp
import matplotlib.pyplot as plt
import seaborn as sb

df = pd.read_csv("limpieza_final_python.csv")

variables = ["Anxiety", "Depression", "Insomnia", "OCD"]
print(df[variables].describe())
print(df[variables].median())

# Primeros gráficos: distribución de indicadores de salud mental 

sb.set_theme(style="whitegrid", palette="muted")
for col in variables:
    sb.histplot(df[col], bins=11, kde=True, color="orchid") 
    plt.title(f"Análisis de {col}")
    plt.xlim(0, 10)
    plt.show()

# Para objetivo 4: relación entre BPM e Insomnio (diagrama de dispersión)

sb.set_theme(style="whitegrid")
plt.figure(figsize=(10, 6))
sb.scatterplot(data=df, x='BPM', y='Insomnia', alpha=0.5, color="orchid")
plt.title('Relación entre Ritmo Musical (BPM) e Insomnio')
plt.xlabel('Ritmo (BPM)')
plt.ylabel('Nivel de Insomnio (0-10)')
plt.show()

# Relación entre Horas al día e Insomnio 

sb.set_theme(style="whitegrid")
plt.figure(figsize=(10, 6))
sb.scatterplot(data=df, x='Hours per day', y='Insomnia', alpha=0.5, color="indianred")
plt.title('Relación entre Horas al día e Insomnio')
plt.xlabel('Horas al día')
plt.ylabel('Nivel de Insomnio (0-10)')
plt.show()

# comparación de indicadores de salud mental (Ansiedad y Depresión) por género musical favorito

df.groupby("Fav genre")[["Anxiety","Depression"]].mean()
sb.boxplot(x="Fav genre", y="Anxiety", data=df)
plt.xticks(rotation=45)
plt.show()

sb.boxplot(x="Fav genre", y="Depression", data=df)
plt.xticks(rotation=45)
plt.show()

# Para objetivo 5: relación entre Music Effect y While working

tabla = pd.crosstab(df["While working"], df["Music effects"])
tabla.columns = ['Empeora', 'Nulo', 'Mejora']
tabla.index = ['No trabaja con música', 'Sí trabaja con música']

colores = ["#F77474", "#8CCCF7", "#2ECC71"] 
ax = tabla.plot(kind="bar", figsize=(10, 6), color=colores, edgecolor="white", rot=0)

plt.title("Impacto de la Música al trabajar", fontsize=14, fontweight='bold')
plt.ylabel("Cantidad de personas")
plt.legend(title="Efecto")
plt.show()


