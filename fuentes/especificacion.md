# Especificación — Minicurso «Introducción al análisis de datos con Python»

Documento rector para todo el equipo. Si algo no está aquí, decide con sensatez y
regístralo en tu informe final. Idioma de todo el contenido: **español de Colombia**
(coma decimal en textos: «3,5 km»; punto de miles: «1.234 pedidos»).

## 1. Contexto y público

- Una sola clase de **1 h 30 min**. La da Andrés David Galeano Quintero (estudiante de
  la UNAL, Facultad de Minas, Sede Medellín) a **otros estudiantes**, principiantes en
  análisis de datos.
- Los estudiantes **siguen cada paso en su computador** (Google Colab), mientras
  Andrés proyecta la presentación. En cada paso la diapositiva **les muestra el método
  o función exacta** que deben escribir; ellos completan el hueco en su notebook.
- **Requisito central del usuario: lo más simple posible en estructura de
  programación**, por el tiempo. Reglas duras para TODO el código del taller:
  - Nada de funciones propias (`def`), clases, `lambda`, bucles `for/while`,
    comprensiones de listas, `apply`, `np.where`, `.loc/.iloc`, `try/except`.
  - Una idea por celda; 1 a 3 líneas por celda. Cadenas de métodos de máximo 3
    eslabones (`df['x'].str.strip().str.title()` está bien).
  - Solo `pandas` y `matplotlib` (pandas `.plot`). Sin seaborn, sin numpy explícito.
  - Variables con nombres en español y simples (`df`, `df_limpio` no: siempre `df`).
  - **Sin comentarios `#` dentro de las celdas de código** (regla del usuario: el
    código entregado va sin comentarios). Toda explicación va en celdas Markdown.
  - Debe correr idéntico en **pandas 2.2 (Colab)** y **pandas 3.x**, sin warnings
    molestos (FutureWarning, SettingWithCopyWarning, etc.).

## 2. Agenda (90 min) — la presentación sigue esta estructura

| Bloque | Tiempo | Contenido |
|---|---|---|
| 1. Por qué y para qué | 0:00–0:12 | Qué es analizar datos, para qué sirve (ejemplos), por qué limpiar importa, el ciclo pregunta → ETL → análisis → comunicar, tipos de variables |
| 2. Tipos de gráficas | 0:12–0:30 | Pregunta → gráfica; barras, líneas, histograma, dispersión, caja y bigotes (cada una: qué pregunta responde, cómo se lee, error típico); gráficas que engañan; lista para leer una gráfica |
| 3. Taller ETL | 0:30–1:05 | Presentar el caso y la base; abrir Colab y subir el archivo (3 min); Extraer → Transformar (7 errores) → Cargar |
| 4. Análisis gráfico | 1:05–1:22 | 5 gráficas sobre la base limpia, cada una responde una pregunta de negocio; lectura guiada |
| 5. Cierre | 1:22–1:30 | Resumen de métodos, lista de chequeo de limpieza, preguntas |

Presentación: ~32–38 diapositivas. Cada diapositiva lleva **notas del orador** con el
minuto aproximado (p. ej. «[0:14 – 0:17]») y qué decir / qué hacer.

## 3. El caso: base de datos con errores

**Empresa ficticia:** «Pan de Datos», panadería con servicio a domicilio en el Valle de
Aburrá. **Datos sintéticos creados para el curso** (decirlo en la diapositiva del caso).
Cada fila = un pedido a domicilio durante **2025** (enero–diciembre).

Archivo sucio: `datos/domicilios_sucio.csv` — separador `;`, decimal `,`, UTF-8.
Generado de forma determinista (semilla fija) por `fuentes/generar_datos.py`.
Tamaño objetivo: ~1.250 filas sucias → ~1.150–1.200 limpias.

### Columnas (encabezado sucio → nombre limpio)

| Encabezado en el CSV | Nombre limpio | Contenido |
|---|---|---|
| `ID Pedido` | `id_pedido` | entero único por pedido (los duplicados lo repiten) |
| ` Fecha` (con espacio adelante) | `fecha` | texto `dd/mm/aaaa` |
| `Municipio ` (espacio atrás) | `municipio` | Medellín, Bello, Itagüí, Envigado, Sabaneta |
| `PRODUCTO` | `producto` | 8 productos, siempre bien escritos: Pan de bono, Buñuelo, Almojábana, Croissant, Torta de chocolate, Sándwich, Café, Jugo natural |
| `Cantidad` | `cantidad` | entero 1–6 |
| `Precio Unitario` | `precio_unitario` | **texto** con signo y punto de miles: `$3.500` (algunos sin `$`) |
| `Metodo Pago` | `metodo_pago` | Efectivo, Nequi, Tarjeta, Daviplata (con mayúsculas/minúsculas mezcladas y faltantes) |
| `Distancia KM` | `distancia_km` | decimal con coma en el CSV (`2,5`) |
| `Tiempo Entrega` | `tiempo_entrega` | minutos, entero |
| `Edad Cliente` | `edad_cliente` | entero, con faltantes |
| `Calificacion` | `calificacion` | 1–5 entero |

