"""Recorrido animado por algunas diapositivas de la presentación."""
import os
import pymupdf
from PIL import Image
from estilo import RAIZ, SALIDA

DIAPOSITIVAS = [1, 4, 8, 13, 14, 21, 24, 28, 31, 32, 35, 37]
pdf = pymupdf.open(os.path.join(RAIZ, "presentacion", "Minicurso_Analisis_de_Datos.pdf"))
cuadros = []
for n in DIAPOSITIVAS:
    pix = pdf[n - 1].get_pixmap(dpi=96)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    cuadros.append(img.resize((900, round(900 * pix.height / pix.width)), Image.LANCZOS))
cuadros[0].save(os.path.join(SALIDA, "presentacion_portada.png"))
paleta = [c.convert("P", palette=Image.ADAPTIVE, colors=128) for c in cuadros]
paleta[0].save(os.path.join(SALIDA, "presentacion.gif"), save_all=True, append_images=paleta[1:],
               duration=2200, loop=0, optimize=True)
print("presentacion.gif")
