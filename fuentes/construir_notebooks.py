import re
import shutil
import sys
import tempfile
from pathlib import Path

import nbformat

RAIZ = Path(__file__).resolve().parents[1]
CARPETA = RAIZ / 'notebooks'
CSV = RAIZ / 'datos' / 'domicilios_sucio.csv'
LIMPIO = RAIZ / 'datos' / 'domicilios_limpio.csv'
HUECO = '___'
MARCA = re.compile(r'«(.+?)»')

VERSIONES = {
    'solucion': {
        'archivo': 'taller_solucion.ipynb',
        'version': '**Versión con soluciones.** Todas las celdas están completas y ejecutadas: úsala para revisar tu trabajo.',
    },
    'estudiante': {
        'archivo': 'taller_estudiante.ipynb',
        'version': '**Versión para completar.** Donde veas `___` escribe el método que muestra la diapositiva y ejecuta la celda.',
    },
}

INTRO = """# Taller · Limpieza y análisis de datos con pandas

**Minicurso «Introducción al análisis de datos con Python»** · Universidad Nacional de Colombia · Facultad de Minas · Sede Medellín

{version}

## Antes de empezar: abre el taller en Google Colab

1. Entra a [colab.research.google.com](https://colab.research.google.com) con tu cuenta de Google.
2. Menú **Archivo → Subir cuaderno** (*File → Upload notebook*) y elige `{archivo}`.
3. En la barra de la izquierda haz clic en el ícono de carpeta (**Archivos**) y arrastra `domicilios_sucio.csv` a ese panel. Colab avisa que los archivos subidos se borran al cerrar la sesión: está bien.
4. Ejecuta las celdas de arriba hacia abajo con **Shift + Enter**.

Si una celda falla porque la ejecutaste dos veces o en desorden, usa **Entorno de ejecución → Ejecutar anteriores** (*Runtime → Run before*) y vuelve a intentarlo. Si Colab se reinició y `domicilios_sucio.csv` ya no aparece en el panel de archivos, vuelve a arrastrarlo antes de ejecutar.

Si te atrasas, no te preocupes: al comienzo de «Análisis gráfico» hay un **punto de control** para seguir con la base ya limpia.

## El caso

«Pan de Datos» es una panadería **ficticia** con servicio a domicilio en el Valle de Aburrá. Cada fila del archivo es un pedido de 2025. Los datos son **sintéticos**: se crearon para este curso y no son cifras reales."""

