"""Ruta del curso: los cinco bloques de la clase con sus tiempos."""
import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from estilo import SALIDA, VERDE, DORADO, TINTA, GRIS, TARJETA

bloques = [
    ("1", "Por qué analizar", "Para qué sirve, preguntas,\nevidencia y el ciclo", "0:00 – 0:12"),
    ("2", "Tipos de gráficas", "Barras, líneas, histograma,\ndispersión y caja", "0:12 – 0:30"),
    ("3", "Taller ETL", "Extraer, corregir 7 errores\ny cargar la base limpia", "0:30 – 1:05"),
    ("4", "Análisis gráfico", "Cinco preguntas de negocio,\ncinco gráficas", "1:05 – 1:22"),
    ("5", "Cierre", "Resumen de métodos y lista\nde chequeo", "1:22 – 1:30"),
]
fig, ax = plt.subplots(figsize=(16, 3.6))
ax.set_axis_off(); ax.set_xlim(0, 100); ax.set_ylim(0, 30)
ancho, paso = 17, 20
for i, (n, titulo, texto, tiempo) in enumerate(bloques):
    x = 1.5 + i * paso
    practica = n in ("3", "4")
    fondo = VERDE if practica else TARJETA
    color_t = "white" if practica else VERDE
    color_c = "#e8f2ec" if practica else TINTA
    ax.add_patch(FancyBboxPatch((x, 3), ancho, 22, boxstyle="round,pad=0.4,rounding_size=1.2",
                                fc=fondo, ec="none"))
    ax.text(x + 1.5, 21, n, fontsize=26, fontweight="bold", color=DORADO, va="center")
    ax.text(x + 4.5, 21, titulo, fontsize=14.5, fontweight="bold", color=color_t, va="center")
    ax.text(x + 1.5, 13, texto, fontsize=12, color=color_c, va="center", linespacing=1.4)
    ax.text(x + 1.5, 5.8, tiempo, fontsize=11.5, color=DORADO if practica else GRIS, va="center")
    if i < len(bloques) - 1:
        ax.annotate("", xy=(x + paso - 0.6, 14), xytext=(x + ancho + 1.0, 14),
                    arrowprops=dict(arrowstyle="-|>", color=GRIS, lw=1.6))
ax.text(1.5, 28.5, "Bloques en verde: los estudiantes escriben código en Google Colab",
        fontsize=11.5, color=GRIS, va="center")
fig.savefig(os.path.join(SALIDA, "ruta.png"), dpi=150, bbox_inches="tight", facecolor="white")
print("ruta.png")
