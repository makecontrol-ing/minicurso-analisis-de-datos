import calendar
import json
from collections import Counter
from datetime import date
from pathlib import Path

import numpy as np

SEMILLA = 2025
RAIZ = Path(__file__).resolve().parents[1]
RUTA_CSV = RAIZ / 'datos' / 'domicilios_sucio.csv'
RUTA_CATALOGO = RAIZ / 'fuentes' / 'contenido' / 'catalogo_errores.json'

N_PEDIDOS = 1210
N_DUPLICADOS = 40
N_FALTA_PAGO = 36
N_FALTA_PRECIO = 12
N_FALTA_EDAD = 60
TIEMPOS_IMPOSIBLES = [-15, -8, -4, 0, 0, 0, 999, 999, 999, 999]
CALIFICACIONES_IMPOSIBLES = [0, 0, 0, 10, 10, 10, 45, 45]
ID_INICIAL = 1001

ENCABEZADOS = ['ID Pedido', ' Fecha', 'Municipio ', 'PRODUCTO', 'Cantidad', 'Precio Unitario',
               'Metodo Pago', 'Distancia KM', 'Tiempo Entrega', 'Edad Cliente', 'Calificacion']
NOMBRES_LIMPIOS = ['id_pedido', 'fecha', 'municipio', 'producto', 'cantidad', 'precio_unitario',
                   'metodo_pago', 'distancia_km', 'tiempo_entrega', 'edad_cliente', 'calificacion']

PESOS_MES = {1: 0.80, 2: 0.58, 3: 0.78, 4: 0.80, 5: 0.83, 6: 1.04, 7: 1.08,
             8: 0.85, 9: 0.81, 10: 0.87, 11: 0.97, 12: 1.56}
PESOS_DIA_SEMANA = [0.80, 0.85, 0.90, 0.95, 1.15, 1.35, 1.25]

PRODUCTOS = {
    'Pan de bono': (0.235, 2500),
    'Buñuelo': (0.150, 2000),
    'Café': (0.140, 3200),
    'Almojábana': (0.125, 2800),
    'Sándwich': (0.112, 9500),
    'Jugo natural': (0.098, 6000),
    'Croissant': (0.080, 4500),
    'Torta de chocolate': (0.060, 7500),
}
REFUERZO_DICIEMBRE = {'Buñuelo': 1.7}

PESOS_CANTIDAD = [0.24, 0.28, 0.20, 0.13, 0.09, 0.06]

MUNICIPIOS = {
    'Medellín': {'peso': 0.44, 'distancia': (0.5, 7.5), 'extra': 0.0, 'ruido': 4.0, 'atraso': 0.015},
    'Envigado': {'peso': 0.17, 'distancia': (2.0, 8.0), 'extra': 0.0, 'ruido': 4.0, 'atraso': 0.015},
    'Itagüí': {'peso': 0.145, 'distancia': (3.0, 9.0), 'extra': 1.0, 'ruido': 4.5, 'atraso': 0.015},
    'Sabaneta': {'peso': 0.11, 'distancia': (3.5, 9.5), 'extra': 0.0, 'ruido': 4.0, 'atraso': 0.015},
    'Bello': {'peso': 0.135, 'distancia': (5.0, 12.0), 'extra': 9.0, 'ruido': 10.0, 'atraso': 0.05},
}

VARIANTES_MUNICIPIO = {
    'Medellín': {'medellin': 41, 'MEDELLIN': 33, 'Medellin': 29, ' Medellín ': 26, 'medellín': 12},
    'Envigado': {'ENVIGADO': 23, 'envigado': 18},
    'Itagüí': {'Itagui': 28, 'itagui': 21, 'ITAGUI': 16},
    'Sabaneta': {'SABANETA': 19, 'sabaneta ': 9},
    'Bello': {'BELLO ': 24, 'bello': 14},
}

