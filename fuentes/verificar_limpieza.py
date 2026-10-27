import codecs
import json
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

warnings.simplefilter('error', FutureWarning)
warnings.simplefilter('error', DeprecationWarning)
warnings.simplefilter('error', PendingDeprecationWarning)
for nombre in ['SettingWithCopyWarning', 'ChainedAssignmentError', 'DtypeWarning', 'PerformanceWarning']:
    if hasattr(pd.errors, nombre):
        warnings.simplefilter('error', getattr(pd.errors, nombre))

RAIZ = Path(__file__).resolve().parents[1]
CATALOGO = json.loads((RAIZ / 'fuentes' / 'contenido' / 'catalogo_errores.json').read_text(encoding='utf-8'))
PASOS = CATALOGO['pasos']
SALIDA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(tempfile.mkdtemp(prefix='verificacion_limpieza_'))
SALIDA.mkdir(parents=True, exist_ok=True)
shutil.copy(RAIZ / 'datos' / 'domicilios_sucio.csv', SALIDA / 'domicilios_sucio.csv')
CON_BOM = (RAIZ / 'datos' / 'domicilios_sucio.csv').read_bytes().startswith(codecs.BOM_UTF8)
os.chdir(SALIDA)

revisiones = 0


def titulo(texto):
    print()
    print(texto)
    print('-' * len(texto))


def revisar(descripcion, obtenido, esperado):
    global revisiones
    assert obtenido == esperado, f'{descripcion}: obtenido {obtenido!r}, esperado {esperado!r}'
    revisiones += 1
    print(f'  [ok] {descripcion}: {obtenido}')


def afirmar(descripcion, condicion, detalle=''):
    global revisiones
    assert condicion, f'{descripcion} ({detalle})'
    revisiones += 1
    print(f'  [ok] {descripcion}' + (f' — {detalle}' if detalle else ''))


def entero(diccionario):
    return {str(k): int(v) for k, v in diccionario.items()}


def orden(serie):
    return [[str(k), int(v)] for k, v in serie.items()]


def lista(diccionario):
    return [[k, v] for k, v in diccionario.items()]


def sin_empates(descripcion, conteos):
    afirmar(f'{descripcion}: sin empates, mismo orden en pandas 2.2 y 3.x', conteos.is_unique)


print(f'pandas {pd.__version__} · matplotlib {matplotlib.__version__} · carpeta de trabajo {SALIDA}')

titulo('Paso E · Extraer')
df = pd.read_csv('domicilios_sucio.csv')
df.head()
revisar('read_csv sin parámetros: forma', list(df.shape), PASOS['E']['forma_sin_parametros'])
revisar('read_csv sin parámetros: número de columnas', df.shape[1], 1)
df = pd.read_csv('domicilios_sucio.csv', sep=';', decimal=',')
df.head()
revisar("read_csv con sep=';' y decimal=',': forma", list(df.shape), PASOS['E']['forma'])
afirmar('Distancia KM es numérica', pd.api.types.is_float_dtype(df['Distancia KM']), str(df['Distancia KM'].dtype))
afirmar('Precio Unitario llega como texto', not pd.api.types.is_numeric_dtype(df['Precio Unitario']),
        str(df['Precio Unitario'].dtype))
revisar('encabezados sucios', list(df.columns), CATALOGO['encabezados_sucios'])
afirmar('el archivo trae BOM y pandas no lo deja en el primer encabezado', CON_BOM and df.columns[0] == 'ID Pedido',
        repr(df.columns[0]))

titulo('Paso 1 · Nombres de columnas')
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
revisar('nombres limpios', list(df.columns), PASOS['1']['columnas'])

titulo('Paso 2 · Duplicados')
revisar('df.duplicated().sum()', int(df.duplicated().sum()), PASOS['2']['duplicados'])
df = df.drop_duplicates()
revisar('forma tras drop_duplicates', list(df.shape), PASOS['2']['forma_despues'])
revisar('id_pedido único tras quitar duplicados', bool(df['id_pedido'].is_unique), True)

titulo('Paso 3 · Texto inconsistente')
revisar('municipio antes (value_counts)', orden(df['municipio'].value_counts()),
        lista(PASOS['3']['municipio_antes']))
