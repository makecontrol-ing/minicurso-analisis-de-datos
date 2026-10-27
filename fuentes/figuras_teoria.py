from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from matplotlib.ticker import FuncFormatter

VERDE = "#06784F"
VERDE_OSCURO = "#044E34"
DORADO = "#FFB93E"
GRIS = "#9A9AA0"
TEXTO = "#29272D"
TEXTO_2 = "#626268"
REJILLA = "#E6E6E9"
TARJETA = "#F0F5F2"

SALIDA = Path(__file__).resolve().parent / "figuras"
SALIDA.mkdir(exist_ok=True)

plt.rcParams.update({
    "font.family": "Calibri",
    "font.size": 12,
    "text.color": TEXTO,
    "axes.edgecolor": GRIS,
    "axes.linewidth": 0.9,
    "axes.labelcolor": TEXTO,
    "axes.labelsize": 12.5,
    "axes.titlesize": 13.5,
    "axes.titlecolor": TEXTO,
    "axes.titleweight": "bold",
    "axes.titlelocation": "left",
    "axes.titlepad": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.unicode_minus": False,
    "axes.axisbelow": True,
    "axes.facecolor": "white",
    "figure.facecolor": "white",
    "xtick.color": GRIS,
    "ytick.color": GRIS,
    "xtick.labelcolor": TEXTO_2,
    "ytick.labelcolor": TEXTO_2,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "savefig.dpi": 200,
    "savefig.facecolor": "white",
})

FLECHA = {"arrowstyle": "-", "color": TEXTO_2, "lw": 0.9, "shrinkA": 2, "shrinkB": 2}


def coma(valor, posicion=None):
    return f"{valor:g}".replace(".", ",")


def porcentaje(valor, posicion=None):
    return f"{valor:.0f} %"


def rejilla(ax, eje):
    ax.grid(axis=eje, color=REJILLA, linewidth=0.8)


def guardar(fig, nombre):
    fig.savefig(SALIDA / nombre, dpi=200)
    plt.close(fig)


def barras():
    medios = ["Carro", "Bicicleta", "Moto", "A pie", "Bus", "Metro"]
    estudiantes = [12, 15, 22, 31, 52, 68]
    fig, ax = plt.subplots(figsize=(5.2, 3.2), layout="constrained")
    ax.barh(medios, estudiantes, color=VERDE, height=0.62)
    for posicion, valor in enumerate(estudiantes):
        ax.text(valor + 1.2, posicion, str(valor), va="center", color=TEXTO, fontsize=12)
    ax.set_title("¿Cómo llegan 200 estudiantes al campus?")
    ax.set_xlabel("Número de estudiantes")
    ax.set_xlim(0, 78)
    ax.tick_params(axis="y", length=0, labelcolor=TEXTO)
    rejilla(ax, "x")
    guardar(fig, "teoria_barras.png")


def lineas():
    semanas = list(range(1, 17))
    horas = [5, 6, 7, 8, 9, 12, 17, 21, 10, 9, 10, 12, 14, 18, 25, 23]
    fig, ax = plt.subplots(figsize=(5.2, 3.2), layout="constrained")
    ax.plot(semanas, horas, color=VERDE, linewidth=2, marker="o", markersize=5.5,
            markerfacecolor=VERDE, markeredgecolor="white", markeredgewidth=1.2,
            solid_joinstyle="round", solid_capstyle="round")
    ax.plot([8, 15], [21, 25], linestyle="none", marker="o", markersize=9,
            markerfacecolor=DORADO, markeredgecolor=VERDE_OSCURO, markeredgewidth=1.2)
    ax.annotate("Parciales", xy=(8, 21), xytext=(8, 25.6), ha="center", fontsize=12,
                color=TEXTO, arrowprops=FLECHA)
    ax.annotate("Finales", xy=(15, 25), xytext=(15, 28.4), ha="center", fontsize=12,
                color=TEXTO, arrowprops=FLECHA)
    ax.set_title("Horas de estudio por semana en un semestre")
    ax.set_xlabel("Semana del semestre")
    ax.set_ylabel("Horas de estudio")
    ax.set_xticks([1, 4, 8, 12, 16])
    ax.set_xlim(0.4, 16.6)
    ax.set_ylim(0, 30)
    rejilla(ax, "y")
    guardar(fig, "teoria_lineas.png")


