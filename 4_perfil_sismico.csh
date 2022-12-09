#!/bin/csh -f

#==================================================================================
echo ""
echo "+==========================================================================+"
echo "|                           PERFIL SISMICO v1.1.0                          |"
echo "+==========================================================================+"
echo "| -Grafica el perfil de profundidad con datos de topografia (GRD/NC)       |"
echo "| -Ultima actualizacion: 17/10/2020                                        |"
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
set grdfile = $1
#set grdfile = /media/nestor/Datos/Topografia_Batimetria/gebco/GridOne.nc
#set grdfile = /media/nestor/Datos/Topografia_Batimetria/gebco/Peru_2.nc
#set grdfile = /media/nestor/Datos/Topografia_Batimetria/ETOPO1_Bed_g_gmt4.grd

#################### Archivos de entrada y salida ############################
set txt_sup = sismos_superficiales.txt
set txt_int = sismos_intermedios.txt
set txt_pro = sismos_profundos.txt
set file_coord = coordenadas_perfiles.txt

#set psfile  = perfil_sismicidad.ps
#set epsfile = perfil_sismicidad.eps

set linea_perfil = linea_perfil.txt
set linea_topo_bati = linea_topo_bati.txt

######################### Variables a modificar  #############################
#set TITULO_leyenda = "Sismicidad 1980-2019 Mw >= 5.0"
set TITULO_leyenda_pre = $10
set TITULO_leyenda = `echo $TITULO_leyenda_pre | tr "%" " "`

#set Label_x = "Distancia\040(km)"
set Label_x = $14
set Label_y1 = $15
set Label_y2 = $16

set Titulo_perfil_norte =  "$17\040AA\47"
set Titulo_perfil_centro = "$17\040BB\47"
set Titulo_perfil_sur    = "$17\040CC\47"

set leyenda = $3           # Variables: 'si', 'no' (mostrar leyenda, no mostrar leyenda)
set perfil_region = $2     # Variables: 'norte', 'centro', 'sur'
set L1 = $4
set L2 = $5
set L3 = $6

set mostrar_sup  = $7     # Variables: 'si', 'no' (Graficar sismos superficiales, no graficar).
set mostrar_int  = $8     # Variables: 'si', 'no' (Graficar sismos intermedios, no graficar).
set mostrar_prof = $9     # Variables: 'si', 'no' (Graficar sismos profundos, no graficar).

set Texto_leyenda_01_pre = $11
set Texto_leyenda_01 = `echo $Texto_leyenda_01_pre | tr "%" " "`

set Texto_leyenda_02_pre = $12
set Texto_leyenda_02 = `echo $Texto_leyenda_02_pre | tr "%" " "`

set Texto_leyenda_03_pre = $13
set Texto_leyenda_03 = `echo $Texto_leyenda_03_pre | tr "%" " "`

gmtset HEADER_FONT_SIZE 14
gmtset ANOT_FONT_SIZE 12
gmtset LABEL_FONT_SIZE 14
gmtset GRID_PEN_PRIMARY	= 0.25p/121/128/129

if ($perfil_region == 'norte') then
    set L = $L1
endif
if ($perfil_region == 'centro') then
    set L = $L2
endif
if ($perfil_region == 'sur') then
    set L = $L3
endif

set resto_L = `echo "$L%50.0" | bc` # Corrección para el límite final del eje x si L no es entero.
if ($resto_L != 0) then
    set L = `echo "scale=2; $L-$resto_L+50.0" | bc` 
endif
set REGION1 = 0/$L/$26/$27
set SIZE1 = 17.0c/2.0c
set div_x = $18
set grid_x = $19
set div_y1 = $20
set grid_y1 = $21
set div_y2 = $22
set grid_y2 = $23

set REGION2 = 0/$L/$24/$25
set AXIS2 = "a{$div_x}g{$grid_x}:"$Label_x":/a${div_y1}g{$grid_y1}:"$Label_y1":SW"
set SIZE2 = 17.0c/7.0c

set N = `awk 'END {print NR}' $file_coord` # Numero de filas del archivo.
set i = 1                                  # Contador del bucle.

