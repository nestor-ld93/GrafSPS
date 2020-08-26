#!/bin/csh -f

#==================================================================================
echo ""
echo "+==========================================================================+"
echo "|                           SISMICIDAD v1.0.0                              |"
echo "+==========================================================================+"
echo "| -Generar un mapa de sismicidad en el Perú (a partir del cat. del NEIC)   |"
echo "| -Ultima actualizacion: 16/07/2020                                        |"
echo "| -Basado en los scripts de Cesar Jimenez y Cristobal Condori              |"
echo "+--------------------------------------------------------------------------+"
echo "| -Copyright (C) 2020  Nestor Luna Diaz                                    |"
echo "| -Contacto: nestor.luna@unmsm.edu.pe                                      |"
echo "+--------------------------------------------------------------------------+"
echo ""
#==================================================================================

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.

#==================================================================================

######################## Topografía y batimetría #############################
set grdfile = $22
#set grdfile = /media/nestor/Datos/Topografia_Batimetria/gebco/GridOne.nc
#set grdfile = /media/nestor/Datos/Topografia_Batimetria/gebco/Peru_2.nc
#set grdfile = /media/nestor/Datos/Topografia_Batimetria/etopo1_bed_Peru.grd

#################### Gradiente de topografía y batimetría ####################
set grdgrad = $23
#set grdgrad = /media/nestor/Datos/Topografia_Batimetria/gebco/Grad_GridOne.grd
#set grdgrad = /media/nestor/Datos/Topografia_Batimetria/gebco/Grad_Peru_2.grd
#set grdgrad = /media/nestor/Datos/Topografia_Batimetria/Grad_etopo1_Peru.grd

#################### Archivos de entrada y salida ############################
set folder  = $24
#set folder  = /media/nestor/Datos/Datos_contornos
set txt_sup = sismos_superficiales.txt
set txt_int = sismos_intermedios.txt
set txt_pro = sismos_profundos.txt

set psfile  = sismicidad.ps
set epsfile = sismicidad.eps
set cptfile = depth.cpt

makecpt -Cglobe > $cptfile

############################ Límites de los mapas  ###########################
set LAT1_1 = $13
set LAT2_1 = $14
set LON1_1 = $15
set LON2_1 = $16
set REGION1 = $LON2_1/$LON1_1/$LAT1_1/$LAT2_1
set AXIS1 = a4f2/a4f2WeSn
set SIZE1 = M15c

set LAT1_2 = $17
set LAT2_2 = $18
set LON1_2 = $19
set LON2_2 = $20
set REGION2 = $LON2_2/$LON1_2/$LAT1_2/$LAT2_2
set SIZE2 = M3c

######################### Variables a modificar  #############################
#set TITULO = "Sismicidad 1980-2019 Mw >= 5.0"
set TITULO_pre = $28
set TITULO = `echo $TITULO_pre | tr "%" " "`

set CATALOGO = $21          # Catálogo sísmico de entrada (formato NEIC sin ',').

set topo_bati = $11         # Variables: 1, 2, 3 (sin topo_bati, con topo_bati simple, con topo_bati compleja).
set escala_color = $10      # Variables: 0, 1 (sin escala de color, con escala de color de topo_bati).

set leyenda = $12           # Variables: 1, 2 (leyenda 1, leyenda 2).
set mini_mapa = $1          # Variables: 'si', 'no' (mostrar mini-mapa, no mostrar mini-mapa).
set fosa = $2               # Variables: 'si', 'no' (mostrar fosa, no mostrar fosa).
set fractura_mendana = $3   # Variables: 'si', 'no' (mostrar fractura, no mostrar fractura).
set dorsal_nazca = $4       # Variables: 'si', 'no' (mostrar dorsal, no mostrar dorsal).
set lim_dptos_ext = $5      # Variables: 'si', 'no' (mostrar dptos de .dat, no mostrar dptos de .dat).
set lim_dptos_gmt = $6      # Variables: 'si', 'no' (mostrar dptos de gmt, no mostrar dptos de gmt).