def histograma():
    generador = np.random.default_rng(7)
    minutos = generador.gamma(shape=4, scale=11, size=300).clip(5, 125)
    fig, ax = plt.subplots(figsize=(5.2, 3.2), layout="constrained")
    ax.hist(minutos, bins=range(0, 121, 10), color=VERDE, edgecolor="white", linewidth=1.5)
    ax.plot([90, 90, 110, 110], [6, 8.5, 8.5, 6], color=TEXTO_2, linewidth=1)
    ax.text(100, 11, f"Solo {(minutos > 90).sum()} tardan\nmás de 90 min", ha="center", va="bottom", fontsize=12,
            color=TEXTO)
    ax.set_title("Tiempo de viaje al campus de 300 estudiantes")
    ax.set_xlabel("Minutos de viaje (intervalos de 10 min)")
    ax.set_ylabel("Estudiantes")
    ax.set_xticks(range(0, 121, 20))
    ax.set_xlim(0, 120)
    rejilla(ax, "y")
    guardar(fig, "teoria_histograma.png")


def dispersion():
    generador = np.random.default_rng(11)
    horas = generador.uniform(0.5, 12, 60)
    nota = (1.8 + 0.22 * horas + generador.normal(0, 0.45, 60)).clip(0.5, 5)
    fig, ax = plt.subplots(figsize=(5.2, 3.2), layout="constrained")
    ax.scatter(horas, nota, s=42, color=VERDE, edgecolor="white", linewidth=1.2, zorder=3)
    ax.text(0.4, 4.75, "Tendencia: a más horas,\nmejor nota en promedio", fontsize=12,
            color=TEXTO_2, va="top")
    ax.set_title("Horas de estudio y nota del parcial (60 estudiantes)")
    ax.set_xlabel("Horas de estudio antes del parcial")
    ax.set_ylabel("Nota del parcial")
    ax.set_xticks(range(0, 13, 2))
    ax.set_yticks(range(0, 6))
    ax.set_xlim(0, 12.5)
    ax.set_ylim(0, 5.2)
    rejilla(ax, "both")
    guardar(fig, "teoria_dispersion.png")