########################## Extraer coordenadas ###############################
while ($i <= $N)
    eval `awk 'NR=='$i'{print "set lon0="$1}' $file_coord`
    eval `awk 'NR=='$i'{print "set lat0="$2}' $file_coord`
    eval `awk 'NR=='$i'{print "set lonf="$3}' $file_coord`
    eval `awk 'NR=='$i'{print "set latf="$4}' $file_coord`
    eval `awk 'NR=='$i'{print "set x1="$5}' $file_coord`
    eval `awk 'NR=='$i'{print "set y1="$6}' $file_coord`
    eval `awk 'NR=='$i'{print "set x2="$7}' $file_coord`
    eval `awk 'NR=='$i'{print "set y2="$8}' $file_coord`
    eval `awk 'NR=='$i'{print "set x3="$9}' $file_coord`
    eval `awk 'NR=='$i'{print "set y3="$10}' $file_coord`
    eval `awk 'NR=='$i'{print "set x4="$11}' $file_coord`
    eval `awk 'NR=='$i'{print "set y4="$12}' $file_coord`
    eval `awk 'NR=='$i'{print "set W_2="$13}' $file_coord`
    
    if ($i == 1 && $perfil_region == 'norte') then
        set p1 = $lon0/$lat0        # Punto 1 (WE): (Longitud, Latitud)
        set p2 = $lonf/$latf        # Punto 2 (WE): (Longitud, Latitud)
        set W_mitad = $W_2         # Ancho del perfil/2 (W = 400 km corresponde a  W_mitad = 200)
        set AXIS1 = a{$div_x}g{$grid_x}:."$Titulo_perfil_norte":/a{$div_y2}g{$grid_y2}:"$Label_y2":W
        set psfile  = perfil_sismicidad_norte.ps
        set epsfile = perfil_sismicidad_norte.eps
    endif

    if ($i == 2 && $perfil_region == 'centro') then
        set p1 = $lon0/$lat0        # Punto 1 (WE): (Longitud, Latitud)
        set p2 = $lonf/$latf        # Punto 2 (WE): (Longitud, Latitud)
        set W_mitad = $W_2         # Ancho del perfil/2 (W = 400 km corresponde a  W_mitad = 200)
        set AXIS1 = a{$div_x}g{$grid_x}:."$Titulo_perfil_centro":/a{$div_y2}g{$grid_y2}:"$Label_y2":W
        set psfile  = perfil_sismicidad_centro.ps
        set epsfile = perfil_sismicidad_centro.eps
    endif

    if ($i == 3 && $perfil_region == 'sur') then
        set p1 = $lon0/$lat0        # Punto 1 (WE): (Longitud, Latitud)
        set p2 = $lonf/$latf        # Punto 2 (WE): (Longitud, Latitud)
        set W_mitad = $W_2          # Ancho del perfil/2 (W = 400 km corresponde a  W_mitad = 200)
        set AXIS1 = a{$div_x}g{$grid_x}:."$Titulo_perfil_sur":/a{$div_y2}g{$grid_y2}:"$Label_y2":W
        set psfile  = perfil_sismicidad_sur.ps
        set epsfile = perfil_sismicidad_sur.eps
    endif
    
    @ i = $i + 1
end

################## Generar línea (puntos) del perfil #########################
project -C$p1 -E$p2 -G.5 -Dd -Q > $linea_perfil

##### Extrae valores de la topografia en función de la línea del perfil ######
grdtrack $linea_perfil -G$grdfile | awk '{print $3, $4 }' > $linea_topo_bati

#################### Graficar el pefil de la topografia ######################
psbasemap -JX$SIZE1 -R$REGION1 -B$AXIS1 -P -K -X3.0c -Y15.0c  > $psfile
awk '{print $1,$2*0.001 }' $linea_topo_bati | psxy -R$REGION1 -JX$SIZE1 -W4/10/10/10 -K -O -P >> $psfile

################# Texto (SW, NE) - Ahora es: AA', BB', CC' ###################
set L1 = `echo "scale=2; $L-20.0" | bc`  # Operación para ubicar el texto "NE" (Ahora es: AA', BB', CC').
if ($perfil_region == 'norte') then
    echo 0 10 12 0 0 5 "A" | pstext -R$REGION1 -JX$SIZE1 -V -N -O -K >> $psfile
    echo $L1 10 12 0 0 5 "A\47" | pstext -R$REGION1 -JX$SIZE1 -V -N -O -K >> $psfile
endif

if ($perfil_region == 'centro') then
    echo 0 10 12 0 0 5 "B" | pstext -R$REGION1 -JX$SIZE1 -V -N -O -K >> $psfile
    echo $L1 10 12 0 0 5 "B\47" | pstext -R$REGION1 -JX$SIZE1 -V -N -O -K >> $psfile
endif

if ($perfil_region == 'sur') then
    echo 0 10 12 0 0 5 "C" | pstext -R$REGION1 -JX$SIZE1 -V -N -O -K >> $psfile
    echo $L1 10 12 0 0 5 "C\47" | pstext -R$REGION1 -JX$SIZE1 -V -N -O -K >> $psfile
endif
############ Perfil de Sismos (Longitud, Latitud, Profundidad) ###############
psbasemap -JX$SIZE2 -R$REGION2 -B$AXIS2 -P -K -X0 -Y-7.5c -O >> $psfile

if ($mostrar_sup == 'si') then
awk '{print $3, $2, $4*-1}' $txt_sup | pscoupe -JX$SIZE2 -R$REGION2 \
-Aa$p1/$p2/90/$W_mitad/0/-60 -sc0.28 -G255/0/0 -L1 -P -O -K >> $psfile
endif

