# GrafSPS

[![GitHub release](https://img.shields.io/github/release/nestor-ld93/GrafSPS)](https://github.com/nestor-ld93/GrafSPS)
[![The Founders](https://img.shields.io/badge/authors-blue.svg)](https://github.com/nestor-ld93)

Programa con interfaz gráfica PyQt5 basado en scripts en lenguaje C-Shell y Bash con el objetivo de graficar mapas de sismicidad y perfiles sísmicos principalmente para Perú utilizando GMT4 (Generic Mapping Tools).

**Nota:** Los scripts fueron creados tomando como base el trabajo de César Jiménez y Cristobal Condori.

## CONTENIDO
- [VISIÓN GENERAL](#visión-general)
- [IMÁGENES PRINCIPALES](#imágenes-principales)
- [RECOMENDACIONES](#recomendaciones)
- [REQUISITOS MÍNIMOS](#requisitos-mínimos)
- [¿CÓMO DESCARGAR?](#cómo-descargar)
- [¿CÓMO EJECUTAR?](#cómo-ejecutar)
- [NOTAS IMPORTANTES](#notas-importantes)
- [RECURSOS EXTERNOS](#recursos-externos)
- [RECONOCIMIENTO](#reconocimiento)
- [LISTA DE CAMBIOS](#lista-de-cambios)

## VISIÓN GENERAL

**GrafSPS** permite realizar principalmente lo siguiente (en la región de Perú):

- Graficar un mapa de sismicidad sin topografía, con topografía simple y con topografía compleja (gradiente).
- Seleccionar el archivo de topografía-batimetría y gradiente (GRD/NC).
- Variar las coordenadas del mapa.
- Crear la línea de proyección del perfil y su región rectangular para 3 localizaciones distintas en función de parámetros iniciales.
- Crear perfiles sísmicos de profundidad en función de la región rectangular generada con una proyección de la topografía-batimetría.

**GrafSPS** permite obtener los siguientes archivos de salida:

1. **`sismicidad.eps`**: Mapa de sismicidad
1. **`sismicidad_perfil.eps`**: Mapa de sismicidad con las regiones rectangulares y la línea de perfil.
1. **`perfil_sismicidad_VARIABLE.eps`**: Perfil sísmico de profundidad. Donde VARIABLE toma el nombre de "norte", "centro" o "sur".

## IMÁGENES PRINCIPALES

![app menu](https://github.com/nestor-ld93/GrafSPS/blob/master/IMGs/Graf_SPS_01.jpg "Interfaz gráfica en PyQt5 del programa GrafSPS 01")
![app menu](https://github.com/nestor-ld93/GrafSPS/blob/master/IMGs/Graf_SPS_02.jpg "Interfaz gráfica en PyQt5 del programa GrafSPS 02")
![app menu](https://github.com/nestor-ld93/GrafSPS/blob/master/IMGs/sismicidad.jpg "Mapas de sismicidad generados")
![app menu](https://github.com/nestor-ld93/GrafSPS/blob/master/IMGs/pro_perfil_sismicidad_centro.jpg "Perfil generado")

## RECOMENDACIONES

- Utilizar el catálogo sísmico del NEIC (en formato CSV) y reemplazar las comas (',') por espacios (' ') antes de ingresarlo a GrafSPS.
- De utilizar otro catálogo, el usuario puede asignarle el formato del NEIC o modificar los scripts bash/shell para la correcta interpretación.
- Utilizar una distribución de GNU/Linux con escritorio KDE Plasma 5.12 o superior.

## REQUISITOS MÍNIMOS

- `GMT4`
- `sh` & `csh`
- `gawk` (Para Ubuntu 20.04 o superior)
- `ps2eps`
- `evince`
- `python3`
- `python3-pyqt5`
- `GNU Linux (Kernel 4.15) 64-bit`

## ¿CÓMO DESCARGAR?

Para obtener la última versión estable, descargue desde la pestaña [[Releases](https://github.com/nestor-ld93/GrafSPS/releases)].
Para obtener la última versión candidata a estable, descargue desde el botón [Code] o ejecute en un terminal:

    git clone https://github.com/nestor-ld93/GrafSPS

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

1. En cada inicio del programa es obligatorio seleccionar los archivos CSV y GRD/NC además de la carpeta contenedora de los datos de contorno. Pero, si el usuario lo desea, puede ingresar al archivo "`Launcher.py`" (con cualquier editor de texto) y modificar estas opciones para que se guarden por defecto (linea 56-92).
1. Por defecto, los archivos EPS se ejecutan en "`Evince`". El usuario puede cambiar este lector por el de su preferencia modificando las últimas lineas de los archivos bash/shell.
1. Muchos de los botones no se encuentran desactivados, por lo que si se realiza un procedimiento inadecuado el programa no realizará acción alguna. Para conocer el procedimiento adecuado, revisar la sección "`¿CÓMO EJECUTAR?`".
1. Se proporciona GrafSPS con la carpeta "`Datos_contornos`" (contiene los rasgos tectónicos para Perú).
1. No se proporciona los datos de topografía-batimetría. El usuario deberá conseguirlos de fuentes oficiales.
1. Mientras más grande sean los archivos GRD/NC, mayor será el tiempo computacional para generar los mapas y los perfiles (Este no es un problema de GrafSPS). Para solventarlo, el usuario puede recortar el archivo de topografía-batimetría para una región de interés.
1. Los parámetros del mapa de sismicidad con las regiones rectangulares son dependientes de las pestaña "`Sismicidad`".
1. En distribuciones basadas en el escritorio KDE Plasma, **GrafSPS** se adapta al esquema de colores seleccionado por el SO.

## RECURSOS EXTERNOS

1. "[GMT4 y documentación oficial de instalación](https://www.generic-mapping-tools.org/download/)"
1. "[GMT4 instalación semi-desatendida](https://github.com/nestor-ld93/GMT4)"
1. "[Catálogo sísmico del NEIC](http://earthquake.usgs.gov/earthquakes/map/)"
1. "[Topografía - ETOPO1 Global Relief Model](https://www.ngdc.noaa.gov/mgg/global/)"
1. "[Batimetría - GEBCO The General Bathymetric Chart of the Oceans](https://www.gebco.net/data_and_products/gridded_bathymetry_data/)"

## RECONOCIMIENTO

GMT relies on several other Open Source software libraries, programs and data for its
operation.  We gratefully acknowledge the importance to GMT of these products.
GMT may be linked with these libraries (* means optional):

[Network Common Data Form (netCDF)](https://www.unidata.ucar.edu/software/netcdf/),
[Geospatial Data Abstraction Library (GDAL*)](https://gdal.org),
[Perl Compatible Regular Expressions (PCRE*)](https://www.pcre.org),
[Fastest Fourier Transform in the West (FFTW*)](http://www.fftw.org),
[Linear Algebra Package (LAPACK*)](http://www.netlib.org/lapack/),
[Basic Linear Algebra Subprograms (BLAS*)](http://www.netlib.org/blas/),
[GLIB*](https://developer.gnome.org/glib/), and
[ZLIB*](https://www.zlib.net). GMT may call these executables:
GDAL (ogr2ogr, gdal_translate), [Ghostscript](https://www.ghostscript.com),
[FFmpeg](https://www.ffmpeg.org),
[xdg-open](https://www.freedesktop.org/wiki/Software/xdg-utils/), and
[GraphicsMagick](http://www.graphicsmagick.org).

GMT uses (or can access) data derived from these sources:

- [Scientific Color Maps (CPT)](http://www.fabiocrameri.ch/visualisation.php)
- [Earth 15" DEM](http://dx.doi.org/10.1029/2019EA000658)
- [Earth 1" SRTM DEM](https://lpdaac.usgs.gov/products/srtmgl3v003)
- [Earth 1' crustal age](http://dx.doi.org/10.1029/2020GC009214)
- [Earth 30" Blue Marble images](https://visibleearth.nasa.gov/images/57752/blue-marble-land-surface-shallow-water-and-shaded-topography)
- [Earth 30" Black Marble images](https://earthobservatory.nasa.gov/features/NightLights/page3.php)

## LISTA DE CAMBIOS

- (v1.0.0) [25/08/2020] Lanzamiento inicial.
- (v1.0.1) [08/12/2022] Corregido generador de coordenadas en versiones actuales de sh.
- (v1.1.0) [08/12/2022] Los textos editables ahora aceptan caracteres con tildes y ñ (´,ñ) en minúsculas y mayúsculas.
- (v1.1.0) [08/12/2022] Agregado opción para utilizar paleta de colores personalizada.
- (v1.1.0) [08/12/2022] Agregado opción "3) Opciones avanzadas".
- (v1.1.0) [08/12/2022] Agregado textos editables con parámetros de personalización en "3) Opciones avanzadas".
- (v1.1.0) [08/12/2022] Agregado textos editables para modificar el contenido de la Leyenda 1.
- (v1.1.0) [08/12/2022] Agregado opción para mostrar escala del mapa en "3) Opciones avanzadas".
- (v1.1.0) [08/12/2022] Agregado opciones de grillado para el mapa.