def caja():
    minutos = np.array([3, 5, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 12, 13, 13, 14, 14,
                        15, 16, 16, 17, 18, 19, 21, 24, 27, 36, 42])
    q1, mediana, q3 = np.percentile(minutos, [25, 50, 75])
    ric = q3 - q1
    limite = q3 + 1.5 * ric
    bigote_bajo = minutos[minutos >= q1 - 1.5 * ric].min()
    bigote_alto = minutos[minutos <= limite].max()
    atipicos = minutos[minutos > limite]
    fig, ax = plt.subplots(figsize=(5.2, 3.2), layout="constrained")
    ax.add_patch(Rectangle((q1, -0.28), ric, 0.56, facecolor=TARJETA, edgecolor=VERDE,
                           linewidth=1.8, zorder=2))
    ax.plot([mediana, mediana], [-0.28, 0.28], color=VERDE_OSCURO, linewidth=3.2, zorder=3)
    ax.plot([bigote_bajo, q1], [0, 0], color=VERDE, linewidth=1.8)
    ax.plot([q3, bigote_alto], [0, 0], color=VERDE, linewidth=1.8)
    ax.plot([bigote_bajo, bigote_bajo], [-0.14, 0.14], color=VERDE, linewidth=1.8)
    ax.plot([bigote_alto, bigote_alto], [-0.14, 0.14], color=VERDE, linewidth=1.8)
    ax.scatter(atipicos, [0] * len(atipicos), s=70, color=DORADO, edgecolor=VERDE_OSCURO,
               linewidth=1.2, zorder=4)
    ax.plot([limite, limite], [-0.55, 0.95], color=GRIS, linewidth=1, linestyle=(0, (3, 2)))
    ax.text(limite + 0.6, 0.95, "Límite:\nQ3 + 1,5 × RIC", fontsize=12, color=TEXTO_2,
            va="top", ha="left")
    ax.annotate(f"Q1 = {coma(q1)}", xy=(q1, 0.3), xytext=(q1 - 0.4, 0.72), ha="right",
                fontsize=12, color=TEXTO, arrowprops=FLECHA)
    ax.annotate(f"Q3 = {coma(q3)}", xy=(q3, 0.3), xytext=(q3 + 0.4, 0.72), ha="left",
                fontsize=12, color=TEXTO, arrowprops=FLECHA)
    ax.annotate(f"Mediana = {coma(mediana)}", xy=(mediana, 0.3), xytext=(mediana, 1.3),
                ha="center", fontsize=12, color=TEXTO, fontweight="bold", arrowprops=FLECHA)
    ax.plot([q1, q1, q3, q3], [-0.42, -0.5, -0.5, -0.42], color=TEXTO_2, linewidth=1)
    ax.text((q1 + q3) / 2, -0.62, f"RIC = Q3 − Q1 = {coma(ric)}", ha="center", va="top",
            fontsize=12, color=TEXTO)
    ax.annotate("Bigote", xy=(bigote_bajo, -0.16), xytext=(bigote_bajo, -0.62), ha="center",
                va="top", fontsize=12, color=TEXTO, arrowprops=FLECHA)
    ax.annotate("Bigote", xy=(bigote_alto, -0.16), xytext=(bigote_alto - 2.5, -0.62),
                ha="center", va="top", fontsize=12, color=TEXTO, arrowprops=FLECHA)
    centro_atipicos = atipicos.mean()
    for valor in atipicos:
        ax.annotate("", xy=(valor, -0.17), xytext=(centro_atipicos, -0.6), arrowprops=FLECHA)
    ax.text(centro_atipicos, -0.62, "Atípicos", ha="center", va="top", fontsize=12, color=TEXTO)
    ax.set_title("Anatomía de una caja: minutos de fila en la cafetería")
    ax.set_xlabel("Minutos en la fila (31 almuerzos)")
    ax.set_xlim(0, 46)
    ax.set_ylim(-1.05, 1.6)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xticks(range(0, 46, 5))
    guardar(fig, "teoria_caja.png")


def enganosa():
    grupos = ["Grupo A", "Grupo B"]
    aprobacion = [78, 82]
    fig, (izquierda, derecha) = plt.subplots(1, 2, figsize=(8.5, 3.0), layout="constrained")
    for ax, minimo, maximo in [(izquierda, 76, 83), (derecha, 0, 100)]:
        ax.bar(grupos, aprobacion, color=VERDE, width=0.5)
        for posicion, valor in enumerate(aprobacion):
            ax.text(posicion, valor + (maximo - minimo) * 0.025, f"{valor} %", ha="center",
                    va="bottom", fontsize=12.5, color=TEXTO)
        ax.set_ylim(minimo, maximo)
        ax.yaxis.set_major_formatter(FuncFormatter(porcentaje))
        ax.set_ylabel("Aprobaron Cálculo I")
        ax.tick_params(axis="x", length=0, labelcolor=TEXTO, labelsize=12.5)
        rejilla(ax, "y")
    izquierda.set_title("Eje desde 76 %: B parece el triple de A")
    derecha.set_title("Eje desde 0 %: la diferencia es de 4 puntos")
    izquierda.set_yticks(range(76, 84, 1))
    derecha.set_yticks(range(0, 101, 20))
    guardar(fig, "teoria_enganosa.png")


barras()
lineas()
histograma()
dispersion()
caja()
enganosa()
print("Figuras guardadas en fuentes/figuras:", ", ".join(sorted(p.name for p in SALIDA.glob("teoria_*.png"))))