METODOS = ['Efectivo', 'Nequi', 'Tarjeta', 'Daviplata']
PESOS_METODO_JOVEN = [0.18, 0.52, 0.14, 0.16]
PESOS_METODO_ADULTO = [0.36, 0.26, 0.26, 0.12]
VARIANTES_METODO = {
    'Efectivo': {'efectivo': 37, 'EFECTIVO': 31},
    'Nequi': {'nequi': 62, 'NEQUI': 35, 'Nequi ': 22},
    'Tarjeta': {'tarjeta': 30, 'TARJETA': 20},
    'Daviplata': {'DaviPlata': 25, 'daviplata': 17, 'DAVIPLATA': 13},
}
PROPORCION_PRECIO_SIN_SIGNO = 0.10


def repartir(total, pesos):
    claves = list(pesos)
    valores = np.array([pesos[c] for c in claves], dtype=float)
    exactos = valores / valores.sum() * total
    enteros = np.floor(exactos).astype(int)
    faltan = total - enteros.sum()
    orden = np.argsort(-(exactos - enteros), kind='stable')
    enteros[orden[:faltan]] += 1
    return dict(zip(claves, enteros.tolist()))


def asignar_variantes(rng, grupo, campo, canonico, variantes):
    etiquetas = [v for v, n in variantes.items() for _ in range(n)]
    etiquetas += [canonico] * (len(grupo) - len(etiquetas))
    for p, k in zip(grupo, rng.permutation(len(grupo))):
        p[campo] = etiquetas[k]


def generar_calendario(rng):
    por_mes = repartir(N_PEDIDOS, PESOS_MES)
    calendario = []
    for mes, cantidad in por_mes.items():
        dias = calendar.monthrange(2025, mes)[1]
        pesos = np.array([PESOS_DIA_SEMANA[date(2025, mes, d).weekday()] for d in range(1, dias + 1)])
        elegidos = sorted(rng.choice(np.arange(1, dias + 1), size=cantidad, p=pesos / pesos.sum()).tolist())
        pesos_producto = {p: v[0] * (REFUERZO_DICIEMBRE.get(p, 1.0) if mes == 12 else 1.0)
                          for p, v in PRODUCTOS.items()}
        productos = [p for p, n in repartir(cantidad, pesos_producto).items() for _ in range(n)]
        unidades = [u for u, n in repartir(cantidad, dict(zip(range(1, 7), PESOS_CANTIDAD))).items() for _ in range(n)]
        productos = [productos[k] for k in rng.permutation(cantidad)]
        unidades = [unidades[k] for k in rng.permutation(cantidad)]
        calendario.extend(zip([date(2025, mes, d) for d in elegidos], productos, unidades))
    return calendario


def generar_edad(rng):
    grupo = rng.choice(3, p=[0.40, 0.37, 0.23])
    if grupo == 0:
        edad = rng.normal(21.5, 2.5)
    elif grupo == 1:
        edad = rng.normal(43.0, 4.8)
    else:
        edad = rng.uniform(15, 75)
    return int(np.clip(round(edad), 15, 75))


def generar_pedido(rng, fecha, producto, cantidad, municipio):
    datos = MUNICIPIOS[municipio]
    minimo, maximo = datos['distancia']
    distancia = round(minimo + (maximo - minimo) * rng.beta(2.0, 2.6), 1)
    tiempo = 10 + 4 * distancia + datos['extra'] + rng.normal(0, datos['ruido'])
    if rng.random() < datos['atraso']:
        tiempo += rng.uniform(22, 45)
    tiempo = max(int(round(8 + 2 * distancia)), int(round(tiempo)))
    edad = generar_edad(rng)
    pesos_metodo = PESOS_METODO_JOVEN if edad < 27 else PESOS_METODO_ADULTO
    metodo = METODOS[rng.choice(4, p=pesos_metodo)]
    calificacion = int(np.clip(round(4.75 - 0.045 * (tiempo - 30) + rng.normal(0, 0.7)), 1, 5))
    return {
        'fecha': fecha, 'municipio': municipio, 'producto': producto, 'cantidad': cantidad,
        'precio': PRODUCTOS[producto][1], 'metodo': metodo, 'distancia': distancia,
        'tiempo': tiempo, 'edad': edad, 'calificacion': calificacion,
    }


def texto_precio(precio, con_signo):
    cifra = f'{precio:,}'.replace(',', '.')
    return f'${cifra}' if con_signo else cifra