set nombres_dptos = $7      # Variables: 'si', 'no' (mostrar nombres de dptos, no mostrar nombres de dptos).
set nombres_paises = $8     # Variables: 'si', 'no' (mostrar nombres de paises, no mostrar nombres de paises).
set nombre_oceano = $9      # Variables: 'si', 'no' (mostrar nombre de oceano, no mostrar nombre de oceano).

set mostrar_sup  = $25     # Variables: 'si', 'no' (Graficar sismos superficiales, no graficar).
set mostrar_int  = $26     # Variables: 'si', 'no' (Graficar sismos intermedios, no graficar).
set mostrar_prof = $27     # Variables: 'si', 'no' (Graficar sismos profundos, no graficar).

gmtset ANOT_FONT_SIZE 12
gmtset LABEL_FONT_SIZE 14
gmtset HEADER_FONT_SIZE 14
gmtset PAPER_MEDIA A4

########### Separar sismos: superficiales, intermedios, profundos ############
cat $CATALOGO | awk '{if ($4 <= 60.0) print $1,$2,$3,$4,$5}' > $txt_sup
cat $CATALOGO | awk '{if ($4>60.0 && $4<=300.0) print $1,$2,$3,$4,$5}' > $txt_int
cat $CATALOGO | awk '{if ($4 > 300.0) print $1,$2,$3,$4,$5}' > $txt_pro

################# Sin topografía y batimetría  ###############################
if ($topo_bati == 1) then
    psbasemap -R$REGION1 -J$SIZE1 -B$AXIS1 -X3.0c -Y5.0c -P -K -V > $psfile
    if ($lim_dptos_gmt == 'si') then
        pscoast -J$SIZE1 -R$REGION1 -B$AXIS1 -Lf-82.5/-16.3/-82.5/15.3/200+lkm -S120/180/225 -G220/220/220 -Df -W1 -Na -P -K -V -O >> $psfile
        else
            pscoast -J$SIZE1 -R$REGION1 -B$AXIS1 -Lf-82.5/-16.3/-82.5/15.3/200+lkm -S120/180/225 -G220/220/220 -Df -W1 -N1 -P -K -V -O >> $psfile
    endif
endif
##############################################################################

############### Topografía y batimetría simple ###############################
if ($topo_bati == 2) then
    grdimage $grdfile -R$REGION1 -J$SIZE1 -C$cptfile -X3.0c -Y5.0c -P -K -V > ! $psfile
    if ($lim_dptos_gmt == 'si') then
        pscoast -J$SIZE1 -R$REGION1 -B$AXIS1 -Lf-82.5/-16.3/-82.5/15.3/200+lkm -Df -W1 -Na -P -K -V -O >> $psfile
        else
            pscoast -J$SIZE1 -R$REGION1 -B$AXIS1 -Lf-82.5/-16.3/-82.5/15.3/200+lkm -Df -W1 -N1 -P -K -V -O >> $psfile
    endif
    if ($escala_color == 1) then
        psscale -C$cptfile -D7.5/-1.0/12c/0.4ch -B4000/:m: -O -K -V  >> $psfile
    endif
endif
##############################################################################

############ Topografía y batimetría con gradiente ###########################
if ($topo_bati == 3) then
    grdimage $grdfile -R$REGION1 -J$SIZE1 -C$cptfile -I$grdgrad -X3.0c -Y5.0c -P -K -V > ! $psfile
    if ($lim_dptos_gmt == 'si') then
        pscoast -J$SIZE1 -R$REGION1 -B$AXIS1 -Lf-82.5/-16.3/-82.5/15.3/200+lkm -Df -W1 -Na -P -K -V -O >> $psfile
        else
            pscoast -J$SIZE1 -R$REGION1 -B$AXIS1 -Lf-82.5/-16.3/-82.5/15.3/200+lkm -Df -W1 -N1 -P -K -V -O >> $psfile
    endif
    if ($escala_color == 1) then
        psscale -C$cptfile -D7.5/-1.0/12c/0.4ch -B4000/:m: -O -K -V  >> $psfile
    endif
