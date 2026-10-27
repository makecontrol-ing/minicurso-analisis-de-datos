# Cómo armé el curso

Aquí está todo lo que usé para construir el material. Si quieres cambiar la base de datos, los
notebooks o la presentación, este es el lugar. El diseño completo del curso (para quién es, la
agenda, los errores que metí, las reglas para que el código fuera simple y el estilo visual)
lo escribí en [`especificacion.md`](especificacion.md).

| Archivo | Para qué sirve |
|---|---|
| [`generar_datos.py`](generar_datos.py) | crea `datos/domicilios_sucio.csv` (siempre igual) y anota cada error en [`contenido/catalogo_errores.json`](contenido/catalogo_errores.json) |
| [`verificar_limpieza.py`](verificar_limpieza.py) | aplica la limpieza del taller línea por línea y revisa que todo dé lo que debe dar (77 revisiones) |
| [`construir_notebooks.py`](construir_notebooks.py) | arma los dos notebooks a partir de una sola definición; con `--ejecutar` también corre la solución |
| [`figuras_teoria.py`](figuras_teoria.py) | hace las gráficas de ejemplo de la parte de teoría (`figuras/teoria_*.png`) |
| [`figuras_taller.py`](figuras_taller.py) | corre el código de cada gráfica del taller y guarda las imágenes (`figuras/taller_*.png`) |
| [`construir_presentacion.py`](construir_presentacion.py) | arma el `.pptx` a partir de [`contenido/teoria.json`](contenido/teoria.json) y [`contenido/taller.json`](contenido/taller.json) |
| [`exportar.ps1`](exportar.ps1) | pasa el `.pptx` a PDF con PowerPoint (en Windows) |
| [`renderizar.py`](renderizar.py) | saca una imagen de cada diapositiva para revisarlas |
| [`fondos/`](fondos) | los fondos de la portada, el contenido y el cierre |
| [`requirements.txt`](requirements.txt) | lo que necesitas instalar para correr estos scripts |

Si quieres regenerar todo, este es el orden, desde la raíz del repositorio:

```sh
python -m pip install -r fuentes/requirements.txt
python fuentes/generar_datos.py
python fuentes/verificar_limpieza.py
python fuentes/construir_notebooks.py --ejecutar
python fuentes/figuras_teoria.py
python fuentes/figuras_taller.py
python fuentes/construir_presentacion.py
powershell -ExecutionPolicy Bypass -File fuentes/exportar.ps1
```