def construir():
    rng = np.random.default_rng(SEMILLA)
    calendario = generar_calendario(rng)
    municipios = [m for m, n in repartir(N_PEDIDOS, {m: v['peso'] for m, v in MUNICIPIOS.items()}).items()
                  for _ in range(n)]
    municipios = [municipios[k] for k in rng.permutation(N_PEDIDOS)]
    pedidos = [generar_pedido(rng, f, p, c, m) for (f, p, c), m in zip(calendario, municipios)]
    for i, p in enumerate(pedidos):
        p['id'] = ID_INICIAL + i

    orden = rng.permutation(N_PEDIDOS)
    cortes = np.cumsum([0, N_FALTA_PAGO, N_FALTA_PRECIO, N_FALTA_EDAD,
                        len(TIEMPOS_IMPOSIBLES), len(CALIFICACIONES_IMPOSIBLES), N_DUPLICADOS])
    grupos = [sorted(orden[cortes[k]:cortes[k + 1]].tolist()) for k in range(len(cortes) - 1)]
    falta_pago, falta_precio, falta_edad, tiempo_mal, calificacion_mal, fuentes_dup = grupos

    sin_pago = set(falta_pago)
    for canonico, variantes in VARIANTES_MUNICIPIO.items():
        grupo = [p for p in pedidos if p['municipio'] == canonico]
        asignar_variantes(rng, grupo, 'municipio_txt', canonico, variantes)
    for canonico, variantes in VARIANTES_METODO.items():
        grupo = [p for i, p in enumerate(pedidos) if p['metodo'] == canonico and i not in sin_pago]
        asignar_variantes(rng, grupo, 'metodo_txt', canonico, variantes)
    for p in pedidos:
        p['precio_txt'] = texto_precio(p['precio'], rng.random() >= PROPORCION_PRECIO_SIN_SIGNO)
        p['tiempo_txt'] = p['tiempo']
        p['calificacion_txt'] = p['calificacion']
        p['edad_txt'] = p['edad']
    for i in falta_pago:
        pedidos[i]['metodo_txt'] = None
    for i in falta_precio:
        pedidos[i]['precio_txt'] = None
    for i in falta_edad:
        pedidos[i]['edad_txt'] = None
    for i, v in zip(tiempo_mal, rng.permutation(TIEMPOS_IMPOSIBLES).tolist()):
        pedidos[i]['tiempo_txt'] = int(v)
    for i, v in zip(calificacion_mal, rng.permutation(CALIFICACIONES_IMPOSIBLES).tolist()):
        pedidos[i]['calificacion_txt'] = int(v)

    desfases = rng.choice([0, 0, 1, 2, 3, 5], size=N_DUPLICADOS)
    claves = [(i, 0, i) for i in range(N_PEDIDOS)]
    claves += [(min(i + int(d), N_PEDIDOS - 1), 1, i) for i, d in zip(fuentes_dup, desfases)]
    filas = [pedidos[fuente] for _, _, fuente in sorted(claves)]
    grupos_error = {
        'falta_pago': falta_pago, 'falta_precio': falta_precio, 'falta_edad': falta_edad,
        'tiempo_imposible': tiempo_mal, 'calificacion_imposible': calificacion_mal,
        'fuentes_duplicados': fuentes_dup,
    }
    return pedidos, filas, grupos_error


def linea_csv(p):
    campos = [
        str(p['id']),
        p['fecha'].strftime('%d/%m/%Y'),
        p['municipio_txt'],
        p['producto'],
        str(p['cantidad']),
        p['precio_txt'] or '',
        p['metodo_txt'] or '',
        f"{p['distancia']:.1f}".replace('.', ','),
        str(p['tiempo_txt']),
        '' if p['edad_txt'] is None else str(p['edad_txt']),
        str(p['calificacion_txt']),
    ]
    return ';'.join(campos)


def escribir_csv(filas):
    RUTA_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(RUTA_CSV, 'w', encoding='utf-8-sig', newline='') as archivo:
        archivo.write(';'.join(ENCABEZADOS) + '\r\n')
        for p in filas:
            archivo.write(linea_csv(p) + '\r\n')


def conteo(valores):
    return dict(Counter(valores).most_common())


