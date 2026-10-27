"""Regenera todas las figuras del README:  python .github/readme/generador/generar_todo.py"""
import os
import runpy
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
for nombre in ["banner.py", "ruta.py", "gif_presentacion.py", "destacados.py"]:
    runpy.run_path(os.path.join(AQUI, nombre), run_name="__main__")
