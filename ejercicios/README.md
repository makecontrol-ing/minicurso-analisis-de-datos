# Para seguir practicando

Si llegaste hasta aquí, ya sabes limpiar una base y graficarla. Ahora te propongo seguir con
la misma base limpia, [`datos/domicilios_limpio.csv`](../datos/domicilios_limpio.csv), y el
notebook del taller ([`notebooks/`](../notebooks)).

Un consejo antes de empezar: **antes de ejecutar cada cosa, escribe qué crees que va a pasar.**
Después lo ejecutas y comparas. Ahí es donde de verdad se aprende.

Escríbelo igual que en el taller: una idea por celda, pocas líneas y nada complicado.

## Ejercicios

| # | La pregunta | Una pista | En qué fijarte |
|:-:|---|---|---|
| 1 | **¿Qué municipio vende más?** ¿Es el mismo que tiene más pedidos? | `df.groupby('municipio')['total'].sum().plot(kind='barh')` y compáralo con `df['municipio'].value_counts()` | Tener más pedidos no siempre significa vender más. Mira cuánto vale cada pedido. |
| 2 | **¿Qué día de la semana se piden más domicilios?** | Cuando lees la base limpia, `fecha` vuelve a ser texto. Usa `pd.to_datetime(df['fecha'])`, luego `.dt.day_name()` y después `value_counts()` | ¿Las barras quedan en el orden de la semana o en el de los conteos? |
| 3 | **¿Con qué método de pago se gasta más por pedido?** | `df.groupby('metodo_pago')['total'].mean()` | ¿Qué haces con «Sin dato»? ¿Lo tienes en cuenta en tu conclusión? |
| 4 | **El reto del taller:** ¿califican peor cuando el domicilio se demora? | La última celda del notebook: `groupby('calificacion')['tiempo_entrega'].mean()` | ¿Una cosa causa la otra o solo van juntas? |
| 5 | **¿Y si no quito los duplicados?** Calcula las ventas del año con y sin el paso 2. | `df['total'].sum()` antes y después de `drop_duplicates()` | ¿Cuánta plata «aparece» que nunca se vendió? |
| 6 | **Otra forma de tratar los vacíos.** En el paso 6, en vez de borrar los pedidos sin precio, ponles el precio típico de su producto. | Empieza con `df.groupby('producto')['precio_unitario'].median()` | Compara las ventas totales con las del taller. ¿Cuál decisión te parece más honesta? |
| 7 | **Una gráfica que engaña.** Repite la de ventas por mes, pero con el eje empezando en cero. | Agrega `ylim=0` dentro de `.plot(...)` | ¿Diciembre sigue pareciendo que «se dispara»? ¿Cuál versión mostrarías y por qué? |
| 8 | **Haz de auditor.** Demuestra con código que en la base limpia ya no queda ninguno de los siete errores. | `df.duplicated().sum()`, `value_counts()`, `df.dtypes`, `df.isna().sum()`, `df.describe()` | Escribe una frase por error con la prueba de que ya no está. |

## Proyectos con datos reales

En el taller los datos eran inventados para que todos encontráramos los mismos errores. El
siguiente paso, y el más divertido, es hacer lo mismo con datos de verdad, donde nadie te
avisa qué está mal. El camino es el mismo de la clase: **pregunta → extraer → transformar →
cargar → analizar → comunicar**.

### 1 · La calidad del aire en el Valle de Aburrá

**La idea.** Elige una pregunta concreta sobre el PM2.5, por ejemplo en qué meses y a qué horas
se pone peor el aire, y respóndela con las mediciones del [SIATA](https://siata.gov.co).

**Cómo hacerlo.**
1. Escribe la pregunta y escoge una o dos estaciones.
2. Descarga los datos y revisa el separador, los decimales, las fechas y los datos que faltan.
3. Decide qué hacer con los vacíos y con los valores imposibles, como negativos o ceros sospechosos.
4. Responde con una gráfica de líneas y una de caja por mes, y escribe tu conclusión en una sola frase.

### 2 · Los datos abiertos de tu ciudad

**La idea.** Escoge un conjunto de datos de [datos.gov.co](https://www.datos.gov.co) o del portal
[MEData](https://medata.gov.co) de Medellín (movilidad, accidentes, precios, educación) y cuenta
una historia con tres gráficas.

**Cómo hacerlo.**
1. Escribe tres preguntas antes de mirar los datos.
2. Pasa la lista de chequeo de la clase: lectura, nombres, duplicados, texto, tipos, faltantes y valores imposibles.
3. Anota cada decisión de limpieza en una celda de texto: qué encontraste y qué hiciste.
4. Cuéntalo en cinco minutos usando las seis preguntas para leer una gráfica.