Transformación de encabezados, en UNA línea:
`df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')`
→ debe producir exactamente los nombres limpios de la tabla.

### Patrones reales que la base debe mostrar (para que las gráficas digan algo)

- **Línea (ventas por mes):** estacionalidad clara: pico en diciembre, subida en
  junio–julio (vacaciones), valle en febrero. Que se note sin ambigüedad.
- **Barras (pedidos por producto):** un líder claro (Pan de bono), un producto
  rezagado claro (Torta de chocolate o Croissant).
- **Histograma (edad):** distribución **bimodal**: estudiantes (~19–25) y familias
  (~38–48). Rango plausible 15–75.
- **Dispersión (distancia vs tiempo de entrega):** relación positiva clara
  (≈ 10 min + 4 min/km + ruido), distancias 0,5–12 km.
- **Caja (tiempo de entrega por municipio):** un municipio claramente más lento y
  con más dispersión (Bello), con algunos atípicos legítimos (no errores).
- Opcional para reto: calificación baja cuando el tiempo de entrega es alto.

### Errores que se siembran (en este orden de corrección en el taller)

| # | Paso | Error sembrado | Diagnóstico (método) | Corrección (método) |
|---|---|---|---|---|
| E | Extraer | CSV con `;` y coma decimal: `pd.read_csv` sin parámetros da UNA sola columna | `df.head()`, `df.shape` | `pd.read_csv('domicilios_sucio.csv', sep=';', decimal=',')` |
| 1 | Nombres de columnas | espacios, mayúsculas, espacios internos | `df.columns` | `.str.strip().str.lower().str.replace(' ', '_')` |
| 2 | Duplicados | ~40 filas exactamente repetidas | `df.duplicated().sum()` | `df = df.drop_duplicates()` |
| 3 | Texto inconsistente | municipio: `Medellín`, `medellin`, `MEDELLIN`, ` Medellín `, `Itagui`, `itagui`, `BELLO `, `envigado`, `SABANETA`…; metodo_pago: `efectivo`, `EFECTIVO`, `nequi`… | `df['municipio'].value_counts()` | `.str.strip().str.title()` y luego `.replace({'Medellin': 'Medellín', 'Itagui': 'Itagüí'})` |
| 4 | Números guardados como texto | `precio_unitario` = `$3.500` | `df.dtypes` / `df.info()` | `.str.replace('$', '').str.replace('.', '')` y `pd.to_numeric(...)` |
| 5 | Fechas como texto | `fecha` = `14/03/2025` (un solo formato) | `df.dtypes` | `pd.to_datetime(df['fecha'], format='%d/%m/%Y')`; luego crear `df['mes'] = df['fecha'].dt.month` y `df['total'] = df['cantidad'] * df['precio_unitario']` |
| 6 | Datos faltantes | `metodo_pago` ~3 % vacío; `precio_unitario` ~1 % vacío; `edad_cliente` ~5 % vacío | `df.isna().sum()` | `df['metodo_pago'] = df['metodo_pago'].fillna('Sin dato')`; `df = df.dropna(subset=['precio_unitario'])`; edad se deja vacía y se explica por qué (pandas la ignora en promedios y gráficas) |
| 7 | Valores imposibles | `tiempo_entrega` negativo, 0 o 999; `calificacion` 0, 10, 45 | `df.describe()` | `df = df[df['tiempo_entrega'].between(1, 180)]`; `df = df[df['calificacion'].between(1, 5)]` |
| L | Cargar | — | `df.info()` final | `df.to_csv('domicilios_limpio.csv', index=False)` |

Cuidado con el orden: los faltantes de `precio_unitario` deben sobrevivir a los pasos 3–5
sin romper nada (`str.replace` sobre NaN da NaN; `pd.to_numeric` acepta NaN). Las
columnas con valores imposibles (`tiempo_entrega`, `calificacion`) **no** tienen
faltantes, para que `between` no borre filas por accidente. El total se calcula en el
paso 5 y queda NaN donde falta el precio; esas filas se eliminan en el paso 6.
Los errores no deben solaparse de forma que un paso dependa de otro de manera
confusa. `fuentes/generar_datos.py` debe guardar `fuentes/contenido/catalogo_errores.json`
con los conteos exactos de cada error y el número final de filas esperado.

