##
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

# Objetivo 4: relación entre BPM e Insomnio 
# Cálculo de Coeficiente de Correlación de Pearson:
correlacion = df['BPM'].corr(df['Insomnia'])
print("Coeficiente de correlación:", correlacion)

plt.figure(figsize=(9, 5))
plt.scatter(df['BPM'], df['Insomnia'], alpha=0.5, color="violet")
m, b = np.polyfit(df['BPM'], df['Insomnia'], 1)
plt.plot(df['BPM'], m*df['BPM'] + b, color="blue", label=f"Tendencia (r={correlacion:.2f})")
plt.title("Relación entre Ritmo Musical (BPM) e Insomnio")
plt.xlabel("BPM")
plt.ylabel("Nivel de Insomnio")
plt.legend()
plt.savefig("graficos_img/dispersion_bpm.png")
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
# Correlación entre edad y salud mental 
plt.figure(figsize=(8, 6))
sb.heatmap(df[['Age', 'Anxiety', 'Depression', "OCD", "Insomnia"]].corr(), annot=True, cmap="magma")
plt.title("Correlación: Edad vs Salud Mental")
plt.savefig("graficos_img/heatmap_correlacion.png")
plt.show()

# Objetivo 7: exploración entre top 5 géneros (estadística descriptiva)
top_5 = df['Fav genre'].value_counts().nlargest(5).index
df_top5 = df[df['Fav genre'].isin(top_5)]

indicadores = ["Anxiety", "Depression", "OCD", "Insomnia"]
tabla = df_top5.groupby('Fav genre')[indicadores].agg(['mean', 'var']).round(2)

fig, ax = plt.subplots(figsize=(14, 6)) 
ax.axis('off')

res_tabla = ax.table(cellText=tabla.values, 
                     colLabels=[f"{c[0]} ({'x̄' if c[1]=='mean' else 'S²'})" for c in tabla.columns], 
                     rowLabels=tabla.index, 
                     loc='center', 
                     cellLoc='center')

res_tabla.auto_set_font_size(False)
res_tabla.set_fontsize(10) 
res_tabla.scale(1, 2.5) 
plt.title("Estadísticos Descriptivos (Top 5 Géneros): Media (x̄) y Varianza (S²)", pad=30, weight='bold')
plt.savefig("graficos_img/tabla_top5.png", dpi=300, bbox_inches='tight')
plt.show()




