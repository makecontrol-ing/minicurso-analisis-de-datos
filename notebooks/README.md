# Los notebooks del taller

| Archivo | Para qué es | Ábrelo aquí |
|---|---|---|
| [`taller_estudiante.ipynb`](taller_estudiante.ipynb) | el tuyo para la clase: cada vez que veas `___` va un método (son 45) | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/makecontrol-ing/minicurso-analisis-de-datos/blob/main/notebooks/taller_estudiante.ipynb) |
| [`taller_solucion.ipynb`](taller_solucion.ipynb) | la solución completa, ya ejecutada y con las gráficas, para que revises tu trabajo | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/makecontrol-ing/minicurso-analisis-de-datos/blob/main/notebooks/taller_solucion.ipynb) |
| [`requirements.txt`](requirements.txt) | lo que necesitas instalar si prefieres trabajar en tu computador y no en Colab | |

## Cómo lo vamos a usar en clase

1. Abre tu notebook en Colab y sube [`domicilios_sucio.csv`](../datos/domicilios_sucio.csv) al panel de archivos (el ícono de carpeta de la izquierda).
2. Ejecuta las celdas de arriba hacia abajo con **Shift + Enter**. Cuando veas `___`, escribe el método que te muestro en la diapositiva.
3. Si te atrasas o Colab se reinicia, no pasa nada. Al comienzo de «Análisis gráfico» hay un **punto de control**: subes [`domicilios_limpio.csv`](../datos/domicilios_limpio.csv) y sigues con las gráficas.

## Por qué el código se ve así

Lo escribí para que se **lea fácil**, no para que sea corto. Cada celda hace una sola cosa y
tiene de una a tres líneas. Solo usamos pandas, sin funciones propias, sin bucles y sin
trucos. Las explicaciones están en las celdas de texto, no metidas entre el código.

Todos los pasos siguen el mismo ritmo: primero un texto que dice **Paso N**, cuál es el
problema y qué método vamos a usar. Después **miramos** el problema, lo **corregimos** y
**comprobamos** que quedó bien. Lo probé en la versión de pandas de Colab (2.2) y en la más
nueva (3.x), y en las dos corre igual, sin errores ni advertencias.

## Si quieres regenerarlos

Los dos notebooks salen del mismo script,
[`fuentes/construir_notebooks.py`](../fuentes/construir_notebooks.py). Desde la raíz:

```sh
python fuentes/construir_notebooks.py --ejecutar
```

Con `--ejecutar` corre la solución, la guarda solo si no hubo errores ni advertencias y
actualiza `datos/domicilios_limpio.csv`. Si lo corres sin `--ejecutar`, la solución queda sin
resultados.
