"""Colores y rutas compartidos por las figuras del README."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
SALIDA = os.path.abspath(os.path.join(AQUI, ".."))

VERDE, VERDE_OSCURO, DORADO = "#06784F", "#044E34", "#FFB93E"
TINTA, GRIS, TARJETA, CREMA = "#29272D", "#626268", "#F0F5F2", "#F7F5F2"

plt.rcParams.update({
    "font.family": "Calibri", "font.size": 12,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#9A9AA0", "xtick.color": GRIS, "ytick.color": GRIS,
})
