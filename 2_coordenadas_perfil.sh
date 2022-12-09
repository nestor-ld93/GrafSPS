#!/bin/sh

#==================================================================================
echo ""
echo "+==========================================================================+"
echo "|                      COORDENADAS-PERFILES v1.0.0                         |"
echo "+==========================================================================+"
echo "| -Genera las coordenadas del perfil a partir de 1 punto (lat0,lon0)       |"
echo "| -Ultima actualizacion: 16/07/2020                                        |"
echo "| -Basado en el programa transcord.f de Cesar Jimenez - 16 Apr 2013        |"
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

archivo_salida=coordenadas_perfiles.txt
N=3 # 3 perfiles

rm $archivo_salida
i=1

while [ $i -le $N ]; do
################## Variables a modificar (Perfil Norte) #######################
if [ $i -eq 1 ]; then
    lat0=${1}             # Latitud inicial.
    lon0=${2}            # Longitud inicial.

    L=${3}              # Largo del perfil (km2).
    W=${4}               # Ancho del perfil (km2).
    ang=${5}              # Angulo de rotacion (grad).
fi

################## Variables a modificar (Perfil Centro) ######################
if [ $i -eq 2 ]; then
    lat0=${6}           # Latitud inicial.
    lon0=${7}           # Longitud inicial.

    L=${8}              # Largo del perfil (km2).
    W=${9}               # Ancho del perfil (km2).
    ang=${10}              # Angulo de rotacion (grad).
fi

################## Variables a modificar (Perfil Sur) ########################
if [ $i -eq 3 ]; then
    lat0=${11}          # Latitud inicial.
    lon0=${12}          # Longitud inicial.

#    L=886.37             # Largo del perfil (km2).
    L=${13}             # Largo del perfil (km2).
    W=${14}              # Ancho del perfil (km2).
    ang=${15}             # Angulo de rotacion (grad).
fi

################## Operaciones para rotar coordenadas ########################
    ang=$(echo "scale=6; $ang*3.141592/180.0" | bc -l)

    cte1=$(echo "scale=4; $L / 110.0" | bc -l)
    xf=$(echo "scale=4; $cte1 * c($ang)" | bc -l)
    yf=$(echo "scale=4; $cte1 * s($ang)" | bc -l)
    lonf=$(echo "scale=4; $lon0 + $xf" | bc -l)
    latf=$(echo "scale=4; $lat0 + $yf" | bc -l)

    cte2=$(echo "scale=4; 0.5 * $W / 110.0" | bc -l)
    x1=$(echo "scale=4; $lon0 + 0 * c($ang) - $cte2 * s($ang)" | bc -l)
    y1=$(echo "scale=4; $lat0 + 0 * s($ang) + $cte2 * c($ang)" | bc -l)
    x2=$(echo "scale=4; $lon0 + 0 * c($ang) + $cte2 * s($ang)" | bc -l)
    y2=$(echo "scale=4; $lat0 + 0 * s($ang) - $cte2 * c($ang)" | bc -l)
    x3=$(echo "scale=4; $lon0 + $cte1 * c($ang) + $cte2 * s($ang)" | bc -l)
    y3=$(echo "scale=4; $lat0 + $cte1 * s($ang) - $cte2 * c($ang)" | bc -l)
    x4=$(echo "scale=4; $lon0 + $cte1 * c($ang) - $cte2 * s($ang)" | bc -l)
    y4=$(echo "scale=4; $lat0 + $cte1 * s($ang) + $cte2 * c($ang)" | bc -l)
    
    W_2=$(echo "scale=1; $W * 0.5" | bc -l)   # Se calcula la mitad del ancho.

################## Mostrar y guardar variables en txt ########################
    echo ""
    echo "-->Extremos del perfil $i:"
    echo "P0: $lon0 $lat0"
    echo "Pf: $lonf $latf"
    echo "-->Extremos del rectangulo $i:"
    echo "P1: $x1 $y1"
    echo "P2: $x2 $y2"
    echo "P3: $x3 $y3"
    echo "P4: $x4 $y4"

cat >>$archivo_salida << END
$lon0 $lat0 $lonf $latf $x1 $y1 $x2 $y2 $x3 $y3 $x4 $y4 $W_2
END

i=$((i + 1))             # Contador para el bucle.

done
