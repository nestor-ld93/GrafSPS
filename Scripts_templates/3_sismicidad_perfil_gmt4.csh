#!/bin/csh -f

#==================================================================================
echo ""
echo "+==========================================================================+"
echo "|                      SISMICIDAD-PERFILES v1.1.0                          |"
echo "+==========================================================================+"
echo "| -Generar un mapa de sismicidad con los perfiles de corte en el Perú      |"
echo "| -Ultima actualizacion: 16/10/2020                                        |"
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
set file_coord = coordenadas_perfiles.txt

set psfile  = sismicidad_perfil.ps
set epsfile = sismicidad_perfil.eps

############################ Límites de los mapas  ###########################
set LAT1_1 = $13
set LAT2_1 = $14
set LON1_1 = $15
set LON2_1 = $16
set REGION1 = $LON2_1/$LON1_1/$LAT1_1/$LAT2_1
set AXIS1 = a$29f$30/a$31f$32WeSn
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
set nombre_fosa = $43       # Variables: 'si', 'no' (mostrar el nombre de la fosa).
set nombre_dorsal = $44     # Variables: 'si', 'no' (mostrar el nombre de la dorsal de nazca).
set nombre_mendana = $45    # Variables: 'si', 'no' (mostrar el nombre de la fractura de mendaña).

set mostrar_sup  = $25     # Variables: 'si', 'no' (Graficar sismos superficiales, no graficar).
set mostrar_int  = $26     # Variables: 'si', 'no' (Graficar sismos intermedios, no graficar).
set mostrar_prof = $27     # Variables: 'si', 'no' (Graficar sismos profundos, no graficar).

set usar_cpt_file = $33    # Valores: 'si', 'no' (utilizar un cpt personalizado).
set usar_escala = $35
set LAT_escala = $36
set LON_escala = $37
set VAL_escala = $38

set LAT_oceano = $39
set LON_oceano = $40
set VAL_angulo_oceano = $41
set TITULO_oceano_pre = $42
set TITULO_oceano = `echo $TITULO_oceano_pre | tr "%" " "`

set LAT_fosa = $46
set LON_fosa = $47
set VAL_angulo_fosa = $48
set TITULO_fosa_pre = $49
set TITULO_fosa = `echo $TITULO_fosa_pre | tr "%" " "`

set LAT_dorsal = $50
set LON_dorsal = $51
set VAL_angulo_dorsal = $52
set TITULO_dorsal_pre = $53
set TITULO_dorsal = `echo $TITULO_dorsal_pre | tr "%" " "`

set LAT_mendana = $54
set LON_mendana = $55
set VAL_angulo_mendana = $56
set TITULO_mendana_pre = $57
set TITULO_mendana = `echo $TITULO_mendana_pre | tr "%" " "`

set Texto_leyenda_01_pre = $58
set Texto_leyenda_01 = `echo $Texto_leyenda_01_pre | tr "%" " "`

set Texto_leyenda_02_pre = $59
set Texto_leyenda_02 = `echo $Texto_leyenda_02_pre | tr "%" " "`

set Texto_leyenda_03_pre = $60
set Texto_leyenda_03 = `echo $Texto_leyenda_03_pre | tr "%" " "`

set Texto2_leyenda_01_pre = $61
set Texto2_leyenda_01 = `echo $Texto2_leyenda_01_pre | tr "%" " "`

set Texto2_leyenda_02_pre = $62
set Texto2_leyenda_02 = `echo $Texto2_leyenda_02_pre | tr "%" " "`

set perfil_norte  = $63     # Variables: 'si', 'no' (Graficar el area del perfil, no graficar).
set perfil_centro = $64     # Variables: 'si', 'no' (Graficar el area y corte del perfil, no graficar).
set perfil_sur    = $65     # Variables: 'si', 'no' (Graficar el area y corte del perfil, no graficar).

gmtset ANOT_FONT_SIZE 12
gmtset LABEL_FONT_SIZE 14
gmtset HEADER_FONT_SIZE 14
gmtset PAPER_MEDIA A4