sin_empates('municipio antes', df['municipio'].value_counts())
df['municipio'] = df['municipio'].str.strip().str.title()
df['municipio'] = df['municipio'].replace({'Medellin': 'Medellín', 'Itagui': 'Itagüí'})
revisar('municipio después', orden(df['municipio'].value_counts()), lista(PASOS['3']['municipio_despues']))
sin_empates('municipio después', df['municipio'].value_counts())
revisar('municipios distintos', sorted(df['municipio'].unique().tolist()),
        sorted(['Medellín', 'Bello', 'Itagüí', 'Envigado', 'Sabaneta']))
revisar('metodo_pago antes', orden(df['metodo_pago'].value_counts()), lista(PASOS['3']['metodo_pago_antes']))
sin_empates('metodo_pago antes', df['metodo_pago'].value_counts())
df['metodo_pago'] = df['metodo_pago'].str.strip().str.title()
revisar('metodo_pago después', orden(df['metodo_pago'].value_counts()), lista(PASOS['3']['metodo_pago_despues']))
sin_empates('metodo_pago después', df['metodo_pago'].value_counts())
revisar('métodos distintos (sin contar vacíos)', sorted(df['metodo_pago'].dropna().unique().tolist()),
        sorted(['Efectivo', 'Nequi', 'Tarjeta', 'Daviplata']))
revisar('metodo_pago vacíos siguen vacíos', int(df['metodo_pago'].isna().sum()), PASOS['3']['metodo_pago_faltantes'])

titulo('Paso 4 · Números guardados como texto')
print('  df.dtypes antes:', dict(df.dtypes.astype(str)))
df['precio_unitario'] = df['precio_unitario'].str.replace('$', '')
df['precio_unitario'] = df['precio_unitario'].str.replace('.', '')
df['precio_unitario'] = pd.to_numeric(df['precio_unitario'])
print('  df.dtypes después:', dict(df.dtypes.astype(str)))
afirmar('precio_unitario numérico', pd.api.types.is_numeric_dtype(df['precio_unitario']),
        str(df['precio_unitario'].dtype))
revisar('precio_unitario faltantes', int(df['precio_unitario'].isna().sum()), PASOS['4']['precio_unitario_faltantes'])
revisar('precio mínimo', int(df['precio_unitario'].min()), PASOS['4']['precio_min'])
revisar('precio máximo', int(df['precio_unitario'].max()), PASOS['4']['precio_max'])

titulo('Paso 5 · Fechas como texto')
df['fecha'] = pd.to_datetime(df['fecha'], format='%d/%m/%Y')
df['mes'] = df['fecha'].dt.month
df['total'] = df['cantidad'] * df['precio_unitario']
afirmar('fecha es datetime', pd.api.types.is_datetime64_any_dtype(df['fecha']), str(df['fecha'].dtype))
revisar('fecha mínima', df['fecha'].min().date().isoformat(), PASOS['5']['fecha_min'])
revisar('fecha máxima', df['fecha'].max().date().isoformat(), PASOS['5']['fecha_max'])
revisar('meses presentes', sorted(df['mes'].unique().tolist()), list(range(1, 13)))
revisar('forma con mes y total', list(df.shape), PASOS['5']['forma_despues'])
afirmar('total numérico', pd.api.types.is_numeric_dtype(df['total']), str(df['total'].dtype))
revisar('total vacío donde falta el precio', int(df['total'].isna().sum()), PASOS['5']['total_faltantes'])

titulo('Paso 6 · Datos faltantes')
revisar('df.isna().sum() antes', entero(df.isna().sum().to_dict()), PASOS['6']['faltantes_antes'])
df['metodo_pago'] = df['metodo_pago'].fillna('Sin dato')
df = df.dropna(subset=['precio_unitario'])
revisar("filas con 'Sin dato'", int((df['metodo_pago'] == 'Sin dato').sum()), PASOS['6']['sin_dato'])
revisar('forma tras dropna', list(df.shape), PASOS['6']['forma_despues'])
revisar('métodos de pago tras el paso 6', sorted(df['metodo_pago'].unique().tolist()),
        sorted(['Efectivo', 'Nequi', 'Tarjeta', 'Daviplata', 'Sin dato']))
print('  df.isna().sum() después:', {k: int(v) for k, v in df.isna().sum().items() if v})

