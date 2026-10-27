import contextlib
import io
import os
import shutil
import sys
import tempfile
import warnings
from pathlib import Path

import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

from construir_notebooks import CELDAS, CSV, solucion

warnings.simplefilter('error', FutureWarning)
warnings.simplefilter('error', DeprecationWarning)
for nombre in ['SettingWithCopyWarning', 'ChainedAssignmentError']:
    if hasattr(pd.errors, nombre):
        warnings.simplefilter('error', getattr(pd.errors, nombre))

FIGURAS = Path(__file__).resolve().parent / 'figuras'
GRAFICAS = ['barras', 'linea', 'histograma', 'dispersion', 'caja', 'reto']

ANCHO_FIGURA = 6.1
ALTO_SEGUN_LINEAS = {1: 3.75, 2: 3.48, 3: 3.2}

GRIS = '#9A9AA0'
TEXTO = '#29272D'
TEXTO_2 = '#626268'
REJILLA = '#E6E6E9'

plt.rcParams.update({
    'font.family': 'Calibri',
    'font.size': 14,
    'text.color': TEXTO,
    'figure.figsize': (ANCHO_FIGURA, 3.2),
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.edgecolor': GRIS,
    'axes.linewidth': 0.9,
    'axes.labelcolor': TEXTO,
    'axes.labelsize': 14.5,
    'axes.titlesize': 15,
    'axes.titlecolor': TEXTO,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.unicode_minus': False,
    'axes.axisbelow': True,
    'xtick.color': GRIS,
    'ytick.color': GRIS,
    'xtick.labelcolor': TEXTO_2,
    'ytick.labelcolor': TEXTO_2,
    'xtick.labelsize': 14,
    'ytick.labelsize': 14,
    'grid.color': REJILLA,
    'grid.linewidth': 0.8,
    'lines.linewidth': 2,
    'savefig.dpi': 200,
    'savefig.facecolor': 'white',
})


def main():
    FIGURAS.mkdir(exist_ok=True)
    carpeta = Path(tempfile.mkdtemp(prefix='figuras_taller_'))
    shutil.copy(CSV, carpeta / CSV.name)
    inicio = os.getcwd()
    os.chdir(carpeta)
    entorno = {}
    guardadas = []
    try:
        for celda in CELDAS:
            if celda[0] != 'code':
                continue
            clave = celda[2] if len(celda) > 2 else None
            plt.close('all')
            lineas = len(solucion(celda[1]).splitlines())
            plt.rcParams['figure.figsize'] = (ANCHO_FIGURA, ALTO_SEGUN_LINEAS[min(lineas, 3)])
            with contextlib.redirect_stdout(io.StringIO()):
                exec(solucion(celda[1]), entorno)
            if clave in GRAFICAS:
                figura = plt.gcf()
                if clave == 'caja':
                    figura.suptitle('').set_visible(False)
                figura.tight_layout()
                ruta = FIGURAS / f'taller_{clave}.png'
                figura.savefig(ruta, dpi=200)
                guardadas.append(ruta)
        plt.close('all')
    finally:
        os.chdir(inicio)
        shutil.rmtree(carpeta, ignore_errors=True)
    filas, columnas = entorno['df'].shape
    print(f'pandas {pd.__version__}: base limpia de {filas} filas y {columnas} columnas')
    for ruta in guardadas:
        print(f'  {ruta.relative_to(FIGURAS.parent)}')


if __name__ == '__main__':
    main()
