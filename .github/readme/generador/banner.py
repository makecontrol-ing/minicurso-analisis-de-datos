"""Banner: título a la izquierda, ventas por mes de la base limpia a la derecha."""
import os
import pandas as pd
import matplotlib.pyplot as plt
from estilo import RAIZ, SALIDA, VERDE, DORADO, CREMA

df = pd.read_csv(os.path.join(RAIZ, "datos", "domicilios_limpio.csv"))
ventas = df.groupby("mes")["total"].sum() / 1e6

fig = plt.figure(figsize=(16, 4.4), facecolor=VERDE)
ax = fig.add_axes([0, 0, 1, 1], facecolor=VERDE)
ax.set_axis_off(); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.plot([0.04, 0.96], [0.93, 0.93], color=DORADO, lw=1.2)
ax.plot([0.80, 0.96], [0.93, 0.93], color=DORADO, lw=6)
ax.text(0.04, 0.70, "Introducción al análisis", color="white", fontsize=36, fontweight="bold", va="center")
ax.text(0.04, 0.52, "de datos con Python", color="white", fontsize=36, fontweight="bold", va="center")
ax.plot([0.04, 0.46], [0.39, 0.39], color=DORADO, lw=3)
ax.text(0.04, 0.29, "De una base de datos con errores a gráficas que responden preguntas",
        color=CREMA, fontsize=15, va="center")
ax.text(0.04, 0.16, "Minicurso de 1 h 30 min  ·  Andrés David Galeano Quintero  ·  pandas y matplotlib  ·  2026",
        color="#cfe3d8", fontsize=13, va="center")

ins = fig.add_axes([0.62, 0.20, 0.34, 0.62], facecolor=VERDE)
ins.plot(ventas.index, ventas.values, color=DORADO, lw=3, marker="o")
ins.set_xticks(range(1, 13)); ins.set_xlim(0.6, 12.4)
for s in ["left", "bottom"]:
    ins.spines[s].set_color("#9fcbb5")
ins.tick_params(colors="#cfe3d8", labelsize=11)
ins.set_xlabel("mes de 2025", color="#cfe3d8", fontsize=11)
ins.set_ylabel("ventas (millones de pesos)", color="#cfe3d8", fontsize=11)
ins.set_title("«Pan de Datos»: ventas por mes, ya con la base limpia", color="white", fontsize=12, loc="left")

fig.savefig(os.path.join(SALIDA, "banner.png"), dpi=150, facecolor=VERDE)
print("banner.png")
