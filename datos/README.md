# Los datos

«Pan de Datos» es una panadería que **me inventé** para el curso: hace domicilios en el Valle
de Aburrá y cada fila es un pedido de 2025. Los datos son **sintéticos**: los genera
[`fuentes/generar_datos.py`](../fuentes/generar_datos.py), siempre iguales, así que ninguna
cifra es de una empresa real.

| Archivo | Filas | Cómo viene | Para qué lo usas |
|---|--:|---|---|
| [`domicilios_sucio.csv`](domicilios_sucio.csv) | 1.250 | separado con `;`, con coma decimal y en UTF-8 con BOM, tal como lo guarda Excel en Colombia | es la base con errores que limpiamos en el taller |
| [`domicilios_limpio.csv`](domicilios_limpio.csv) | 1.180 | separado con `,` y con punto decimal | es lo que te debe quedar al final; también sirve de punto de control si te atrasas |

## Qué trae cada columna (y qué le metí)

| Así aparece en el archivo | Así queda después de limpiar | Qué guarda | El error que tiene |
|---|---|---|---|
| `ID Pedido` | `id_pedido` | número del pedido | 40 filas repetidas |
| ` Fecha` | `fecha` | día del pedido (`dd/mm/aaaa`) | es texto, no fecha |
| `Municipio ` | `municipio` | Medellín, Bello, Itagüí, Envigado o Sabaneta | 19 formas distintas de escribirlos |
| `PRODUCTO` | `producto` | uno de 8 productos | ninguno |
| `Cantidad` | `cantidad` | unidades, de 1 a 6 | ninguno |
| `Precio Unitario` | `precio_unitario` | precio de una unidad | texto con `$` y punto de miles; 12 vacíos |
| `Metodo Pago` | `metodo_pago` | Efectivo, Nequi, Tarjeta o Daviplata | 14 formas de escribirlos; 36 vacíos |
| `Distancia KM` | `distancia_km` | kilómetros recorridos | viene con coma decimal |
| `Tiempo Entrega` | `tiempo_entrega` | minutos hasta entregar | 10 imposibles: −15, −8, −4, 0 y 999 |
| `Edad Cliente` | `edad_cliente` | edad en años | 60 vacíos |
| `Calificacion` | `calificacion` | nota del cliente, de 1 a 5 | 8 imposibles: 0, 10 y 45 |

Fíjate también en que todos los encabezados traen espacios o mayúsculas. Al final, la base
limpia tiene dos columnas más: `mes` y `total`.

## Lo que vas a descubrir con las gráficas

No te lo cuento todo, pero te adelanto lo que esconde la base:

- **Las ventas del año** suben en diciembre y en junio y julio, y bajan en febrero.
- **Lo que más se pide** es el pan de bono, y la torta de chocolate es lo que menos.
- **Los clientes** no son un solo grupo: hay estudiantes y hay familias.
- **La distancia y el tiempo** van de la mano: entre más lejos, más se demora el pedido.
- **Bello** es el municipio donde los domicilios tardan más y son más impredecibles.

Si quieres comprobar que la limpieza da exactamente lo que debe dar,
[`fuentes/verificar_limpieza.py`](../fuentes/verificar_limpieza.py) aplica las mismas líneas del
taller y hace 77 revisiones.
