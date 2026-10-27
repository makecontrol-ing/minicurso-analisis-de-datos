"""Tres gráficas del análisis, tal como aparecen en la presentación."""
import os
import matplotlib.pyplot as plt
from matplotlib.image import imread
from estilo import RAIZ, SALIDA, VERDE, GRIS

paneles = [
    ("taller_linea.png", "Diciembre vende 2,6 veces lo que vende febrero"),
    ("taller_histograma.png", "Los clientes forman dos grupos de edad"),
    ("taller_caja.png", "Bello es el municipio más lento"),
]
fig, ejes = plt.subplots(1, 3, figsize=(16, 3.9))
for ax, (archivo, titulo) in zip(ejes, paneles):
    ax.imshow(imread(os.path.join(RAIZ, "fuentes", "figuras", archivo)))
    ax.set_axis_off()
fig.text(0.01, 0.01, "Datos sintéticos de la panadería ficticia «Pan de Datos» (1.180 pedidos limpios de 2025).",
         fontsize=10.5, color=GRIS)
fig.tight_layout(rect=(0, 0.05, 1, 0.90))
for ax, (_, titulo) in zip(ejes, paneles):
    fig.text(ax.get_position().x0 + 0.01, 0.95, titulo, fontsize=14, color=VERDE, fontweight="bold", va="center")
fig.savefig(os.path.join(SALIDA, "destacados.png"), dpi=150, facecolor="white")
print("destacados.png")