CELDAS = [
    ('md', INTRO),
    ('md', """## Preparación

Importamos pandas con su apodo de siempre, `pd`. Las gráficas también salen de pandas (`.plot`), que usa matplotlib por dentro."""),
    ('code', """import pandas as pd"""),

    ('md', """## Paso E · Extraer: leer el archivo

**Problema:** el archivo separa las columnas con `;` y usa coma decimal (`7,1`), como Excel en Colombia, pero `read_csv` espera comas.

**Diagnóstico:** `df.head()` y `df.shape` · **Método:** `pd.read_csv('domicilios_sucio.csv', sep=';', decimal=',')`

**Error común:** leer el archivo sin decirle a pandas cuál es el separador. Ejecuta y mira qué pasa."""),
    ('code', """df = pd.«read_csv»('domicilios_sucio.csv')
df.head()"""),
    ('code', """df.«shape»"""),
    ('md', """Todo quedó amontonado en **una sola columna**. Ahora sí, con el separador y el decimal correctos:"""),
    ('code', """df = pd.read_csv('domicilios_sucio.csv', sep='«;»', decimal='«,»')
df.head()""", 'paso-e'),
    ('code', """df.«shape»"""),

    ('md', """## Paso 1 · Nombres de columnas

**Problema:** los encabezados traen espacios, mayúsculas y espacios internos (`' Fecha'`, `'Municipio '`, `'Precio Unitario'`): así es muy fácil escribirlos mal.

**Diagnóstico:** `df.columns` · **Método:** `.str.strip().str.lower().str.replace(' ', '_')`"""),
    ('code', """df.«columns»"""),
    ('code', """df.columns = df.columns.str.«strip»().str.«lower»().str.«replace»(' ', '_')
df.columns""", 'paso-1'),

    ('md', """## Paso 2 · Filas duplicadas

**Problema:** algunos pedidos quedaron registrados dos veces; si no los quitamos, contamos doble.

**Diagnóstico:** `df.duplicated().sum()` · **Método:** `df.drop_duplicates()`

Si el conteo aparece como `np.int64(...)`, es simplemente un número entero."""),
    ('code', """df.«duplicated»().sum()"""),
    ('code', """df = df.«drop_duplicates»()
df.shape""", 'paso-2'),

    ('md', """## Paso 3 · Texto inconsistente

**Problema:** el mismo municipio aparece escrito de muchas formas (`medellin`, `MEDELLIN`, `' Medellín '`, `Itagui`…) y pandas cuenta cada una por aparte.

**Diagnóstico:** `value_counts()` · **Método:** `.str.strip().str.title()` y luego `.replace({...})`

Para mirar la tabla usa `df.head()`. Si en algún momento aparece un aviso rosado `SettingWithCopyWarning`, no es un error: el resultado es el mismo."""),
    ('code', """df['municipio'].«value_counts»()"""),
    ('md', """`strip()` quita los espacios de los extremos y `title()` deja solo la primera letra en mayúscula. Como `title()` no pone tildes, `replace` cambia `Medellin` por `Medellín` e `Itagui` por `Itagüí`."""),
    ('code', """df['municipio'] = df['municipio'].str.«strip»().str.«title»()
df['municipio'] = df['municipio'].«replace»({'Medellin': 'Medellín', 'Itagui': 'Itagüí'})""", 'paso-3'),
    ('code', """df['municipio'].«value_counts»()"""),
    ('md', """Lo mismo pasa con el método de pago (`nequi`, `NEQUI`, `'Nequi '`…). Aquí bastan `strip()` y `title()`. Fíjate en que `Nequi` sale dos veces en el conteo: una de las dos trae un espacio invisible al final (`'Nequi '`). Por eso `strip()` va primero."""),
    ('code', """df['metodo_pago'].«value_counts»()"""),
    ('code', """df['metodo_pago'] = df['metodo_pago'].str.«strip»().str.«title»()
df['metodo_pago'].value_counts()"""),

    ('md', """## Paso 4 · Números guardados como texto

**Problema:** `precio_unitario` llegó como texto (`$2.800`), con signo y punto de miles; así no se puede sumar ni multiplicar.

**Diagnóstico:** `df.dtypes` · **Método:** `.str.replace('$', '')`, `.str.replace('.', '')` y `pd.to_numeric()`"""),
    ('code', """df.«dtypes»"""),
    ('md', """En `df.dtypes`, `object` significa texto (en pandas 3 aparece como `str`). Primero quitamos el `$`, después el punto de miles y al final convertimos a número."""),
    ('code', """df['precio_unitario'] = df['precio_unitario'].str.«replace»('$', '')
df['precio_unitario'] = df['precio_unitario'].str.«replace»('.', '')
df['precio_unitario'] = pd.«to_numeric»(df['precio_unitario'])""", 'paso-4'),
    ('code', """df.«dtypes»"""),

    ('md', """## Paso 5 · Fechas como texto

**Problema:** `fecha` también es texto (`03/01/2025`); como texto no se puede sacar el mes ni ordenar en el tiempo.

**Método:** `pd.to_datetime(df['fecha'], format='%d/%m/%Y')` (día/mes/año) y luego `.dt.month`. De paso creamos `total` = cantidad × precio.

**Comprobación:** `df.head()`. La columna `fecha` debe verse como `2025-01-03` y al final deben aparecer `mes` y `total`."""),
    ('code', """df['fecha'] = pd.«to_datetime»(df['fecha'], format='%d/%m/%Y')
df['mes'] = df['fecha'].dt.«month»
df['total'] = df['cantidad'] * df['precio_unitario']""", 'paso-5'),
    ('code', """df.«head»()"""),

    ('md', """## Paso 6 · Datos faltantes

**Problema:** hay celdas vacías (`NaN`) en el método de pago, el precio y la edad del cliente.

**Diagnóstico:** `df.isna().sum()` · **Método:** `fillna('Sin dato')` y `dropna(subset=['precio_unitario'])`"""),
    ('code', """df.«isna»().sum()"""),
    ('md', """Cada columna se trata distinto. Al método de pago le ponemos `'Sin dato'`, porque el pedido sí ocurrió. Sin precio no hay total de venta, así que quitamos esas filas. La **edad se deja vacía**: pandas ignora los vacíos al promediar y al graficar, y borrar esas filas haría perder pedidos válidos."""),
    ('code', """df['metodo_pago'] = df['metodo_pago'].«fillna»('Sin dato')
df = df.«dropna»(subset=['precio_unitario'])
df.shape""", 'paso-6'),
    ('code', """df.«isna»().sum()"""),

    ('md', """## Paso 7 · Valores imposibles

**Problema:** hay tiempos de entrega negativos, de 0 o de 999 minutos, y calificaciones de 0, 10 o 45, cuando la escala va de 1 a 5.

**Diagnóstico:** `df.describe()` (mira las filas `min` y `max`) · **Método:** `between()`"""),
    ('code', """df.«describe»()"""),
    ('md', """`between(1, 180)` marca con `True` las filas cuyo valor está entre 1 y 180 (incluidos) y `df[...]` se queda solo con esas. Tres horas es un límite generoso para un domicilio."""),
    ('code', """df = df[df['tiempo_entrega'].«between»(1, 180)]
df = df[df['calificacion'].«between»(1, 5)]
df.shape""", 'paso-7'),
    ('code', """df.«describe»()"""),

    ('md', """## Paso L · Cargar: guardar la base limpia

**Problema:** la base limpia solo vive en la memoria de Colab; hay que revisarla y guardarla en un archivo nuevo.

**Diagnóstico:** `df.info()` · **Método:** `df.to_csv('domicilios_limpio.csv', index=False)`"""),
    ('code', """df.«info»()
df.«to_csv»('domicilios_limpio.csv', index=False)""", 'paso-l'),
    ('md', """`domicilios_limpio.csv` aparece en el panel de archivos (a veces hay que actualizarlo). Para conservarlo: clic derecho sobre el archivo → **Descargar**. `index=False` evita guardar el índice como una columna más.

Es un archivo pensado para pandas: separa con comas y usa punto decimal. Si lo abres con doble clic en un Excel en español, todo queda en una sola columna; en Excel se abre con **Datos → Desde texto/CSV**."""),

    ('md', """# Análisis gráfico

Con la base limpia respondemos cinco preguntas de negocio. Cada gráfica es una sola instrucción de pandas (`.plot`), partida en renglones para que se lea mejor. El único concepto nuevo es `groupby`: agrupar y resumir.

Encima de cada gráfica aparece un texto como `<Axes: ...>`: es normal, es el objeto que devuelve pandas. Tus gráficas se verán con el estilo por defecto de Colab, que cambia la letra, el tamaño y el marco: los datos y la forma son los mismos que en la presentación."""),

    ('md', """## Punto de control

**Solo si te atrasaste, si algo falló o si Colab se reinició.** Sube `domicilios_limpio.csv` (carpeta *respaldo* del enlace del taller) al panel de archivos, ejecuta la celda `import pandas as pd` del comienzo y luego la celda siguiente: debe mostrar `(1180, 13)`.

Si llegaste bien hasta aquí, puedes saltarla. Ejecutarla tampoco daña nada: lee el archivo que acabas de guardar en el paso L."""),
    ('code', """df = pd.read_csv('domicilios_limpio.csv')
df.shape""", 'punto-control'),

    ('md', """## Gráfica 1 · ¿Qué productos se piden más?

**Gráfica:** barras horizontales · **Método:** `value_counts().plot(kind='barh')`"""),
    ('code', """df['producto'].value_counts().plot(
    kind='«barh»', title='Pedidos por producto', color='#06784F')""", 'barras'),

    ('md', """## Gráfica 2 · ¿Cómo cambian las ventas durante el año?

**Gráfica:** línea · **Método:** `groupby('mes')['total'].sum()` agrupa los pedidos por mes y suma sus ventas. El `1e6` encima del eje significa «millones»."""),
    ('code', """df.«groupby»('mes')['total'].sum().plot(
    kind='line', marker='o', color='#06784F',
    title='Ventas por mes', ylabel='Pesos')""", 'linea'),

    ('md', """## Gráfica 3 · ¿Quiénes son nuestros clientes?

**Gráfica:** histograma de la edad · **Método:** `plot(kind='hist', bins=20)`. Los pedidos sin edad simplemente no se cuentan."""),
    ('code', """df['edad_cliente'].plot(
    kind='«hist»', bins=20, color='#06784F',
    title='Edad de los clientes', ylabel='Pedidos')""", 'histograma'),

    ('md', """## Gráfica 4 · ¿Tardamos más cuando el pedido va más lejos?

**Gráfica:** dispersión · **Método:** `df.plot(kind='scatter', x=..., y=...)`"""),
    ('code', """df.plot(
    kind='«scatter»', x='distancia_km', y='tiempo_entrega',
    title='Distancia contra tiempo de entrega', color='#06784F')""", 'dispersion'),

    ('md', """## Gráfica 5 · ¿Dónde se demoran más los domicilios?

**Gráfica:** caja y bigotes · **Método:** `df.boxplot(column=..., by=...)`. pandas agrega por su cuenta un título en inglés («Boxplot grouped by municipio»): no es un error."""),
    ('code', """df.«boxplot»(column='tiempo_entrega', by='municipio', color='#06784F')""", 'caja'),

    ('md', """## Reto opcional · ¿Califican peor cuando el domicilio tarda más?

Calcula el tiempo promedio de entrega para cada calificación y grafícalo en barras. **Pista:** es como la gráfica 2, pero se agrupa por `calificacion`, se resume `tiempo_entrega` y se usa `mean()` (promedio) en lugar de `sum()`."""),
    ('code', """df.groupby('«calificacion»')['«tiempo_entrega»'].«mean»().plot(
    kind='barh', color='#06784F',
    title='Minutos promedio de entrega por calificación')""", 'reto'),

    ('md', """## Para seguir aprendiendo

- Documentación de pandas: [pandas.pydata.org/docs](https://pandas.pydata.org/docs/)
- Kaggle Learn, cursos gratuitos de pandas y visualización: [kaggle.com/learn](https://www.kaggle.com/learn)
- Google Colab: [colab.research.google.com](https://colab.research.google.com)"""),
]


