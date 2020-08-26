# GrafSPS
Programa con interfaz gráfica PyQt5 basado en scripts en lenguaje C-Shell y Bash con el objetivo de graficar mapas de sismicidad y perfiles sísmicos principalmente para Perú utilizando GMT4 (Generic Mapping Tools).

**Nota:** Los scripts fueron creados tomando como base el trabajo de César Jimenez y Cristobal Condori.

**GrafSPS** permite realizar principalmente lo siguiente (en la región de Perú):

- Graficar un mapa de sismicidad sin topografía, con topografía simple y con topografía compleja (gradiente).
- Seleccionar el archivo de topografía-batimetría y gradiente (GRD/NC).
- Variar las coordenadas del mapa.
- Crear la línea de proyección del perfil y su región rectangular para 3 localizaciones distintas en función de parámetros iniciales.
- Crear perfiles sísmicos de profundidad en función de la región rectangular generada con una proyección de la topografía-batimetría.

**GrafSPS** permite obtener los siguientes archivos de salida:

1. **sismicidad.eps**: Mapa de sismicidad
1. **sismicidad_perfil.eps**: Mapa de sismicidad con las regiones rectangulares y la línea de perfil.
1. **perfil_sismicidad_VARIABLE.eps**: Perfil sísmico de profundidad. Donde VARIABLE toma el nombre de "norte", "centro" o "sur".

## IMÁGENES PRINCIPALES

![app menu](https://lh3.googleusercontent.com/-JV36HEQP6EA/XuKy0VxFBbI/AAAAAAAABEI/25aU9_BJJN03-nFN8JIx2SkhxLpZvhayQCLcBGAsYHQ/h633/Graf_SPS_01.png "Interfaz gráfica en PyQt5 del programa GrafSPS 01")
![app menu](https://lh3.googleusercontent.com/-B7bYTk48oy4/XuKy0l26thI/AAAAAAAABEE/HSbr7G7h0isgPj2q7A_Q_sQos8tMQv1tACLcBGAsYHQ/h633/Graf_SPS_02.png "Interfaz gráfica en PyQt5 del programa GrafSPS 02")
![app menu](https://lh3.googleusercontent.com/-RR__zVYSsPk/XuKy1oEQK1I/AAAAAAAABEQ/hVQzU4EQZwclcMI3tOVG8JqvkqgTqamfQCLcBGAsYHQ/h633/sismicidad.png "Mapas de sismicidad generados")
![app menu](https://lh3.googleusercontent.com/-WJCabVVK2kA/XuKy0kVcDBI/AAAAAAAABEM/ajiCjpiURUQKpYlAyaQCN0u_K78gYyppACLcBGAsYHQ/h450/pro_perfil_sismicidad_centro.png "Perfil generado")

## RECOMENDACIONES
- Utilizar el catálogo sísmico del NEIC (en formato CSV) y eliminar las comas (',') antes de ingresarlo a GrafSPS.
- De utilizar otro catálogo, el usuario puede asignarle el formato del NEIC o modificar los scripts bash/shell para la correcta interpretación.

## REQUISITOS MÍNIMOS
- GMT4
- Shell y C-Shell
- gawk (Para Ubuntu 20.04 o superior)
- ps2eps
- Evince
- python3
- python3-pyqt5
- GNU Linux (Kernel 4.15) 64-bit [Se recomienda una distribución con KDE Plasma 5.12 o superior]

## ¿CÓMO DESCARGAR?
- Para obtener la última versión estable, descargue desde la pestaña [[Releases](https://github.com/nestor-ld93/GrafSPS/releases)].
- Para obtener la última versión candidata a estable, descargue desde el botón [Code] o ejecute en un terminal:
`git clone https://github.com/nestor-ld93/GrafSPS`

## ¿CÓMO EJECUTAR?
1. Descargar un catálogo sísmico del NEIC en formato CSV. Posteriormente, modificarlo para reemplazar las comas (',') por espacios (' ').
1. Ejecutar en un terminal: `./Launcher.py`. Una vez abierta la interfaz gráfica, ingresar a la pestaña "`Sismicidad`".
1. Seleccionar el archivo del catálogo sísmico (CSV) y la carpeta contenedora de los datos de contorno (ASCCI).
1. Desplegar la opción "`2) Parámetros de personalización`".
1. Modificar los parámetros a su preferencia. Al seleccionar el tipo de topografía, si selecciona la opción "`Simple`" o "`Gradiente`", desplegar la opción "`1) Archivos externos`" para agregar los archivos GRD/NC necesarios.
1. Clic en "`Graficar Sismicidad`". Inmediatamente debería visualizar el mapa de sismicidad.
1. Ingresar a la pestaña "`Perfiles sísmicos`".
1. Modificar los parámetros iniciales para generar las coordenadas de la región rectangular y la línea de perfil.
1. Clic en "`Generar coordenadas`".
1. Clic en "`Graficar sismicidad con rectángulos`". Si el resultado de las regiones rectangulares no son los deseados, puede volver a modificar los parámetros iniciales (no olvidar dar clic en "`Generar coordenadas`" y en "`Graficar sismicidad con rectángulos`" al momento de realizar la modificación).
1. Seleccionar un archivo de topografía-batimetría (GRD/NC) para realizar la proyección sobre la línea de perfil generada.
1. Seleccionar la región a graficar ("`Norte`", "`Centro`" o "`Sur`") y otras opciones adicionales.
1. Clic en "`Graficar Perfil Sísmico`".

## NOTAS IMPORTANTES
1. En cada inicio del programa es obligatorio seleccionar los archivos CSV y GRD/NC además de la carpeta contenedora de los datos de contorno. Pero, si el usuario lo desea, puede ingresar al archivo "`Launcher.py`" (con cualquier editor de texto) y modificar estas opciones para que se guarden por defecto (linea 56-83).
1. Por defecto, los archivos EPS se ejecutan en "`Evince`". El usuario puede cambiar este lector por el de su preferencia modificando las últimas lineas de los archivos bash/shell.
1. Muchos de los botones no se encuentran desactivados, por lo que si se realiza un procedimiento inadecuado el programa no realizará acción alguna. Para conocer el procedimiento adecuado, revisar la sección "`¿CÓMO EJECUTAR?`".
1. Se proporciona GrafSPS con la carpeta "`Datos_contornos`" (contiene los rasgos tectónicos para Perú).
1. No se proporciona los datos de topografía-batimetría. El usuario deberá conseguirlos de fuentes oficiales.
1. Mientras más grande sean los archivos GRD/NC, mayor será el tiempo computacional para generar los mapas y los perfiles (Este no es un problema de GrafSPS). Para solventarlo, el usuario puede recortar el archivo de topografía-batimetría para una región de interés.
1. Los parámetros del mapa de sismicidad con las regiones rectangulares son dependientes de las pestaña "`Sismicidad`".
1. En distribuciones basadas en el escritorio KDE Plasma, **GrafSPS** se adapta al esquema de colores seleccionado por el SO.

## RECURSOS EXTERNOS
1. "[GMT4 y documentación oficial de instalación](https://www.generic-mapping-tools.org/download/)"
1. "[Catálogo sísmico del NEIC](http://earthquake.usgs.gov/earthquakes/map/)"
1. "[Topografía - ETOPO1 Global Relief Model](https://www.ngdc.noaa.gov/mgg/global/)"
1. "[Batimetría - GEBCO The General Bathymetric Chart of the Oceans](https://www.gebco.net/data_and_products/gridded_bathymetry_data/)"

## LISTA DE CAMBIOS
- (v1.0.0) [25/08/2020] Lanzamiento inicial.