## 4. Las 5 gráficas del análisis (código de una línea, pandas `.plot`)

| Pregunta de negocio | Gráfica | Código base |
|---|---|---|
| ¿Qué productos se piden más? | Barras horizontales | `df['producto'].value_counts().plot(kind='barh', title=...)` |
| ¿Cómo cambian las ventas durante el año? | Línea | `df.groupby('mes')['total'].sum().plot(kind='line', marker='o', title=...)` |
| ¿Quiénes son nuestros clientes? | Histograma | `df['edad_cliente'].plot(kind='hist', bins=20, title=...)` |
| ¿Tardamos más cuando el pedido va más lejos? | Dispersión | `df.plot(kind='scatter', x='distancia_km', y='tiempo_entrega', title=...)` |
| ¿Dónde se demoran más los domicilios? | Caja y bigotes | `df.boxplot(column='tiempo_entrega', by='municipio')` |

`groupby` se introduce aquí como el único concepto nuevo de agregación. Se permite el
parámetro `color='#06784F'` y `title=`/`xlabel=`/`ylabel=` para que se vea limpio.
Cada gráfica en la presentación: código + imagen real + 2–3 frases de lectura
(qué se ve, qué decisión sugiere) + una pregunta para el grupo.

## 5. Notebooks

- `notebooks/taller_solucion.ipynb`: completo, ejecutado sin errores, con salidas.
- `notebooks/taller_estudiante.ipynb`: mismo orden y celdas; en cada celda de
  práctica el método clave se reemplaza por `___` (tres guiones bajos), p. ej.
  `df = df.___()`. Sin salidas. Primera celda Markdown: cómo abrir en Colab y subir
  `domicilios_sucio.csv` arrastrándolo al panel de archivos (ícono de carpeta).
- Cada paso: celda Markdown con «Paso N · título», el problema en una frase y el
  **método a usar** en `código`; luego celda(s) de código.
- Los dos notebooks se verifican ejecutando la solución en pandas 2.2 y 3.x
  (entornos abajo). Las cifras que aparezcan en la presentación salen de la ejecución.

## 6. Identidad visual de la presentación (copiar la referencia)

Referencia: la presentación del proyecto final de Andrés en la Facultad de Minas (no se incluye en el repositorio); sus fondos están en `fuentes/fondos/`.
Diapositiva 16:9 de **10 × 5,625 in (720 × 405 pt)**. Fuente **Calibri** en todo;
el código en **Consolas**.

Fondos (imagen a toda la diapositiva, ya traen línea dorada, pie y logo UNAL):
- `fuentes/fondos/fondo_portada.png` — portada (pie verde con logo).
- `fuentes/fondos/fondo_contenido.png` — todas las de contenido (pie beige con logo).
- `fuentes/fondos/fondo_cierre.png` — «Gracias» (fondo verde completo).

Colores: verde UNAL `#06784F` (títulos, encabezados de tabla, bloques destacados);
verde oscuro `#044E34` (etiquetas en negrita dentro de texto); dorado `#FFB93E`
(etiqueta sobre fondo verde); texto `#29272D`; texto secundario `#626268`;
tarjeta `#F0F5F2`; blanco sobre verde `#FFFFFF`; crema sobre cierre `#F7F5F2`.
Semáforo solo si hace falta: `#2E7D32` bien, `#C18300` medio, `#C62828` mal.

Medidas (pt) de la diapositiva de contenido:
- Número de página: (22, 7), 10 pt, `#626268`.
- Título: (37, 37), 21 pt, `#06784F`, una línea (máx. ~60 caracteres).
- Etiqueta de sección en MAYÚSCULAS ESPACIADAS: (37, 73), 10 pt, `#06784F`
  (espaciado de caracteres ~3 pt; usar el atributo `spc` del run, no espacios).
- Área útil: x 37,4 → 682,6; y 92 → 340.
- Pie: «Facultad de Minas · Sede Medellín», Calibri cursiva 9 pt, `#06784F`, en (20, 374).
- Tarjetas: relleno `#F0F5F2`, sin borde, título 12 pt `#06784F`, cuerpo 9,8 pt `#29272D`.
- Bloque destacado: relleno `#06784F`, etiqueta dorada espaciada 9,6 pt, texto blanco 12,6 pt.
- Tablas: encabezado `#06784F` con texto blanco negrita 9,4–9,6 pt; filas alternas
  blanco / `#F0F5F2`; sin bordes.