if ($mostrar_int == 'si') then
awk '{print $3, $2, $4*-1}' $txt_int | pscoupe -JX$SIZE2 -R$REGION2 \
-Aa$p1/$p2/90/$W_mitad/0/-60 -sc0.28 -G255/255/0 -L1 -P -O -K >> $psfile
endif

if ($mostrar_prof == 'si') then
awk '{print $3, $2, $4*-1}' $txt_pro | pscoupe -JX$SIZE2 -R$REGION2 \
-Aa$p1/$p2/90/$W_mitad/0/-60 -sc0.28 -G0/0/255 -L1 -P -O -K >> $psfile
endif

########################## Leyenda 01: Sismicidad ############################
# G es el espacio vertical, V es la línea vertical, N establece el # de columnas, D dibuja línea horizontal.
# H es encabezado, L es etiqueta, S es símbolo, T es texto de párrafo, M es escala de mapa.
set SIZE_LEYENDA = 3.65c/2.55c/7.2c/2.5c/TC

if ($leyenda == 'si' && $mostrar_sup == 'si' && $mostrar_int == 'si' && $mostrar_prof == 'si') then
pslegend <<END -Dx$SIZE_LEYENDA -R$REGION2 -JX$SIZE2 -F -G255/255/255 -O >> $psfile
H 12 1 $TITULO_leyenda
D 0 1p
S 0.1i c 0.1i red 0.25p 0.2i $Texto_leyenda_01
V 0 1p
S 0.1i c 0.1i yellow 0.25p 0.2i $Texto_leyenda_02
V 0 1p
S 0.1i c 0.1i blue 0.25p 0.2i $Texto_leyenda_03
>
END
endif

if ($leyenda == 'si' && $mostrar_sup == 'si' && $mostrar_int == 'si' && $mostrar_prof == 'no') then
pslegend <<END -Dx$SIZE_LEYENDA -R$REGION2 -JX$SIZE2 -F -G255/255/255 -O >> $psfile
H 12 1 $TITULO_leyenda
D 0 1p
S 0.1i c 0.1i red 0.25p 0.2i $Texto_leyenda_01
V 0 1p
S 0.1i c 0.1i yellow 0.25p 0.2i $Texto_leyenda_02
>
END
endif

if ($leyenda == 'si' && $mostrar_sup == 'si' && $mostrar_int == 'no' && $mostrar_prof == 'si') then
pslegend <<END -Dx$SIZE_LEYENDA -R$REGION2 -JX$SIZE2 -F -G255/255/255 -O >> $psfile
H 12 1 $TITULO_leyenda
D 0 1p
S 0.1i c 0.1i red 0.25p 0.2i $Texto_leyenda_01
V 0 1p
S 0.1i c 0.1i blue 0.25p 0.2i $Texto_leyenda_03
>
END
endif

if ($leyenda == 'si' && $mostrar_sup == 'si' && $mostrar_int == 'no' && $mostrar_prof == 'no') then
pslegend <<END -Dx$SIZE_LEYENDA -R$REGION2 -JX$SIZE2 -F -G255/255/255 -O >> $psfile
H 12 1 $TITULO_leyenda
D 0 1p
S 0.1i c 0.1i red 0.25p 0.2i $Texto_leyenda_01
>
END
endif

if ($leyenda == 'si' && $mostrar_sup == 'no' && $mostrar_int == 'si' && $mostrar_prof == 'si') then
pslegend <<END -Dx$SIZE_LEYENDA -R$REGION2 -JX$SIZE2 -F -G255/255/255 -O >> $psfile
H 12 1 $TITULO_leyenda
D 0 1p
S 0.1i c 0.1i yellow 0.25p 0.2i $Texto_leyenda_02
V 0 1p
S 0.1i c 0.1i blue 0.25p 0.2i $Texto_leyenda_03
>
END
endif

if ($leyenda == 'si' && $mostrar_sup == 'no' && $mostrar_int == 'si' && $mostrar_prof == 'no') then
pslegend <<END -Dx$SIZE_LEYENDA -R$REGION2 -JX$SIZE2 -F -G255/255/255 -O >> $psfile
H 12 1 $TITULO_leyenda
D 0 1p
S 0.1i c 0.1i yellow 0.25p 0.2i $Texto_leyenda_02
>
END
endif

if ($leyenda == 'si' && $mostrar_sup == 'no' && $mostrar_int == 'no' && $mostrar_prof == 'si') then
pslegend <<END -Dx$SIZE_LEYENDA -R$REGION2 -JX$SIZE2 -F -G255/255/255 -O >> $psfile
H 12 1 $TITULO_leyenda
D 0 1p
S 0.1i c 0.1i blue 0.25p 0.2i $Texto_leyenda_03
>
END
endif

################################ Finalizando #################################
ps2eps $psfile -f
rm Aa-* $psfile
evince $epsfile &