################ Generar/Utilizar archivo CPT  ###############################
if ($usar_cpt_file == 'si') then
    set cptfile = $34
    else
        set cptfile = depth.cpt
        makecpt -Cglobe > $cptfile
endif
##############################################################################

########### Separar sismos: superficiales, intermedios, profundos ############
#cat $CATALOGO | awk '{if ($4 <= 60.0) print $1,$2,$3,$4,$5}' > $txt_sup
#cat $CATALOGO | awk '{if ($4>60.0 && $4<=300.0) print $1,$2,$3,$4,$5}' > $txt_int
#cat $CATALOGO | awk '{if ($4 > 300.0) print $1,$2,$3,$4,$5}' > $txt_pro

################# Sin topografía y batimetría  ###############################
if ($usar_escala == 'si') then
    if ($topo_bati == 1) then
        psbasemap -R$REGION1 -J$SIZE1 -B$AXIS1 -X3.0c -Y5.0c -P -K -V > $psfile
        if ($lim_dptos_gmt == 'si') then
            pscoast -J$SIZE1 -R$REGION1 -B$AXIS1 -Lf$LON_escala/$LAT_escala/$LON_escala/15.3/$VAL_escala+lkm -S120/180/225 -G220/220/220 -Df -W1 -N1/3 -N2 -N3 -P -K -V -O >> $psfile
            else
                pscoast -J$SIZE1 -R$REGION1 -B$AXIS1 -Lf$LON_escala/$LAT_escala/$LON_escala/15.3/$VAL_escala+lkm -S120/180/225 -G220/220/220 -Df -W1 -N1/3 -P -K -V -O >> $psfile
        endif
    endif
    else
    if ($topo_bati == 1) then
        psbasemap -R$REGION1 -J$SIZE1 -B$AXIS1 -X3.0c -Y5.0c -P -K -V > $psfile
        if ($lim_dptos_gmt == 'si') then
            pscoast -J$SIZE1 -R$REGION1 -B$AXIS1 -S120/180/225 -G220/220/220 -Df -W1 -N1/3 -N2 -N3 -P -K -V -O >> $psfile
            else
                pscoast -J$SIZE1 -R$REGION1 -B$AXIS1 -S120/180/225 -G220/220/220 -Df -W1 -N1/3 -P -K -V -O >> $psfile
        endif
    endif
endif
##############################################################################

############### Topografía y batimetría simple ###############################
if ($usar_escala == 'si') then
    if ($topo_bati == 2) then
        grdimage $grdfile -R$REGION1 -J$SIZE1 -C$cptfile -X3.0c -Y5.0c -P -K -V > ! $psfile
        if ($lim_dptos_gmt == 'si') then
            pscoast -J$SIZE1 -R$REGION1 -B$AXIS1 -Lf$LON_escala/$LAT_escala/$LON_escala/15.3/$VAL_escala+lkm -Df -W1 -N1/3 -N2 -N3 -P -K -V -O >> $psfile
            else
                pscoast -J$SIZE1 -R$REGION1 -B$AXIS1 -Lf$LON_escala/$LAT_escala/$LON_escala/15.3/$VAL_escala+lkm -Df -W1 -N1/3 -P -K -V -O >> $psfile
        endif
        if ($escala_color == 1) then
            psscale -C$cptfile -D7.5/-1.0/12c/0.4ch -B4000/:m: -O -K -V  >> $psfile
        endif
    endif
    else
    if ($topo_bati == 2) then
        grdimage $grdfile -R$REGION1 -J$SIZE1 -C$cptfile -X3.0c -Y5.0c -P -K -V > ! $psfile
        if ($lim_dptos_gmt == 'si') then
            pscoast -J$SIZE1 -R$REGION1 -B$AXIS1 -Df -W1 -N1/3 -N2 -N3 -P -K -V -O >> $psfile
            else
                pscoast -J$SIZE1 -R$REGION1 -B$AXIS1 -Df -W1 -N1/3 -P -K -V -O >> $psfile
        endif
        if ($escala_color == 1) then
            psscale -C$cptfile -D7.5/-1.0/12c/0.4ch -B4000/:m: -O -K -V  >> $psfile
        endif
    endif