def solucion(fuente):
    return MARCA.sub(r'\1', fuente)


def estudiante(fuente):
    return MARCA.sub(HUECO, fuente)


def rellenos(fuente):
    return MARCA.findall(fuente)


def celdas_de_codigo():
    return [celda for celda in CELDAS if celda[0] == 'code']


def codigo(clave):
    for celda in celdas_de_codigo():
        if len(celda) > 2 and celda[2] == clave:
            return solucion(celda[1])
    raise KeyError(clave)


def construir(variante):
    datos = VERSIONES[variante]
    nb = nbformat.v4.new_notebook()
    nb.metadata = {
        'kernelspec': {'name': 'python3', 'display_name': 'Python 3', 'language': 'python'},
        'language_info': {'name': 'python'},
        'colab': {'provenance': []},
    }
    for numero, celda in enumerate(CELDAS):
        tipo, texto = celda[0], celda[1]
        if tipo == 'md':
            if numero == 0:
                texto = texto.format(**datos)
            nueva = nbformat.v4.new_markdown_cell(texto)
        else:
            nueva = nbformat.v4.new_code_cell(solucion(texto) if variante == 'solucion' else estudiante(texto))
        nueva['id'] = f'celda-{numero:02d}'
        nb.cells.append(nueva)
    nbformat.validate(nb)
    return nb