titulo('Paso 7 · Valores imposibles')
resumen = df.describe()
revisar('tiempo_entrega mínimo (describe)', int(resumen.at['min', 'tiempo_entrega']), PASOS['7']['tiempo_entrega_min'])
revisar('tiempo_entrega máximo (describe)', int(resumen.at['max', 'tiempo_entrega']), PASOS['7']['tiempo_entrega_max'])
revisar('calificacion mínima (describe)', int(resumen.at['min', 'calificacion']), PASOS['7']['calificacion_min'])
revisar('calificacion máxima (describe)', int(resumen.at['max', 'calificacion']), PASOS['7']['calificacion_max'])
df = df[df['tiempo_entrega'].between(1, 180)]
revisar('forma tras filtrar tiempo_entrega', list(df.shape), PASOS['7']['forma_tras_tiempo'])
df = df[df['calificacion'].between(1, 5)]
revisar('forma tras filtrar calificacion', list(df.shape), PASOS['7']['forma_despues'])
resumen = df.describe()
print('  tiempo_entrega queda entre', int(resumen.at['min', 'tiempo_entrega']), 'y', int(resumen.at['max', 'tiempo_entrega']))
print('  calificacion queda entre', int(resumen.at['min', 'calificacion']), 'y', int(resumen.at['max', 'calificacion']))

titulo('Paso L · Cargar')
df.info()
df.to_csv('domicilios_limpio.csv', index=False)
revisar('domicilios_limpio.csv releído: forma', list(pd.read_csv('domicilios_limpio.csv').shape), PASOS['L']['forma'])
revisar('filas finales', len(df), CATALOGO['filas_finales_esperadas'])
respaldo = pd.read_csv('domicilios_limpio.csv')
revisar('punto de control: ventas por mes desde domicilios_limpio.csv',
        {str(k): int(round(v)) for k, v in respaldo.groupby('mes')['total'].sum().items()},
        CATALOGO['final']['ventas_por_mes'])
revisar('punto de control: pedidos por producto desde domicilios_limpio.csv',
        orden(respaldo['producto'].value_counts()), lista(CATALOGO['final']['productos']))
revisar('punto de control: edades vacías', int(respaldo['edad_cliente'].isna().sum()),
        CATALOGO['final']['edad_cliente_faltantes'])
for columna in ['precio_unitario', 'total', 'metodo_pago']:
    revisar(f'{columna} sin faltantes al final', int(df[columna].isna().sum()), 0)
revisar('edad_cliente se deja con faltantes', int(df['edad_cliente'].isna().sum()), CATALOGO['final']['edad_cliente_faltantes'])
revisar('pedidos por producto', orden(df['producto'].value_counts()), lista(CATALOGO['final']['productos']))
sin_empates('pedidos por producto', df['producto'].value_counts())
revisar('pedidos por municipio', orden(df['municipio'].value_counts()), lista(CATALOGO['final']['municipios']))
sin_empates('pedidos por municipio', df['municipio'].value_counts())
revisar('pedidos por método de pago', orden(df['metodo_pago'].value_counts()), lista(CATALOGO['final']['metodo_pago']))
sin_empates('pedidos por método de pago', df['metodo_pago'].value_counts())
revisar('ventas por mes', {str(k): int(round(v)) for k, v in df.groupby('mes')['total'].sum().items()},
        CATALOGO['final']['ventas_por_mes'])

titulo('Patrones de las cinco gráficas')
productos = df['producto'].value_counts()
print('  value_counts de producto:', productos.to_dict())
revisar('producto más pedido', productos.index[0], 'Pan de bono')
afirmar('líder claro', productos.iloc[0] >= 1.25 * productos.iloc[1],
        f'{productos.iloc[0]} contra {productos.iloc[1]} ({productos.iloc[0] / productos.iloc[1]:.2f} veces)')
afirmar('rezagado claro', productos.index[-1] in ['Torta de chocolate', 'Croissant'] and productos.iloc[-2] >= 1.2 * productos.iloc[-1],
        f'{productos.index[-1]} con {productos.iloc[-1]} contra {productos.iloc[-2]}')

ventas = df.groupby('mes')['total'].sum()
print('  ventas por mes:', {int(k): int(v) for k, v in ventas.items()})
revisar('mes con más ventas', int(ventas.idxmax()), 12)
revisar('mes con menos ventas', int(ventas.idxmin()), 2)
afirmar('diciembre se despega', ventas[12] >= 1.15 * ventas.drop(12).max(),
        f'{ventas[12] / ventas.drop(12).max():.2f} veces el segundo mes')