endif

###################### Departamentos Perú ####################################
if ($lim_dptos_ext == 'si') then
    awk '{print $1, $2}' $folder/deptos.dat | psxy -R -J -M -W1 -O -P -K >> $psfile
endif

############ Graficar Fosa, Fractura de Mendaña y Dorsal de Nazca ############
if ($fosa == 'si') then
    psxy $folder/Fosa.dat -R -J -M -Sf0.8c/0.15clt:0.8c -W2 -G0/0/0 -V -O -P -K >> $psfile
endif
if ($fractura_mendana == 'si') then
    psxy $folder/Mendana.gmt -R -J -M -W2/0/0/0 -O -K >> $psfile
endif
if ($dorsal_nazca == 'si') then
    psxy $folder/Nazca.dat -R -J -M -W2/0/0/0 -O -K >> $psfile
endif

################################ Sismicidad ##################################
if ($mostrar_sup == 'si') then
awk '$5 <  4.0              {print $3, $2}' $txt_sup | psxy -R$REGION1 -J$SIZE1 -Sc0.1 -G255/0/0 -W1 -P -O -K >> $psfile
awk '$5 >= 4.0 && $5 <= 4.9 {print $3, $2}' $txt_sup | psxy -R$REGION1 -J$SIZE1 -Sc0.2 -G255/0/0 -W1 -P -O -K >> $psfile
awk '$5 >= 5.0 && $5 <= 5.9 {print $3, $2}' $txt_sup | psxy -R$REGION1 -J$SIZE1 -Sc0.3 -G255/0/0 -W1 -P -O -K >> $psfile
awk '$5 >= 6.0 && $5 <= 6.9 {print $3, $2}' $txt_sup | psxy -R$REGION1 -J$SIZE1 -Sc0.4 -G255/0/0 -W1 -P -O -K >> $psfile
awk '$5 >= 7.0 && $5 <= 7.9 {print $3, $2}' $txt_sup | psxy -R$REGION1 -J$SIZE1 -Sc0.5 -G255/0/0 -W1 -P -O -K >> $psfile
awk '$5 >= 8.0              {print $3, $2}' $txt_sup | psxy -R$REGION1 -J$SIZE1 -Sc0.6 -G255/0/0 -W1 -P -O -K >> $psfile
endif

if ($mostrar_int == 'si') then
awk '$5 <  4.0              {print $3, $2}' $txt_int | psxy -R$REGION1 -J$SIZE1 -Sc0.1 -G255/255/0 -W1 -P -O -K >> $psfile
awk '$5 >= 4.0 && $5 <= 4.9 {print $3, $2}' $txt_int | psxy -R$REGION1 -J$SIZE1 -Sc0.2 -G255/255/0 -W1 -P -O -K >> $psfile
awk '$5 >= 5.0 && $5 <= 5.9 {print $3, $2}' $txt_int | psxy -R$REGION1 -J$SIZE1 -Sc0.3 -G255/255/0 -W1 -P -O -K >> $psfile
awk '$5 >= 6.0 && $5 <= 6.9 {print $3, $2}' $txt_int | psxy -R$REGION1 -J$SIZE1 -Sc0.4 -G255/255/0 -W1 -P -O -K >> $psfile
awk '$5 >= 7.0 && $5 <= 7.9 {print $3, $2}' $txt_int | psxy -R$REGION1 -J$SIZE1 -Sc0.5 -G255/255/0 -W1 -P -O -K >> $psfile
awk '$5 >= 8.0              {print $3, $2}' $txt_int | psxy -R$REGION1 -J$SIZE1 -Sc0.6 -G255/255/0 -W1 -P -O -K >> $psfile
endif

