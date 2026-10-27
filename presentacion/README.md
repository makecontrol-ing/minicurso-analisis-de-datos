# La presentación

**[Introducción al análisis de datos con Python (PDF, 38 diapositivas)](Minicurso_Analisis_de_Datos.pdf)**
&nbsp;·&nbsp; si quieres la versión editable, con mis notas: [`Minicurso_Analisis_de_Datos.pptx`](Minicurso_Analisis_de_Datos.pptx)

Así está organizada la clase:

| Bloque | Minutos | Diapositivas | De qué hablamos |
|---|---|:-:|---|
| Bienvenida | 0:00–0:02 | 1–2 | la portada y el plan de la clase |
| 1 · Por qué y para qué | 0:02–0:12 | 3–7 | para qué sirve analizar datos, casos reales, por qué limpiar importa, el ciclo del análisis y los tipos de variables |
| 2 · Tipos de gráficas | 0:12–0:30 | 8–15 | qué gráfica responde cada pregunta: barras, líneas, histograma, dispersión y caja y bigotes; las gráficas que engañan y seis preguntas para leer cualquier gráfica |
| 3 · Taller | 0:30–1:05 | 16–29 | conocemos a «Pan de Datos», preparamos Colab y corregimos los errores uno por uno |
| 4 · Análisis | 1:05–1:22 | 30–35 | cinco preguntas, cinco gráficas y qué nos dice cada una |
| 5 · Cierre | 1:22–1:30 | 36–38 | resumen de lo que usamos, lista de chequeo y dónde seguir aprendiendo |

En las diapositivas del taller vas a ver el problema, ejemplos de los datos sucios, el código
de la celda con el **método clave en verde** (es el que va en el `___` de tu notebook) y lo
que te debe dar.

## Para quien vaya a dictar la clase

Si vas a usar esta presentación, abre el `.pptx`: en las **notas del orador** dejé, para cada
diapositiva, el minuto en que debería ir, qué decir, qué escribir, qué deben ver los
estudiantes, el error que casi siempre aparece y qué hacer si el grupo se atrasa o Colab falla.

Antes de la clase, cambia el marcador `[enlace del taller]` de las diapositivas 2, 19 y 36 por
el enlace donde los estudiantes van a descargar los archivos. Tiene que tener máximo 60
caracteres, así que sirve uno acortado. Ponlo en `ENLACE_TALLER`, al comienzo de
[`fuentes/construir_presentacion.py`](../fuentes/construir_presentacion.py), y vuelve a construir
la presentación:

```sh
python fuentes/construir_presentacion.py                         # arma el .pptx desde fuentes/contenido/*.json
powershell -ExecutionPolicy Bypass -File fuentes/exportar.ps1    # lo pasa a PDF (necesita PowerPoint en Windows)
python fuentes/renderizar.py                                     # saca una imagen de cada diapositiva para revisarlas
```

Todo el texto y las notas de cada diapositiva están en
[`fuentes/contenido/teoria.json`](../fuentes/contenido/teoria.json) y
[`fuentes/contenido/taller.json`](../fuentes/contenido/taller.json), por si quieres cambiar algo.

El diseño (el verde UNAL, la línea dorada y el pie de la Facultad de Minas) sigue el estilo de
las presentaciones de la Universidad Nacional de Colombia, Sede Medellín.