afirmar('febrero es valle claro', ventas[2] <= 0.88 * ventas.drop(2).min(),
        f'{ventas[2] / ventas.drop(2).min():.2f} del segundo mes más bajo')
afirmar('subida en junio y julio', min(ventas[6], ventas[7]) > 1.1 * max(ventas[5], ventas[8]),
        f'jun {int(ventas[6])}, jul {int(ventas[7])} contra may {int(ventas[5])}, ago {int(ventas[8])}')

edad = df['edad_cliente']
jovenes = int(edad.between(19, 25).sum())
familias = int(edad.between(38, 48).sum())
valle = int(edad.between(29, 35).sum())
afirmar('edad bimodal', jovenes >= 2 * valle and familias >= 2 * valle,
        f'19–25: {jovenes}, 38–48: {familias}, 29–35: {valle}')
afirmar('edad en rango plausible', edad.min() >= 15 and edad.max() <= 75, f'{int(edad.min())} a {int(edad.max())}')

correlacion = df['distancia_km'].corr(df['tiempo_entrega'])
afirmar('correlación distancia–tiempo > 0,7', correlacion > 0.7, f'{correlacion:.3f}')
afirmar('distancias entre 0,5 y 12 km', df['distancia_km'].min() >= 0.5 and df['distancia_km'].max() <= 12,
        f"{df['distancia_km'].min()} a {df['distancia_km'].max()}")

grupos = df.groupby('municipio')['tiempo_entrega']
medianas = grupos.median().sort_values(ascending=False)
rangos = (grupos.quantile(0.75) - grupos.quantile(0.25)).sort_values(ascending=False)
print('  medianas de tiempo:', medianas.to_dict())
print('  rango intercuartílico:', rangos.to_dict())
revisar('municipio con mayor mediana', medianas.index[0], 'Bello')
afirmar('Bello claramente más lento', medianas.iloc[0] - medianas.iloc[1] >= 8,
        f'{medianas.iloc[0] - medianas.iloc[1]:.1f} min sobre {medianas.index[1]}')
revisar('municipio con más dispersión', rangos.index[0], 'Bello')
q1 = grupos.transform(lambda s: s.quantile(0.25))
q3 = grupos.transform(lambda s: s.quantile(0.75))
atipicos = df[(df['tiempo_entrega'] > q3 + 1.5 * (q3 - q1)) | (df['tiempo_entrega'] < q1 - 1.5 * (q3 - q1))]
afirmar('hay atípicos legítimos en la caja', len(atipicos) > 0,
        f"{len(atipicos)} en total: {atipicos['municipio'].value_counts().to_dict()}, máximo {int(df['tiempo_entrega'].max())} min")

lento = df[df['tiempo_entrega'] > 60]['calificacion'].mean()
rapido = df[df['tiempo_entrega'] <= 40]['calificacion'].mean()
afirmar('reto: calificación baja con entregas lentas', lento < rapido - 0.8,
        f'promedio {lento:.2f} con más de 60 min contra {rapido:.2f} con 40 min o menos')

titulo('Las cinco gráficas (pandas .plot)')
df['producto'].value_counts().plot(kind='barh', title='Pedidos por producto', color='#06784F')
plt.savefig('grafica_1_barras.png', dpi=80)
plt.close('all')
df.groupby('mes')['total'].sum().plot(kind='line', marker='o', title='Ventas por mes', color='#06784F')
plt.savefig('grafica_2_linea.png', dpi=80)
plt.close('all')
df['edad_cliente'].plot(kind='hist', bins=20, title='Edad de los clientes', color='#06784F')
plt.savefig('grafica_3_histograma.png', dpi=80)
plt.close('all')
df.plot(kind='scatter', x='distancia_km', y='tiempo_entrega', title='Distancia contra tiempo', color='#06784F')
plt.savefig('grafica_4_dispersion.png', dpi=80)
plt.close('all')
df.boxplot(column='tiempo_entrega', by='municipio')
plt.savefig('grafica_5_caja.png', dpi=80)
plt.close('all')
afirmar('las cinco gráficas se dibujan sin advertencias', True, f'PNG en {SALIDA}')

print()
print(f'TODO EN ORDEN: {revisiones} revisiones superadas con pandas {pd.__version__}.')