endif
##############################################################################

############ Topografía y batimetría con gradiente ###########################
if ($usar_escala == 'si') then
    if ($topo_bati == 3) then
        grdimage $grdfile -R$REGION1 -J$SIZE1 -C$cptfile -I$grdgrad -X3.0c -Y5.0c -P -K -V > ! $psfile
        if ($lim_dptos_gmt == 'si') then
            pscoast -J$SIZE1 -R$REGION1 -B$AXIS1 -Lf$LON_escala/$LAT_escala/$LON_escala/15.3/$VAL_escala+lkm -Df -W1 -N1/3 -N2 -N3 -P -K -V -O >> $psfile
            else
                pscoast -J$SIZE1 -R$REGION1 -B$AXIS1 -Lf$LON_escala/$LAT_escala/$LON_escala/15.3/$VAL_escala+lkm -Df -W1 -N1/3 -P -K -V -O >> $psfile
        endif
        if ($escala_color == 1) then
            psscale -C$cptfile -D7.5/-1.0/12c/0.4ch -B4000/:m: -O -K -V  >> $psfile
        endif
    endif
    else
    if ($topo_bati == 3) then
        grdimage $grdfile -R$REGION1 -J$SIZE1 -C$cptfile -I$grdgrad -X3.0c -Y5.0c -P -K -V > ! $psfile
        if ($lim_dptos_gmt == 'si') then
            pscoast -J$SIZE1 -R$REGION1 -B$AXIS1 -Df -W1 -N1/3 -N2 -N3 -P -K -V -O >> $psfile
            else
                pscoast -J$SIZE1 -R$REGION1 -B$AXIS1 -Df -W1 -N1/3 -P -K -V -O >> $psfile
        endif
        if ($escala_color == 1) then
            psscale -C$cptfile -D7.5/-1.0/12c/0.4ch -B4000/:m: -O -K -V  >> $psfile
        endif
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

######################### Coordenadas de perfiles ############################
#set N = `awk 'END {print NR}' $file_coord`    # Numero de filas del archivo.

#LINEA NEGRA y rectangulo del perfil Norte <---------------
if ($perfil_norte == 'si') then
    set i = 1
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

psxy -R -JM -W8 -P -O -V -K <<EOF>> $psfile
$lon0 $lat0
$lonf $latf
EOF

set lon_l1 = `echo "scale=2; $lon0-0.70" | bc`   # Calcula coordenadas para graficar letras.
set lat_l1 = `echo "scale=2; $lat0-0.00" | bc`   # Calcula coordenadas para graficar letras.
set lon_l2 = `echo "scale=2; $lonf+0.10" | bc`   # Calcula coordenadas para graficar letras.
set lat_l2 = `echo "scale=2; $latf+0.50" | bc`   # Calcula coordenadas para graficar letras.

pstext -R -JM -P -O -V -K <<EOF>> $psfile
$lon_l1 $lat_l1 14 360 1 LT A
$lon_l2 $lat_l2 14 360 1 LT A\47
EOF

psxy -R -JM -W2 -P -O -V -K <<EOF>> $psfile
$x1 $y1
$x2 $y2
$x3 $y3
$x4 $y4
$x1 $y1
EOF
endif

#LINEA NEGRA y rectangulo del perfil Centro <---------------
if ($perfil_centro == 'si') then
set i = 2
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
psxy -R -JM -W8 -P -O -V -K <<EOF>> $psfile
$lon0 $lat0
$lonf $latf
EOF

set lon_l1 = `echo "scale=2; $lon0-0.70" | bc`   # Calcula coordenadas para graficar letras.
set lat_l1 = `echo "scale=2; $lat0-0.00" | bc`   # Calcula coordenadas para graficar letras.
set lon_l2 = `echo "scale=2; $lonf+0.10" | bc`   # Calcula coordenadas para graficar letras.
set lat_l2 = `echo "scale=2; $latf+0.50" | bc`   # Calcula coordenadas para graficar letras.