def problemas_en_salidas(nb):
    problemas = []
    for numero, celda in enumerate(nb.cells):
        for salida in celda.get('outputs', []):
            if salida.get('output_type') == 'error':
                problemas.append(f"celda {numero}: {salida['ename']}: {salida['evalue']}")
            elif salida.get('output_type') == 'stream' and salida.get('name') == 'stderr':
                problemas.append(f"celda {numero}: stderr: {salida['text'][:300]}")
            datos = salida.get('data', {})
            textos = [salida.get('text', ''), datos.get('text/plain', ''), datos.get('text/html', '')]
            if any('Warning' in t for t in textos):
                problemas.append(f'celda {numero}: aparece la palabra Warning')
    return problemas


def ejecutar(nb):
    from nbclient import NotebookClient

    carpeta = Path(tempfile.mkdtemp(prefix='taller_solucion_'))
    shutil.copy(CSV, carpeta / CSV.name)
    try:
        NotebookClient(nb, timeout=300, kernel_name='python3', record_timing=False,
                       resources={'metadata': {'path': str(carpeta)}}).execute()
        limpio = (carpeta / LIMPIO.name).read_bytes()
    finally:
        shutil.rmtree(carpeta, ignore_errors=True)
    nb.metadata['language_info'] = {'name': 'python'}
    return problemas_en_salidas(nb), limpio


def main():
    CARPETA.mkdir(exist_ok=True)
    nb_solucion = construir('solucion')
    nb_estudiante = construir('estudiante')
    if '--ejecutar' in sys.argv:
        problemas, limpio = ejecutar(nb_solucion)
        if problemas:
            print('\n'.join(problemas))
            sys.exit('La solución tiene errores o advertencias en las salidas; no se guardó.')
        LIMPIO.write_bytes(limpio)
        print(f'{LIMPIO.name} (respaldo del punto de control) escrito en {LIMPIO.parent}')
    nbformat.write(nb_solucion, CARPETA / VERSIONES['solucion']['archivo'])
    nbformat.write(nb_estudiante, CARPETA / VERSIONES['estudiante']['archivo'])
    codigo_total = len(celdas_de_codigo())
    huecos = sum(len(rellenos(celda[1])) for celda in celdas_de_codigo())
    print(f'{len(CELDAS)} celdas ({codigo_total} de código, {huecos} huecos ___) escritas en {CARPETA}')


if __name__ == '__main__':
    main()