if ($mostrar_prof == 'si') then
awk '$5 <  4.0              {print $3, $2}' $txt_pro | psxy -R$REGION1 -J$SIZE1 -Sc0.1 -G0/0/255 -W1 -P -O -K >> $psfile
awk '$5 >= 4.0 && $5 <= 4.9 {print $3, $2}' $txt_pro | psxy -R$REGION1 -J$SIZE1 -Sc0.2 -G0/0/255 -W1 -P -O -K >> $psfile
awk '$5 >= 5.0 && $5 <= 5.9 {print $3, $2}' $txt_pro | psxy -R$REGION1 -J$SIZE1 -Sc0.3 -G0/0/255 -W1 -P -O -K >> $psfile
awk '$5 >= 6.0 && $5 <= 6.9 {print $3, $2}' $txt_pro | psxy -R$REGION1 -J$SIZE1 -Sc0.4 -G0/0/255 -W1 -P -O -K >> $psfile
awk '$5 >= 7.0 && $5 <= 7.9 {print $3, $2}' $txt_pro | psxy -R$REGION1 -J$SIZE1 -Sc0.5 -G0/0/255 -W1 -P -O -K >> $psfile
awk '$5 >= 8.0              {print $3, $2}' $txt_pro | psxy -R$REGION1 -J$SIZE1 -Sc0.6 -G0/0/255 -W1 -P -O -K >> $psfile
endif

########### Nombres de Departamentos en Perú y zonas fronterizas #############
if ($nombres_dptos == 'si') then
pstext -R -JM -Wwhite -O -K <<EOF>> $psfile
-80.63 -05.20 12 0 1 LT Piura
-79.03 -08.11 12 0 1 LT Trujillo
-77.08 -11.90 12 0 1 LT Lima
#-76.18 -13.71 12 0 1 LT Pisco
-75.60 -14.3 12 0 1 LT Ica
-71.54 -16.40 12 0 1 LT Arequipa
-71.00 -17.70 12 0 1 LT Tacna
EOF
endif

if ($nombres_paises == 'si') then
pstext -R -JM -Wwhite -O -K <<EOF>> $psfile
-80.20 -01.50 12 0 1 LT ECUADOR
-73.50 -00.50 12 0 1 LT COLOMBIA
-70.00 -08.00 12 0 1 LT BRASIL
-75.00 -10.00 12 0 1 LT PER\332
-70.00 -19.00 12 0 1 LT CHILE
-69.10 -15.40 12 0 1 LT BOLIVIA
EOF
endif

if ($nombre_oceano == 'si') then
pstext -R -JM -P -O -V -K <<EOF>> $psfile
-82.5 -12.0 14 305 1 LT OC\311ANO PAC\315FICO
EOF
endif

################################# Mini-mapa ##################################
if ($mini_mapa == 'si') then
#psxy -R -JM -W2 -P -O -V -K <<EOF>> $psfile
#-70.49  00.95
#-67.05  00.95
#-67.05  -4.12
#-70.49  -4.12
#-70.49  01.00
#EOF

pscoast -J$SIZE2 -R$REGION2 -Df -W1 -N1 -T-42.2/-48.8/1.4 -G180 -S120/180/225 -O -V -X11.95 -Y15.25 -K >> $psfile

psxy -R$REGION2 -J$SIZE2 -W5,255/0/0 -P -O -V -K <<EOF>> $psfile
$LON2_1  $LAT2_1
$LON1_1  $LAT2_1
$LON1_1  $LAT1_1
$LON2_1  $LAT1_1
$LON2_1  $LAT2_1
EOF
endif

########################## Leyenda 01: Sismicidad ############################
# G es el espacio vertical, V es la línea vertical, N establece el # de columnas, D dibuja línea horizontal.
# H es encabezado, L es etiqueta, S es símbolo, T es texto de párrafo, M es escala de mapa.
if ($mini_mapa == 'si') then
    set SIZE_LEYENDA = -8.3c/-12.50c/7.2c/2.7c/TC
endif
if ($mini_mapa == 'no') then
    set SIZE_LEYENDA = 3.65c/2.75c/7.2c/2.7c/TC