pstext -R -JM -P -O -V -K <<EOF>> $psfile
$lon_l1 $lat_l1 14 360 1 LT B
$lon_l2 $lat_l2 14 360 1 LT B\47
EOF

psxy -R -JM -W2 -P -O -V -K <<EOF>> $psfile
$x1 $y1
$x2 $y2
$x3 $y3
$x4 $y4
$x1 $y1
EOF
endif

#LINEA NEGRA y rectangulo del perfil Sur <---------------
if ($perfil_sur == 'si') then
set i = 3
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
psxy -R -JM -W8 -P -O -V -K <<EOF>> $psfile
$lon0 $lat0
$lonf $latf
EOF

set lon_l1 = `echo "scale=2; $lon0-0.70" | bc`   # Calcula coordenadas para graficar letras.
set lat_l1 = `echo "scale=2; $lat0-0.15" | bc`   # Calcula coordenadas para graficar letras.
set lon_l2 = `echo "scale=2; $lonf+0.10" | bc`   # Calcula coordenadas para graficar letras.
set lat_l2 = `echo "scale=2; $latf+0.50" | bc`   # Calcula coordenadas para graficar letras.

pstext -R -JM -P -O -V -K <<EOF>> $psfile
$lon_l1 $lat_l1 14 360 1 LT C
$lon_l2 $lat_l2 14 360 1 LT C\47
EOF

psxy -R -JM -W2 -P -O -V -K <<EOF>> $psfile
$x1 $y1
$x2 $y2
$x3 $y3
$x4 $y4
$x1 $y1
EOF
endif

########### Nombres de Departamentos en Perú y zonas fronterizas #############
if ($nombres_dptos == 'si') then
pstext -R -JM -Wwhite -O -K <<EOF>> $psfile
-80.63 -05.20 12 0 1 LT Piura
-79.03 -08.11 12 0 1 LT Trujillo
-77.08 -11.90 12 0 1 LT Lima
#-76.18 -13.71 12 0 1 LT Pisco
-75.60 -14.3 12 0 1 LT Ica
-73.04 -15.60 12 0 1 LT Arequipa
#-71.40 -16.90 12 0 1 LT Moquegua
-70.60 -17.70 12 0 1 LT Tacna
#-70.20 -18.60 12 0 1 LT Arica
#-70.00 -20.00 12 0 1 LT Iquique
#-70.00 -22.50 12 0 1 LT Antofagasta
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
$LON_oceano $LAT_oceano 14 $VAL_angulo_oceano 1 LT $TITULO_oceano
EOF
#-82.5 -12.0 14 305 1 LT OC\311ANO PAC\315FICO
endif

if ($nombre_fosa == 'si') then
pstext -R -JM -P -O -V -K <<EOF>> $psfile
$LON_fosa $LAT_fosa 12 $VAL_angulo_fosa 1 LT $TITULO_fosa
EOF
#-80.0 -11.7 12 306 1 LT Fosa Peruana
endif

if ($nombre_dorsal == 'si') then
pstext -R -JM -P -O -V -K <<EOF>> $psfile
$LON_dorsal $LAT_dorsal 12 $VAL_angulo_dorsal 1 LT $TITULO_dorsal
EOF
#-79.0 -20.0 12 47 1 LT Dorsal de Nazca
endif

if ($nombre_mendana == 'si') then
pstext -R -JM -P -O -V -K <<EOF>> $psfile
$LON_mendana $LAT_mendana 12 $VAL_angulo_mendana 1 LT $TITULO_mendana
EOF
#-84.0 -13.0 12 30 1 LT Fractura de Menda\361a
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

