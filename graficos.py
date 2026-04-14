#
import pandas as pd
import numpy as np
import matplotlib as mp
import matplotlib.pyplot as plt
import seaborn as sb

df = pd.read_csv("limpieza_final_python.csv")

#Objetivo 2: distribución de indicadores de salud mental con media, mediana y RIC

variables = ["Anxiety", "Depression", "Insomnia", "OCD"]

sb.set_theme(style="ticks", palette="muted")

for col in variables:
    plt.figure(figsize=(8, 5))
    sb.histplot(df[col], bins=11, kde=True, color="violet") 
    
    media_val = df[col].mean()
    med_val = df[col].median()
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    
    plt.axvline(media_val, color='red', linestyle='-', linewidth=2, label=f'Media: {media_val:.2f}')
    plt.axvline(med_val, color='blue', linestyle='-', linewidth=2, label=f'Mediana: {med_val:.1f}')
    
    plt.axvline(q1, color='black', linestyle='--', linewidth=1, label=f'Q1: {q1:.1f}')
    plt.axvline(q3, color='black', linestyle='--', linewidth=1, label=f'Q3: {q3:.1f}')
    
    plt.title(f"Análisis de {col}")
    plt.xlim(0, 10)
    plt.xlabel("Puntuación")
    plt.ylabel("Participantes")
    plt.legend()
    plt.savefig(f"graficos_img/hist_{col}.png", dpi=300, bbox_inches='tight')
    plt.show()

# Objetivo 3: comparación de variables mediante boxplot (salud mental)

plt.figure(figsize=(12, 6))
sb.set_theme(style="whitegrid")

sb.boxplot(data=df[variables], palette="Set2")
plt.title('Distribución y Comparación de Indicadores de Salud Mental', fontsize=15)
plt.ylabel('Puntuación', fontsize=12)
plt.xlabel('Indicadores', fontsize=12)
plt.savefig("graficos_img/boxplot_mental.png")
plt.show()

# Comparación de indicadores de salud mental (Ansiedad y Depresión) por género musical favorito

sb.set_theme(style="ticks")
indicadores = ["Anxiety", "Depression"]

for indicador in indicadores:
    plt.figure(figsize=(10, 5))
    sb.boxplot(x="Fav genre", y=indicador, data=df, palette="viridis")
    
    plt.title(f"Distribución de {indicador} por Género Musical", fontsize=14)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7) 
    
    plt.tight_layout()
    plt.savefig(f"graficos_img/box_{indicador.lower()}.png")
    plt.show()

# Objetivo 4: relación entre BPM y perfil general de Salud mental
# Gráfico de embudo 

df['Rango_Salud'] = pd.to_numeric(df['Rango_Salud'], errors='coerce')
orden = [1, 0, -1]
df_resumen = df.groupby('Rango_Salud')['BPM'].mean().reindex(orden).reset_index()

plt.figure(figsize=(12, 7), facecolor='#f8f9fa') 
colores = ["#8DF58D", "#FFFF7A", "#E4160C"] 

max_bpm = df_resumen['BPM'].max()
left_margin = (max_bpm - df_resumen['BPM']) / 2

barras = plt.barh(range(len(df_resumen)), df_resumen['BPM'], 
                  left=left_margin, color=colores, 
                  height=0.7, edgecolor='white', linewidth=2)


for i, valor in enumerate(df_resumen['BPM']):
    if not pd.isna(valor):
        plt.text(max_bpm/2, i, f"{valor:.2f} BPM", 
                 va='center', ha='center', fontsize=12, 
                 color="#1D1D1D")

plt.yticks(range(len(df_resumen)), ['Buena (1)', 'Regular (0)', 'Alarmante (-1)'], 
           fontsize=11, color='#333333')

plt.title("BPM Promedio según Estado General de Salud Mental", 
          fontsize=16, pad=30, fontweight="bold", color='#2C3E50')

plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.gca().spines['bottom'].set_visible(False)
plt.xticks([]) 

plt.gca().invert_yaxis() 
plt.savefig("graficos_img/embudo_bpm.png", dpi=300, bbox_inches='tight', facecolor='#f8f9fa')
plt.show()

#Objetivo 5: relación entre Music Effect y While working

tabla = pd.crosstab(df["While working"], df["Music effects"])
tabla.columns = ['Empeora', 'Nulo', 'Mejora']
tabla.index = ['No trabaja con música', 'Sí trabaja con música']

colores = ["#F77474", "#8CCCF7", "#2ECC71"] 
ax = tabla.plot(kind="bar", figsize=(10, 6), color=colores, edgecolor="white", rot=0)

plt.title("Impacto de la Música al trabajar", fontsize=14, fontweight='bold')
plt.ylabel("Cantidad de personas")
plt.legend(title="Efecto")
plt.savefig("graficos_img/barras_trabajo.png")
plt.show()

# Objetivo 6: comparación de salud mental por edad de los participantes
# Correlación entre edad, salud mental y BPM (variables numéricas)
plt.figure(figsize=(10, 8)) 

sb.heatmap(df[['Age', 'Anxiety', 'Depression', 'OCD', 'Insomnia', 'BPM', 'Hours per day']].corr(), 
           annot=True,       
           vmin=-1,          
           vmax=1,           
           cmap='coolwarm',
           fmt=".2f")        

plt.title("Correlación: Variables Numéricas")
plt.savefig("graficos_img/heatmap_correlacion.png")
plt.show()

# Objetivo 7: exploración entre top 5 géneros (estadística descriptiva)
def calcular_ric(columna):
    q3 = columna.quantile(0.75)
    q1 = columna.quantile(0.25)
    return q3 - q1

top_5 = df['Fav genre'].value_counts().nlargest(5).index
df_top5 = df[df['Fav genre'].isin(top_5)]

indicadores = ["Anxiety", "Depression", "OCD", "Insomnia"]
tabla_robusta = df_top5.groupby('Fav genre')[indicadores].agg(['median', calcular_ric]).round(2)

fig, ax = plt.subplots(figsize=(15, 7))
ax.axis('off')

col_nombres = []
for col in tabla_robusta.columns:
    variable = col[0]
    estadistico = "Me" if col[1] == 'median' else "RIC"
    col_nombres.append(f"{variable} ({estadistico})")

res_tabla = ax.table(
    cellText=tabla_robusta.values, 
    colLabels=col_nombres, 
    rowLabels=tabla_robusta.index, 
    loc='center', 
    cellLoc='center'
)

res_tabla.set_fontsize(10)
res_tabla.scale(1, 2.8)

plt.title("Top 5 Géneros Más Escuchados: Mediana (Me) y Rango Intercuartílico (RIC)", pad=40, weight='bold')
plt.savefig("graficos_img/tabla_final.png", dpi=300, bbox_inches='tight')
plt.show()