endif
if ($leyenda == 1 && $mostrar_sup == 'si' && $mostrar_int == 'si' && $mostrar_prof == 'si') then
pslegend <<END -Dx$SIZE_LEYENDA -R$REGION1 -J$SIZE1 -F -G255/255/255 -O >> $psfile
H 12 1 $TITULO
D 0 1p
S 0.1i c 0.1i red 0.25p 0.2i Superficial: 0-60 km
V 0 1p
S 0.1i c 0.1i yellow 0.25p 0.2i Intermedio: 60-300 km
V 0 1p
S 0.1i c 0.1i blue 0.25p 0.2i Profundo: 300-700 km
>
END
endif

if ($leyenda == 1 && $mostrar_sup == 'si' && $mostrar_int == 'si' && $mostrar_prof == 'no') then
pslegend <<END -Dx$SIZE_LEYENDA -R$REGION1 -J$SIZE1 -F -G255/255/255 -O >> $psfile
H 12 1 $TITULO
D 0 1p
S 0.1i c 0.1i red 0.25p 0.2i Superficial: 0-60 km
V 0 1p
S 0.1i c 0.1i yellow 0.25p 0.2i Intermedio: 60-300 km
>
END
endif

if ($leyenda == 1 && $mostrar_sup == 'si' && $mostrar_int == 'no' && $mostrar_prof == 'si') then
pslegend <<END -Dx$SIZE_LEYENDA -R$REGION1 -J$SIZE1 -F -G255/255/255 -O >> $psfile
H 12 1 $TITULO
D 0 1p
S 0.1i c 0.1i red 0.25p 0.2i Superficial: 0-60 km
V 0 1p
S 0.1i c 0.1i blue 0.25p 0.2i Profundo: 300-700 km
>
END
endif

if ($leyenda == 1 && $mostrar_sup == 'si' && $mostrar_int == 'no' && $mostrar_prof == 'no') then
pslegend <<END -Dx$SIZE_LEYENDA -R$REGION1 -J$SIZE1 -F -G255/255/255 -O >> $psfile
H 12 1 $TITULO
D 0 1p
S 0.1i c 0.1i red 0.25p 0.2i Superficial: 0-60 km
>
END
endif

if ($leyenda == 1 && $mostrar_sup == 'no' && $mostrar_int == 'si' && $mostrar_prof == 'si') then
pslegend <<END -Dx$SIZE_LEYENDA -R$REGION1 -J$SIZE1 -F -G255/255/255 -O >> $psfile
H 12 1 $TITULO
D 0 1p
S 0.1i c 0.1i yellow 0.25p 0.2i Intermedio: 60-300 km
V 0 1p
S 0.1i c 0.1i blue 0.25p 0.2i Profundo: 300-700 km
>
END
endif

if ($leyenda == 1 && $mostrar_sup == 'no' && $mostrar_int == 'si' && $mostrar_prof == 'no') then
pslegend <<END -Dx$SIZE_LEYENDA -R$REGION1 -J$SIZE1 -F -G255/255/255 -O >> $psfile
H 12 1 $TITULO
D 0 1p
S 0.1i c 0.1i yellow 0.25p 0.2i Intermedio: 60-300 km
>
END
endif

if ($leyenda == 1 && $mostrar_sup == 'no' && $mostrar_int == 'no' && $mostrar_prof == 'si') then
pslegend <<END -Dx$SIZE_LEYENDA -R$REGION1 -J$SIZE1 -F -G255/255/255 -O >> $psfile
H 12 1 $TITULO
D 0 1p
S 0.1i c 0.1i blue 0.25p 0.2i Profundo: 300-700 km
>
END
endif

########################## Leyenda 02: Sismicidad ############################
# G es el espacio vertical, V es la línea vertical, N establece el # de columnas, D dibuja línea horizontal.
# H es encabezado, L es etiqueta, S es símbolo, T es texto de párrafo, M es escala de mapa.
if ($mini_mapa == 'si') then
    set SIZE_LEYENDA = -8.1c/-11.8c/7.6c/3.4c/TC
endif
if ($mini_mapa == 'no') then
    set SIZE_LEYENDA = 3.85c/3.45c/7.6c/3.4c/TC