pscoast -J$SIZE2 -R$REGION2 -Di -W1 -N1 -T-42.2/-48.8/1.4 -G180 -S120/180/225 -O -V -X11.95 -Y15.25 -K >> $psfile

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
S 0.1i c 0.1i red 0.25p 0.2i $Texto_leyenda_01
V 0 1p
S 0.1i c 0.1i yellow 0.25p 0.2i $Texto_leyenda_02
V 0 1p
S 0.1i c 0.1i blue 0.25p 0.2i $Texto_leyenda_03
>
END
endif

if ($leyenda == 1 && $mostrar_sup == 'si' && $mostrar_int == 'si' && $mostrar_prof == 'no') then
pslegend <<END -Dx$SIZE_LEYENDA -R$REGION1 -J$SIZE1 -F -G255/255/255 -O >> $psfile
H 12 1 $TITULO
D 0 1p
S 0.1i c 0.1i red 0.25p 0.2i $Texto_leyenda_01
V 0 1p
S 0.1i c 0.1i yellow 0.25p 0.2i $Texto_leyenda_02
>
END
endif

if ($leyenda == 1 && $mostrar_sup == 'si' && $mostrar_int == 'no' && $mostrar_prof == 'si') then
pslegend <<END -Dx$SIZE_LEYENDA -R$REGION1 -J$SIZE1 -F -G255/255/255 -O >> $psfile
H 12 1 $TITULO
D 0 1p
S 0.1i c 0.1i red 0.25p 0.2i $Texto_leyenda_01
V 0 1p
S 0.1i c 0.1i blue 0.25p 0.2i $Texto_leyenda_03
>
END
endif

if ($leyenda == 1 && $mostrar_sup == 'si' && $mostrar_int == 'no' && $mostrar_prof == 'no') then
pslegend <<END -Dx$SIZE_LEYENDA -R$REGION1 -J$SIZE1 -F -G255/255/255 -O >> $psfile
H 12 1 $TITULO
D 0 1p
S 0.1i c 0.1i red 0.25p 0.2i $Texto_leyenda_01
>
END
endif

if ($leyenda == 1 && $mostrar_sup == 'no' && $mostrar_int == 'si' && $mostrar_prof == 'si') then
pslegend <<END -Dx$SIZE_LEYENDA -R$REGION1 -J$SIZE1 -F -G255/255/255 -O >> $psfile
H 12 1 $TITULO
D 0 1p
S 0.1i c 0.1i yellow 0.25p 0.2i $Texto_leyenda_02
V 0 1p
S 0.1i c 0.1i blue 0.25p 0.2i $Texto_leyenda_03
>
END
endif

if ($leyenda == 1 && $mostrar_sup == 'no' && $mostrar_int == 'si' && $mostrar_prof == 'no') then
pslegend <<END -Dx$SIZE_LEYENDA -R$REGION1 -J$SIZE1 -F -G255/255/255 -O >> $psfile
H 12 1 $TITULO
D 0 1p
S 0.1i c 0.1i yellow 0.25p 0.2i $Texto_leyenda_02
>
END
endif

if ($leyenda == 1 && $mostrar_sup == 'no' && $mostrar_int == 'no' && $mostrar_prof == 'si') then
pslegend <<END -Dx$SIZE_LEYENDA -R$REGION1 -J$SIZE1 -F -G255/255/255 -O >> $psfile
H 12 1 $TITULO
D 0 1p
S 0.1i c 0.1i blue 0.25p 0.2i $Texto_leyenda_03
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
H 11 0 $Texto2_leyenda_01                  $Texto2_leyenda_02
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
H 11 0 $Texto2_leyenda_01                  $Texto2_leyenda_02
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
H 11 0 $Texto2_leyenda_01                  $Texto2_leyenda_02
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
H 11 0 $Texto2_leyenda_01                  $Texto2_leyenda_02
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
H 11 0 $Texto2_leyenda_01                  $Texto2_leyenda_02
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
H 11 0 $Texto2_leyenda_01                  $Texto2_leyenda_02
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
H 11 0 $Texto2_leyenda_01                  $Texto2_leyenda_02
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
rm $psfile
evince $epsfile &