- Pies de figura: cursiva 8,6 pt `#626268`.
- Cifras grandes (KPI): 26 pt `#06784F` con leyenda 9,6 pt `#626268`.
- Código: caja relleno `#F0F5F2` con barra izquierda de 3 pt `#06784F`; Consolas
  10,5–12 pt `#29272D`; el **método clave en negrita `#06784F`**. Legible proyectado.
- Portada: título 27 pt `#06784F` en (37,119); etiqueta espaciada 10 pt; nombre 13 pt
  `#29272D`; nota 10,6 pt `#626268`; texto blanco 10,6 pt en el pie verde (37,374):
  «Universidad Nacional de Colombia · Facultad de Minas · Sede Medellín».
- Cierre: «Gracias» 30 pt `#F7F5F2` en (37,108); etiqueta dorada espaciada; textos 9,2 pt crema.
- Títulos como afirmaciones que dicen algo («Cada gráfica responde una pregunta
  distinta»), como en la referencia. Sin viñetas genéricas de relleno.
- Sin animaciones ni transiciones.

Figuras de la teoría (`fuentes/figuras/teoria_*.png`): matplotlib, fuente Calibri,
paleta UNAL (verde `#06784F` principal, dorado `#FFB93E` y gris `#9A9AA0` de apoyo),
fondo blanco, sin bordes superior/derecho, 200 dpi, proporción acorde al hueco.
Datos ilustrativos (no presentarlos como reales).

## 7. Formato de contenido (JSON) que consume el constructor

`fuentes/contenido/teoria.json` (bloques 1–2) y `fuentes/contenido/taller.json`
(bloques 3–5) son listas de diapositivas. Cada diapositiva:

```json
{"id": "slug-unico", "layout": "<uno de abajo>", "titulo": "...", "etiqueta": "...",
 "notas": "[0:14 – 0:17] Qué decir...", ...campos del layout}
```

Layouts (el constructor puede añadir otros si los documenta):
- `portada`: `titulo` (con `\n`), `etiqueta`, `autores`, `nota`.
- `tarjetas`: `tarjetas`: [{`titulo`, `texto`}] (2–4), opcional `destacado`: {`etiqueta`, `texto`}.
- `cifras`: `cifras`: [{`valor`, `leyenda`}] (2–4) + opcional `tabla` o `texto`.
- `texto_figura`: `parrafos`: [{`negrita`?, `texto`}] o `vinetas`, `figura` (ruta relativa a `fuentes/`), `pie`.
- `tabla`: `columnas`, `filas`, opcional `figura`, `pie`, `nota`.
- `flujo`: `pasos`: [{`titulo`, `texto`}] (4–6, se dibujan como cajas con flechas).
- `paso_etl`: `problema` (texto), `ejemplo` (lista de valores sucios cortos), `metodo`
  (nombre del método clave, p. ej. `drop_duplicates()`), `codigo` (string exacto del
  notebook), `resultado` (texto con cifras reales), opcional `figura`.
- `grafica_taller`: `pregunta`, `codigo`, `figura`, `lectura` (2–3 frases), `pregunta_grupo`.
- `seccion`: separador sobre `fondo_portada.png`: `titulo`, `etiqueta`, `texto`.
- `lista_numerada`: `items`: [{`negrita`, `texto`}].
- `cierre`: `titulo` («Gracias»), `etiqueta`, `lineas`, `firma`.

## 8. Entorno y herramientas

- Dos entornos de Python para comprobar compatibilidad: uno con pandas 3.x
  (`pip install -r fuentes/requirements.txt`) y otro como Colab, con pandas 2.2.
- PowerPoint 2016+ en Windows para exportar PPTX → PDF por COM (`fuentes/exportar.ps1`);
  `fuentes/renderizar.py` convierte el PDF a PNG para revisarlo.
- Fuentes Calibri y Consolas (incluidas en Windows).
- Las rutas de este documento son relativas a la raíz del repositorio.

## 9. Entregables finales

```
minicurso-analisis-de-datos/
  presentacion/Minicurso_Analisis_de_Datos.pptx   (con notas del orador)
  presentacion/Minicurso_Analisis_de_Datos.pdf
  datos/domicilios_sucio.csv
  notebooks/taller_estudiante.ipynb
  notebooks/taller_solucion.ipynb
  fuentes/  (generador, contenido JSON, figuras, constructor del pptx, revisión)
```