endif
if ($leyenda == 2 && $mostrar_sup == 'si' && $mostrar_int == 'si' && $mostrar_prof == 'si') then
pslegend <<END -Dx$SIZE_LEYENDA -R$REGION1 -J$SIZE1 -F -G255/255/255 -O >> $psfile
H 12 1 $TITULO
D 0 1p
H 11 0 Magnitud                  Profundidad
G 0.1
N 3
S 0.35c c 0.2c gray   0.4p 0.30i > 4.0
S -0.1c c 0.5c gray   0.4p 0.15i > 7.0
S -0.5c c 0.3c red    0.4p -0.05i 0-60 km
G 0.2
S 0.35c c 0.3c gray   0.4p 0.30i > 5.0
S -0.1c c 0.6c gray   0.4p 0.15i > 8.0
S -0.5c c 0.3c yellow 0.4p -0.05i 60-300 km
G 0.2
S 0.35c c 0.4c gray   0.4p 0.30i > 6.0
#S -0.1c c 0.7c gray   0.4p 0.15i > 9.0
#S -0.5c c 0.3c blue 0.4p -0.05i 300-700 km
S 2.03c c 0.3c blue   0.4p 0.95i 300-700 km
>
END
endif

if ($leyenda == 2 && $mostrar_sup == 'si' && $mostrar_int == 'si' && $mostrar_prof == 'no') then
pslegend <<END -Dx$SIZE_LEYENDA -R$REGION1 -J$SIZE1 -F -G255/255/255 -O >> $psfile
H 12 1 $TITULO
D 0 1p
H 11 0 Magnitud                  Profundidad
G 0.1
N 3
S 0.35c c 0.2c gray   0.4p 0.30i > 4.0
S -0.1c c 0.5c gray   0.4p 0.15i > 7.0
S -0.5c c 0.3c red    0.4p -0.05i 0-60 km
G 0.2
S 0.35c c 0.3c gray   0.4p 0.30i > 5.0
S -0.1c c 0.6c gray   0.4p 0.15i > 8.0
S -0.5c c 0.3c yellow 0.4p -0.05i 60-300 km
G 0.2
S 0.35c c 0.4c gray   0.4p 0.30i > 6.0
#S -0.1c c 0.7c gray   0.4p 0.15i > 9.0
#S -0.5c c 0.3c blue 0.4p -0.05i 300-700 km
>
END
endif

if ($leyenda == 2 && $mostrar_sup == 'si' && $mostrar_int == 'no' && $mostrar_prof == 'si') then
pslegend <<END -Dx$SIZE_LEYENDA -R$REGION1 -J$SIZE1 -F -G255/255/255 -O >> $psfile
H 12 1 $TITULO
D 0 1p
H 11 0 Magnitud                  Profundidad
G 0.1
N 3
S 0.35c c 0.2c gray   0.4p 0.30i > 4.0
S -0.1c c 0.5c gray   0.4p 0.15i > 7.0
S -0.5c c 0.3c red    0.4p -0.05i 0-60 km
G 0.2
S 0.35c c 0.3c gray   0.4p 0.30i > 5.0
S -0.1c c 0.6c gray   0.4p 0.15i > 8.0
S -0.5c c 0.3c blue   0.4p -0.05i 300-700 km
G 0.2
S 0.35c c 0.4c gray   0.4p 0.30i > 6.0
#S -0.1c c 0.7c gray   0.4p 0.15i > 9.0
#S -0.5c c 0.3c blue 0.4p -0.05i 300-700 km
>
END
endif