def construir_catalogo(pedidos, filas, grupos):
    eliminadas_precio = set(grupos['falta_precio'])
    eliminadas_tiempo = set(grupos['tiempo_imposible'])
    eliminadas_calificacion = set(grupos['calificacion_imposible'])
    finales = [p for i, p in enumerate(pedidos)
               if i not in eliminadas_precio | eliminadas_tiempo | eliminadas_calificacion]

    def canonico_pago(p):
        return 'Sin dato' if p['metodo_txt'] is None else p['metodo']

    ventas_mes = Counter()
    for p in finales:
        ventas_mes[p['fecha'].month] += p['cantidad'] * p['precio']

    tras_paso_6 = len(pedidos) - len(eliminadas_precio)
    tras_tiempo = tras_paso_6 - len(eliminadas_tiempo)
    faltantes = {c: 0 for c in NOMBRES_LIMPIOS + ['mes', 'total']}
    faltantes['precio_unitario'] = N_FALTA_PRECIO
    faltantes['metodo_pago'] = N_FALTA_PAGO
    faltantes['edad_cliente'] = N_FALTA_EDAD
    faltantes['total'] = N_FALTA_PRECIO

    tiempos_sucios = [p['tiempo_txt'] for p in pedidos]
    calificaciones_sucias = [p['calificacion_txt'] for p in pedidos]

    return {
        'descripcion': 'Datos sintéticos creados para el curso por fuentes/generar_datos.py. '
                       'La empresa «Pan de Datos» es ficticia; ninguna cifra es real.',
        'semilla': SEMILLA,
        'archivo': 'datos/domicilios_sucio.csv',
        'formato': {'separador': ';', 'decimal': ',', 'codificacion': 'UTF-8 con BOM (para que Excel muestre bien las tildes)', 'fin_de_linea': 'CRLF'},
        'filas_sucias': len(filas),
        'pedidos_unicos': len(pedidos),
        'duplicados': N_DUPLICADOS,
        'filas_finales_esperadas': len(finales),
        'encabezados_sucios': ENCABEZADOS,
        'nombres_limpios': NOMBRES_LIMPIOS,
        'variantes_texto': {
            'municipio': {
                'en_archivo': conteo(p['municipio_txt'] for p in filas),
                'tras_paso_2': conteo(p['municipio_txt'] for p in pedidos),
            },
            'metodo_pago': {
                'en_archivo': conteo(p['metodo_txt'] for p in filas if p['metodo_txt'] is not None),
                'tras_paso_2': conteo(p['metodo_txt'] for p in pedidos if p['metodo_txt'] is not None),
            },
            'precio_unitario': {
                'con_signo_tras_paso_2': sum(1 for p in pedidos if p['precio_txt'] and p['precio_txt'].startswith('$')),
                'sin_signo_tras_paso_2': sum(1 for p in pedidos if p['precio_txt'] and not p['precio_txt'].startswith('$')),
                'ejemplos': sorted({p['precio_txt'] for p in pedidos if p['precio_txt']}),
            },
        },
        'faltantes_por_columna': {
            'en_archivo': {'precio_unitario': sum(1 for p in filas if p['precio_txt'] is None),
                           'metodo_pago': sum(1 for p in filas if p['metodo_txt'] is None),
                           'edad_cliente': sum(1 for p in filas if p['edad_txt'] is None)},
            'tras_paso_2': {'precio_unitario': N_FALTA_PRECIO, 'metodo_pago': N_FALTA_PAGO,
                            'edad_cliente': N_FALTA_EDAD},
        },
        'imposibles_por_columna': {
            'tiempo_entrega': {'total': len(TIEMPOS_IMPOSIBLES),
                               'valores': conteo(str(v) for v in TIEMPOS_IMPOSIBLES),
                               'regla': 'fuera de 1 a 180 minutos'},
            'calificacion': {'total': len(CALIFICACIONES_IMPOSIBLES),
                             'valores': conteo(str(v) for v in CALIFICACIONES_IMPOSIBLES),
                             'regla': 'fuera de 1 a 5'},
        },
        'pasos': {
            'E': {'forma_sin_parametros': [len(filas), 1], 'forma': [len(filas), 11]},
            '1': {'columnas': NOMBRES_LIMPIOS},
            '2': {'duplicados': N_DUPLICADOS, 'forma_despues': [len(pedidos), 11]},
            '3': {
                'municipio_antes': conteo(p['municipio_txt'] for p in pedidos),
                'municipio_despues': conteo(p['municipio'] for p in pedidos),
                'metodo_pago_antes': conteo(p['metodo_txt'] for p in pedidos if p['metodo_txt'] is not None),
                'metodo_pago_despues': conteo(p['metodo'] for p in pedidos if p['metodo_txt'] is not None),
                'metodo_pago_faltantes': N_FALTA_PAGO,
            },
            '4': {'precio_unitario_faltantes': N_FALTA_PRECIO,
                  'precio_min': min(v[1] for v in PRODUCTOS.values()),
                  'precio_max': max(v[1] for v in PRODUCTOS.values())},
            '5': {'forma_despues': [len(pedidos), 13], 'columnas_nuevas': ['mes', 'total'],
                  'fecha_min': min(p['fecha'] for p in pedidos).isoformat(),
                  'fecha_max': max(p['fecha'] for p in pedidos).isoformat(),
                  'total_faltantes': N_FALTA_PRECIO},
            '6': {'faltantes_antes': faltantes, 'sin_dato': N_FALTA_PAGO,
                  'filas_eliminadas': N_FALTA_PRECIO, 'forma_despues': [tras_paso_6, 13]},
            '7': {'tiempo_entrega_min': min(tiempos_sucios), 'tiempo_entrega_max': max(tiempos_sucios),
                  'calificacion_min': min(calificaciones_sucias), 'calificacion_max': max(calificaciones_sucias),
                  'filas_eliminadas_tiempo': len(TIEMPOS_IMPOSIBLES), 'forma_tras_tiempo': [tras_tiempo, 13],
                  'filas_eliminadas_calificacion': len(CALIFICACIONES_IMPOSIBLES),
                  'forma_despues': [len(finales), 13]},
            'L': {'forma': [len(finales), 13]},
        },
        'final': {
            'productos': conteo(p['producto'] for p in finales),
            'municipios': conteo(p['municipio'] for p in finales),
            'metodo_pago': conteo(canonico_pago(p) for p in finales),
            'edad_cliente_faltantes': sum(1 for p in finales if p['edad_txt'] is None),
            'ventas_por_mes': {str(m): ventas_mes[m] for m in range(1, 13)},
            'pedidos_por_mes': {str(m): sum(1 for p in finales if p['fecha'].month == m) for m in range(1, 13)},
        },
    }


