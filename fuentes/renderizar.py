import sys
from pathlib import Path

import pymupdf

from construir_presentacion import ENLACE_TALLER, MARCADOR_ENLACE

FUENTES = Path(__file__).resolve().parent
RAIZ = FUENTES.parent
PDF = RAIZ / 'presentacion' / 'Minicurso_Analisis_de_Datos.pdf'
CARPETA = FUENTES / 'revision' / 'render'
DPI = 110
PASOS = 'construir_presentacion.py, exportar.ps1 y renderizar.py'


def paginas_con(textos, buscado):
    clave = ''.join(buscado.split())
    return ', '.join(str(n) for n, texto in enumerate(textos, start=1) if clave in texto)


def revisar_enlace(textos):
    enlace = ENLACE_TALLER.strip()
    pendientes = paginas_con(textos, MARCADOR_ENLACE)
    if pendientes and not enlace:
        print(f'PENDIENTE: las diapositivas {pendientes} muestran «{MARCADOR_ENLACE}». Pon el enlace corto en '
              f'ENLACE_TALLER (construir_presentacion.py) y vuelve a correr {PASOS}.')
    elif pendientes:
        print(f'PENDIENTE: ENLACE_TALLER ya tiene valor, pero las diapositivas {pendientes} del PDF todavía muestran '
              f'«{MARCADOR_ENLACE}». Vuelve a correr {PASOS}.')
    elif enlace and paginas_con(textos, enlace):
        print(f'Enlace del taller ({enlace}) en las diapositivas {paginas_con(textos, enlace)}.')
    elif enlace:
        print(f'PENDIENTE: el PDF no muestra el enlace de ENLACE_TALLER ({enlace}). Vuelve a correr {PASOS}.')


def main():
    pdf = Path(sys.argv[1]) if len(sys.argv) > 1 else PDF
    CARPETA.mkdir(parents=True, exist_ok=True)
    for viejo in CARPETA.glob('diapo_*.png'):
        viejo.unlink()
    with pymupdf.open(pdf) as doc:
        for numero, pagina in enumerate(doc, start=1):
            pagina.get_pixmap(dpi=DPI).save(CARPETA / f'diapo_{numero:02d}.png')
        textos = [''.join(pagina.get_text().split()) for pagina in doc]
    print(f'{len(textos)} páginas renderizadas a {DPI} dpi en {CARPETA}')
    revisar_enlace(textos)


if __name__ == '__main__':
    main()