if ($leyenda == 2 && $mostrar_sup == 'si' && $mostrar_int == 'no' && $mostrar_prof == 'no') then
pslegend <<END -Dx$SIZE_LEYENDA -R$REGION1 -J$SIZE1 -F -G255/255/255 -O >> $psfile
H 12 1 $TITULO
D 0 1p
H 11 0 Magnitud                  Profundidad
G 0.1
N 3
S 0.35c c 0.2c gray   0.4p 0.30i > 4.0
S -0.1c c 0.5c gray   0.4p 0.15i > 7.0
S -0.5c c 0.3c red    0.4p -0.05i 0-60 km
G 0.2
S 0.35c c 0.3c gray   0.4p 0.30i > 5.0
S -0.1c c 0.6c gray   0.4p 0.15i > 8.0
G 0.2
S 0.35c c 0.4c gray   0.4p 0.30i > 6.0
#S -0.1c c 0.7c gray   0.4p 0.15i > 9.0
#S -0.5c c 0.3c blue 0.4p -0.05i 300-700 km
>
END
endif

if ($leyenda == 2 && $mostrar_sup == 'no' && $mostrar_int == 'si' && $mostrar_prof == 'si') then
pslegend <<END -Dx$SIZE_LEYENDA -R$REGION1 -J$SIZE1 -F -G255/255/255 -O >> $psfile
H 12 1 $TITULO
D 0 1p
H 11 0 Magnitud                  Profundidad
G 0.1
N 3
S 0.35c c 0.2c gray   0.4p 0.30i > 4.0
S -0.1c c 0.5c gray   0.4p 0.15i > 7.0
S -0.5c c 0.3c yellow 0.4p -0.05i 60-300 km
G 0.2
S 0.35c c 0.3c gray   0.4p 0.30i > 5.0
S -0.1c c 0.6c gray   0.4p 0.15i > 8.0
S -0.5c c 0.3c blue   0.4p -0.05i 300-700 km
G 0.2
S 0.35c c 0.4c gray   0.4p 0.30i > 6.0
#S -0.1c c 0.7c gray   0.4p 0.15i > 9.0
#S -0.5c c 0.3c blue 0.4p -0.05i 300-700 km
>
END
endif

if ($leyenda == 2 && $mostrar_sup == 'no' && $mostrar_int == 'si' && $mostrar_prof == 'no') then
pslegend <<END -Dx$SIZE_LEYENDA -R$REGION1 -J$SIZE1 -F -G255/255/255 -O >> $psfile
H 12 1 $TITULO
D 0 1p
H 11 0 Magnitud                  Profundidad
G 0.1
N 3
S 0.35c c 0.2c gray   0.4p 0.30i > 4.0
S -0.1c c 0.5c gray   0.4p 0.15i > 7.0
S -0.5c c 0.3c yellow 0.4p -0.05i 60-300 km
G 0.2
S 0.35c c 0.3c gray   0.4p 0.30i > 5.0
S -0.1c c 0.6c gray   0.4p 0.15i > 8.0
G 0.2
S 0.35c c 0.4c gray   0.4p 0.30i > 6.0
#S -0.1c c 0.7c gray   0.4p 0.15i > 9.0
#S -0.5c c 0.3c blue 0.4p -0.05i 300-700 km
>
END
endif

if ($leyenda == 2 && $mostrar_sup == 'no' && $mostrar_int == 'no' && $mostrar_prof == 'si') then
pslegend <<END -Dx$SIZE_LEYENDA -R$REGION1 -J$SIZE1 -F -G255/255/255 -O >> $psfile
H 12 1 $TITULO
D 0 1p
H 11 0 Magnitud                  Profundidad
G 0.1
N 3
S 0.35c c 0.2c gray   0.4p 0.30i > 4.0
S -0.1c c 0.5c gray   0.4p 0.15i > 7.0
S -0.5c c 0.3c blue   0.4p -0.05i 300-700 km
G 0.2
S 0.35c c 0.3c gray   0.4p 0.30i > 5.0
S -0.1c c 0.6c gray   0.4p 0.15i > 8.0
G 0.2
S 0.35c c 0.4c gray   0.4p 0.30i > 6.0
#S -0.1c c 0.7c gray   0.4p 0.15i > 9.0
#S -0.5c c 0.3c blue 0.4p -0.05i 300-700 km
>
END
endif

################################ Finalizando #################################
ps2eps $psfile -f
rm $cptfile $psfile
evince $epsfile &