def revisar_empates(catalogo):
    conteos = {
        'municipio_antes': catalogo['pasos']['3']['municipio_antes'],
        'municipio_despues': catalogo['pasos']['3']['municipio_despues'],
        'metodo_pago_antes': catalogo['pasos']['3']['metodo_pago_antes'],
        'metodo_pago_despues': catalogo['pasos']['3']['metodo_pago_despues'],
        'productos_final': catalogo['final']['productos'],
        'municipios_final': catalogo['final']['municipios'],
        'metodo_pago_final': catalogo['final']['metodo_pago'],
    }
    for nombre, valores in conteos.items():
        repetidos = [v for v, n in Counter(valores.values()).items() if n > 1]
        if repetidos:
            raise SystemExit(f'Semilla {SEMILLA}: empate en {nombre} con conteos {repetidos}; '
                             'value_counts ordenaría distinto en pandas 2.2 y 3.x')


def main():
    pedidos, filas, grupos = construir()
    catalogo = construir_catalogo(pedidos, filas, grupos)
    revisar_empates(catalogo)
    escribir_csv(filas)
    RUTA_CATALOGO.parent.mkdir(parents=True, exist_ok=True)
    with open(RUTA_CATALOGO, 'w', encoding='utf-8') as archivo:
        json.dump(catalogo, archivo, ensure_ascii=False, indent=2)
    print(f'{RUTA_CSV.name}: {len(filas)} filas sucias, {catalogo["filas_finales_esperadas"]} filas finales esperadas')
    print(f'{RUTA_CATALOGO.name}: escrito')


if __name__ == '__main__':
    main()
