#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#==================================================================================
#   +==========================================================================+  #
#   |                              GrafSPS v1.0.0                              |  #
#   +==========================================================================+  #
#   | -Graficador de Sismicidad y Perfiles Sísmicos                            |  #
#   | -Interfaz gráfica: PyQt5                                                 |  #
#   | -Ultima actualizacion: 16/07/2020                                        |  #
#   +--------------------------------------------------------------------------+  #
#   | -Copyright (C) 2020  Nestor Luna Diaz                                    |  #
#   +--------------------------------------------------------------------------+  #
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

#==================================================================================
# NOTA:
# - Este Script y todos los Sub-Scripts están pensados para graficar la sismicidad
#   en el Perú utilizando el catálogo sísmico del NEIC-USGS son ',' (archivo CSV
#   sin comas).
# - Se recomienda modificar manualmente el título de la leyenda.

#==================================================================================
# REQUISITOS MINIMOS:
# - GMT4 (Linux)
# - Shell y C-Shell (Linux)
# - ps2eps (Linux)
# - Evince (Linux)
# - python3 (Linux)
# - python3-pyqt5 (Linux)
# - GNU Linux (Kernel 4.15) 64-bit [Se recomienda una distribución con KDE Plasma 5.12 o superior]
#==================================================================================

import sys
import os
import signal
import subprocess
from PyQt5 import uic, QtWidgets

ruta_actual = os.getcwd()

#=========================================== Catálogo sísmico ===============================================
CATALOGO_i = "Ingrese_la_ruta"
#CATALOGO_i = "/home/nestor/Qt_Proyectos/GrafSPS_PyQt5/Catalogo_NEIC-Peru-1980-2019.csv"

#======================================= Topografía y batimetría ============================================
grdfile_i = "Ingrese_la_ruta"
#grdfile_i = "/media/nestor/Datos/Topografia_Batimetria/gebco/GridOne.nc"
#grdfile_i = "/media/nestor/Datos/Topografia_Batimetria/gebco/Peru_2.nc"
#grdfile_i = "/media/nestor/Datos/Topografia_Batimetria/ETOPO1_Bed_g_gmt4.grd"
#grdfile_i = "/media/nestor/Datos/Topografia_Batimetria/etopo1_bed_Peru.grd"

grdfile_2_i = "Ingrese_la_ruta"
#grdfile_2_i = "/media/nestor/Datos/Topografia_Batimetria/gebco/GridOne.nc"
#grdfile_2_i = "/media/nestor/Datos/Topografia_Batimetria/gebco/Peru_2.nc"
#grdfile_2_i = "/media/nestor/Datos/Topografia_Batimetria/ETOPO1_Bed_g_gmt4.grd"
#grdfile_2_i = "/media/nestor/Datos/Topografia_Batimetria/etopo1_bed_Peru.grd"

#================================ Gradiente de topografía y batimetría ======================================
grdgrad_i = "Ingrese_la_ruta"
#grdgrad_i = "/media/nestor/Datos/Topografia_Batimetria/gebco/Grad_GridOne.grd"
#grdgrad_i = "/media/nestor/Datos/Topografia_Batimetria/gebco/Grad_Peru_2.grd"
#grdgrad_i = "/media/nestor/Datos/Topografia_Batimetria/Grad_etopo1_Peru.grd"
#============================================================================================================

#=============================== Carpeta contenedora de datos de contornos ==================================
folder_i = ruta_actual+"/"+"Datos_contornos"
#folder_i  = "/media/nestor/Datos/Datos_contornos"
#============================================================================================================

qtCreatorFile = "main.ui" # Nombre del archivo aquí.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        
        self.Boton_salir.clicked.connect(self.close)
        self.Boton_Borrar.clicked.connect(self.Borrar_resultados)
        
        self.Run_Sismicidad.clicked.connect(self.Run_GrafSPS_01)
        self.Run_Coordenadas.clicked.connect(self.Run_GrafSPS_02)
        self.Run_Sismicidad_2.clicked.connect(self.Run_GrafSPS_03)
        self.Run_Perfil_Sismico.clicked.connect(self.Run_GrafSPS_04)
        
        self.Boton_examinar_1.clicked.connect(self.abrir_catalogo)
        self.Boton_examinar_2.clicked.connect(self.abrir_grdfile)
        self.Boton_examinar_3.clicked.connect(self.abrir_grdgrad)
        self.Boton_examinar_4.clicked.connect(self.abrir_grdfile_2)
        self.Boton_examinar_5.clicked.connect(self.select_directorio)
        
        self.Boton_reiniciar_coord.clicked.connect(self.reiniciar_coordenadas)
        self.Boton_reiniciar_coord_2.clicked.connect(self.reiniciar_parametros)
        
        self.check_folder_contorno.clicked.connect(self.check_folder)
        self.check_lim_dptos_ext.clicked.connect(self.graf_lim_dptos_01)
        self.check_lim_dptos_gmt.clicked.connect(self.graf_lim_dptos_02)
        self.check_minimapa.clicked.connect(self.mostrar_coord_minimapa)
        
        self.combo_topo_bati.currentIndexChanged.connect(self.tipo_topografia_activaciones)
        self.check_superficiales.clicked.connect(self.Leyenda_NA_activacion)
        self.check_intermedios.clicked.connect(self.Leyenda_NA_activacion)
        self.check_profundos.clicked.connect(self.Leyenda_NA_activacion)
        self.check_superficiales_2.clicked.connect(self.Leyenda_NA_activacion_2)
        self.check_intermedios_2.clicked.connect(self.Leyenda_NA_activacion_2)
        self.check_profundos_2.clicked.connect(self.Leyenda_NA_activacion_2)
        
        self.ruta_catalogo.setText(CATALOGO_i)
        self.ruta_grdfile.setText(grdfile_i)
        self.ruta_grdgrad.setText(grdgrad_i)
        self.ruta_grdfile_2.setText(grdfile_2_i)
        self.ruta_folder.setText(folder_i)
        
        self.Run_Sismicidad.setEnabled(True)        # Activar únicamente si se fijan archivos de las linea 56-83.
        self.Run_Sismicidad_2.setEnabled(True)      # Activar únicamente si se fijan archivos de las linea 56-83.
        self.Run_Perfil_Sismico.setEnabled(True)    # Activar únicamente si se fijan archivos de las linea 56-83.

#============================================================================================================
    def Borrar_resultados(self):
        comando_01 = "rm .gmt* *.txt *.eps *.ps"
        process = subprocess.Popen(comando_01, shell=True)
#============================================================================================================

#============================================================================================================
#================================================ Sismicidad ================================================
#============================================================================================================

    def reiniciar_coordenadas(self):
        self.val_LAT1_1.setValue(-21.0)
        self.val_LAT2_1.setValue(01.0)
        self.val_LON1_1.setValue(-67.0)
        self.val_LON2_1.setValue(-84.0)
        
        self.val_LAT1_2.setValue(-59.0)
        self.val_LAT2_2.setValue(15.0)
        self.val_LON1_2.setValue(-30.0)
        self.val_LON2_2.setValue(-90.0)

    def tipo_topografia_activaciones(self):
        topo_bati_aux = self.combo_topo_bati.currentText()
        archivo_catalogo = self.ruta_catalogo.toPlainText()
        archivo_grd = self.ruta_grdfile.toPlainText()
        archivo_grad= self.ruta_grdgrad.toPlainText()
        
        if (topo_bati_aux == 'N/A'):
            self.ruta_grdfile.setEnabled(False)
            self.ruta_grdgrad.setEnabled(False)
            self.Boton_examinar_2.setEnabled(False)
            self.Boton_examinar_3.setEnabled(False)
            self.check_escala_color.setEnabled(False)
            self.check_escala_color.setChecked(False)
            
            if (archivo_catalogo != "" and archivo_catalogo.find(".csv")>0):
                self.Run_Sismicidad.setEnabled(True)
                self.Run_Sismicidad_2.setEnabled(True)
            else:
                self.Run_Sismicidad.setEnabled(False)
                self.Run_Sismicidad_2.setEnabled(False)
        else:
            if (topo_bati_aux == 'Simple'):
                self.ruta_grdfile.setEnabled(True)
                self.ruta_grdgrad.setEnabled(False)
                self.Boton_examinar_2.setEnabled(True)
                self.Boton_examinar_3.setEnabled(False)
                self.check_escala_color.setEnabled(True)
                
                if (archivo_grd != "" and archivo_grd.find(".grd")>0 or archivo_grd.find(".nc")>0):
                    if (archivo_catalogo != "" and archivo_catalogo.find(".csv")>0):
                        self.Run_Sismicidad.setEnabled(True)
                        self.Run_Sismicidad_2.setEnabled(True)
                else:
                    self.Run_Sismicidad.setEnabled(False)
                    self.Run_Sismicidad_2.setEnabled(False)
            else:
                if (topo_bati_aux == 'Gradiente'):
                    self.ruta_grdfile.setEnabled(True)
                    self.ruta_grdgrad.setEnabled(True)
                    self.Boton_examinar_2.setEnabled(True)
                    self.Boton_examinar_3.setEnabled(True)
                    self.check_escala_color.setEnabled(True)
                    
                    if (archivo_grad != "" and archivo_grad.find(".grd")>0 or archivo_grad.find(".nc")>0):
                        if (archivo_grd != "" and archivo_grd.find(".grd")>0 or archivo_grd.find(".nc")>0):
                            if (archivo_catalogo != "" and archivo_catalogo.find(".csv")>0):
                                self.Run_Sismicidad.setEnabled(True)
                                self.Run_Sismicidad_2.setEnabled(True)
                    else:
                        self.Run_Sismicidad.setEnabled(False)
                        self.Run_Sismicidad_2.setEnabled(False)

    def Leyenda_NA_activacion(self):
        if (self.check_superficiales.isChecked()==False and self.check_intermedios.isChecked()==False
            and self.check_profundos.isChecked()==False):
            self.combo_leyenda.setCurrentIndex(0)
    
    def Leyenda_NA_activacion_2(self):
        if (self.check_superficiales_2.isChecked()==False and self.check_intermedios_2.isChecked()==False
            and self.check_profundos_2.isChecked()==False):
            self.check_leyenda_02.setEnabled(False)
            self.check_leyenda_02.setChecked(False)
        else:
            self.check_leyenda_02.setEnabled(True)
            self.check_leyenda_02.setChecked(True)
    
    def abrir_catalogo(self):
        #ruta_actual = os.getcwd()
        
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(self,directory=ruta_actual,filter="Archivos csv (*.csv)")
        
        if (filePath != "" and filePath.find(".csv")>0): # Condición para que el archivo sea .csv.
            self.ruta_catalogo.setText(filePath)
            #self.Run_Sismicidad.setEnabled(True)
            
            archivo_catalogo = self.ruta_catalogo.toPlainText()
            archivo_grd = self.ruta_grdfile.toPlainText()
            archivo_grad= self.ruta_grdgrad.toPlainText()
            topo_bati_aux = self.combo_topo_bati.currentText()
            if (topo_bati_aux == 'N/A'):
                if (archivo_catalogo != "" and archivo_catalogo.find(".csv")>0):
                    self.Run_Sismicidad.setEnabled(True)
                    self.Run_Sismicidad_2.setEnabled(True)
                else:
                    self.Run_Sismicidad.setEnabled(False)
                    self.Run_Sismicidad_2.setEnabled(False)
            else:
                if (topo_bati_aux == 'Simple'):
                    if (archivo_grd != "" and archivo_grd.find(".grd")>0 or archivo_grd.find(".nc")>0):
                        if (archivo_catalogo != "" and archivo_catalogo.find(".csv")>0):
                            self.Run_Sismicidad.setEnabled(True)
                            self.Run_Sismicidad_2.setEnabled(True)
                    else:
                        self.Run_Sismicidad.setEnabled(False)
                        self.Run_Sismicidad_2.setEnabled(False)
                else:
                    if (topo_bati_aux == 'Gradiente'):
                        if (archivo_grad != "" and archivo_grad.find(".grd")>0 or archivo_grad.find(".nc")>0):
                            if (archivo_grd != "" and archivo_grd.find(".grd")>0 or archivo_grd.find(".nc")>0):
                                if (archivo_catalogo != "" and archivo_catalogo.find(".csv")>0):
                                    self.Run_Sismicidad.setEnabled(True)
                                    self.Run_Sismicidad_2.setEnabled(True)
                        else:
                            self.Run_Sismicidad.setEnabled(False)
                            self.Run_Sismicidad_2.setEnabled(False)
            
    def abrir_grdfile(self):
        #ruta_actual = os.getcwd()
        
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(self,directory=ruta_actual,filter="Archivos grd y nc (*.grd *.nc)")
        
        if (filePath != "" and filePath.find(".grd")>0 or filePath.find(".nc")>0): # Condición para que el archivo sea .grd y .nc.
            self.ruta_grdfile.setText(filePath)
            #self.Run_Sismicidad.setEnabled(True)
            
            archivo_catalogo = self.ruta_catalogo.toPlainText()
            archivo_grd = self.ruta_grdfile.toPlainText()
            archivo_grad= self.ruta_grdgrad.toPlainText()
            topo_bati_aux = self.combo_topo_bati.currentText()
            if (topo_bati_aux == 'N/A'):
                if (archivo_catalogo != "" and archivo_catalogo.find(".csv")>0):
                    self.Run_Sismicidad.setEnabled(True)
                    self.Run_Sismicidad_2.setEnabled(True)
                else:
                    self.Run_Sismicidad.setEnabled(False)
                    self.Run_Sismicidad_2.setEnabled(False)
            else:
                if (topo_bati_aux == 'Simple'):
                    if (archivo_grd != "" and archivo_grd.find(".grd")>0 or archivo_grd.find(".nc")>0):
                        if (archivo_catalogo != "" and archivo_catalogo.find(".csv")>0):
                            self.Run_Sismicidad.setEnabled(True)
                            self.Run_Sismicidad_2.setEnabled(True)
                    else:
                        self.Run_Sismicidad.setEnabled(False)
                        self.Run_Sismicidad_2.setEnabled(False)
                else:
                    if (topo_bati_aux == 'Gradiente'):
                        if (archivo_grad != "" and archivo_grad.find(".grd")>0 or archivo_grad.find(".nc")>0):
                            if (archivo_grd != "" and archivo_grd.find(".grd")>0 or archivo_grd.find(".nc")>0):
                                if (archivo_catalogo != "" and archivo_catalogo.find(".csv")>0):
                                    self.Run_Sismicidad.setEnabled(True)
                                    self.Run_Sismicidad_2.setEnabled(True)
                        else:
                            self.Run_Sismicidad.setEnabled(False)
                            self.Run_Sismicidad_2.setEnabled(False)
            
    def abrir_grdgrad(self):
        #ruta_actual = os.getcwd()
        
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(self,directory=ruta_actual,filter="Archivos grd y nc (*.grd *nc)")
        
        if (filePath != "" and filePath.find(".grd")>0 or filePath.find(".nc")>0): # Condición para que el archivo sea .grd y nc.
            self.ruta_grdgrad.setText(filePath)
            #self.Run_Sismicidad.setEnabled(True)
            
            archivo_catalogo = self.ruta_catalogo.toPlainText()
            archivo_grd = self.ruta_grdfile.toPlainText()
            archivo_grad= self.ruta_grdgrad.toPlainText()
            topo_bati_aux = self.combo_topo_bati.currentText()
            if (topo_bati_aux == 'N/A'):
                if (archivo_catalogo != "" and archivo_catalogo.find(".csv")>0):
                    self.Run_Sismicidad.setEnabled(True)
                    self.Run_Sismicidad_2.setEnabled(True)
                else:
                    self.Run_Sismicidad.setEnabled(False)
                    self.Run_Sismicidad_2.setEnabled(False)
            else:
                if (topo_bati_aux == 'Simple'):
                    if (archivo_grd != "" and archivo_grd.find(".grd")>0 or archivo_grd.find(".nc")>0):
                        if (archivo_catalogo != "" and archivo_catalogo.find(".csv")>0):
                            self.Run_Sismicidad.setEnabled(True)
                            self.Run_Sismicidad_2.setEnabled(True)
                    else:
                        self.Run_Sismicidad.setEnabled(False)
                        self.Run_Sismicidad_2.setEnabled(False)
                else:
                    if (topo_bati_aux == 'Gradiente'):
                        if (archivo_grad != "" and archivo_grad.find(".grd")>0 or archivo_grad.find(".nc")>0):
                            if (archivo_grd != "" and archivo_grd.find(".grd")>0 or archivo_grd.find(".nc")>0):
                                if (archivo_catalogo != "" and archivo_catalogo.find(".csv")>0):
                                    self.Run_Sismicidad.setEnabled(True)
                                    self.Run_Sismicidad_2.setEnabled(True)
                        else:
                            self.Run_Sismicidad.setEnabled(False)
                            self.Run_Sismicidad_2.setEnabled(False)
    
    def select_directorio(self):
        #ruta_actual = os.getcwd()
        
        my_dir = QtWidgets.QFileDialog.getExistingDirectory(self,directory=ruta_actual)
        if (my_dir != ""):                               # Condición para que la carpeta exista.
            self.ruta_folder.setText(my_dir)
            #self.Run_Sismicidad.setEnabled(True)
    
    def check_folder(self):
        if (self.check_folder_contorno.isChecked()==False):
            self.ruta_folder.setEnabled(False)
            self.Boton_examinar_5.setEnabled(False)
            
            self.check_fosa.setEnabled(False)
            self.check_mendana.setEnabled(False)
            self.check_dorsal_nazca.setEnabled(False)
            self.check_lim_dptos_ext.setEnabled(False)
            
            self.check_fosa.setChecked(False)
            self.check_mendana.setChecked(False)
            self.check_dorsal_nazca.setChecked(False)
            self.check_lim_dptos_ext.setChecked(False)
            
            self.check_lim_dptos_gmt.setEnabled(True)
            self.check_lim_dptos_gmt.setChecked(True)
        else:
            self.ruta_folder.setEnabled(True)
            self.Boton_examinar_5.setEnabled(True)
            
            self.check_fosa.setEnabled(True)
            self.check_mendana.setEnabled(True)
            self.check_dorsal_nazca.setEnabled(True)
            self.check_lim_dptos_ext.setEnabled(True)
            
            self.check_fosa.setChecked(True)
            self.check_mendana.setChecked(True)
            self.check_dorsal_nazca.setChecked(True)
            self.check_lim_dptos_ext.setChecked(True)
            
            self.check_lim_dptos_gmt.setEnabled(False)
            self.check_lim_dptos_gmt.setChecked(False)
    
    def graf_lim_dptos_01(self):
        if (self.check_lim_dptos_ext.isChecked()==False):
            self.check_lim_dptos_gmt.setEnabled(True)
        else:
            self.check_lim_dptos_gmt.setEnabled(False)
    
    def graf_lim_dptos_02(self):
        if (self.check_lim_dptos_gmt.isChecked()==False and self.check_folder_contorno.isChecked()==True):
            self.check_lim_dptos_ext.setEnabled(True)
        else:
            self.check_lim_dptos_ext.setEnabled(False)
            
    def mostrar_coord_minimapa(self):
        if (self.check_minimapa.isChecked()==False):
            self.val_LAT1_2.setEnabled(False)
            self.val_LAT2_2.setEnabled(False)
            self.val_LON1_2.setEnabled(False)
            self.val_LON2_2.setEnabled(False)
        else:
            self.val_LAT1_2.setEnabled(True)
            self.val_LAT2_2.setEnabled(True)
            self.val_LON1_2.setEnabled(True)
            self.val_LON2_2.setEnabled(True)
    
    def Run_GrafSPS_01(self):
        
        CATALOGO = self.ruta_catalogo.toPlainText()
        grdfile = self.ruta_grdfile.toPlainText()
        grdgrad = self.ruta_grdgrad.toPlainText()
        folder = self.ruta_folder.toPlainText()
        
        if (self.check_minimapa.isChecked()==True):
            mini_mapa = "si"
        else:
            mini_mapa = "no"
        
        if (self.check_fosa.isChecked()==True):
            fosa = "si"
        else:
            fosa = "no"
        
        if (self.check_mendana.isChecked()==True):
            fractura_mendana = "si"
        else:
            fractura_mendana = "no"
        
        if (self.check_dorsal_nazca.isChecked()==True):
            dorsal_nazca = "si"
        else:
            dorsal_nazca = "no"
        
        if (self.check_lim_dptos_ext.isChecked()==True):
            lim_dptos_ext = "si"
        else:
            lim_dptos_ext = "no"
        
        if (self.check_lim_dptos_gmt.isChecked()==True):
            lim_dptos_gmt = "si"
        else:
            lim_dptos_gmt = "no"
        
        if (self.check_nombres_dptos.isChecked()==True):
            nombres_dptos = "si"
        else:
            nombres_dptos = "no"
        
        if (self.check_nombres_paises.isChecked()==True):
            nombres_paises = "si"
        else:
            nombres_paises = "no"
        
        if (self.check_nombres_oceano.isChecked()==True):
            nombre_oceano = "si"
        else:
            nombre_oceano = "no"
        ##
        if (self.check_escala_color.isChecked()==True):
            escala_color = "1"
        else:
            escala_color = "0"
            
        topo_bati_aux = self.combo_topo_bati.currentText()
        if (topo_bati_aux == 'N/A'):
            topo_bati = "1"
        else:
            if (topo_bati_aux == 'Simple'):
                topo_bati = "2"
            else:
                if (topo_bati_aux == 'Gradiente'):
                    topo_bati = "3"
        
        leyenda_aux = self.combo_leyenda.currentText()
        if (leyenda_aux == 'Leyenda 1'):
            leyenda = "1"
        else:
            if (leyenda_aux == 'Leyenda 2'):
                leyenda = "2"
            else:
                if (leyenda_aux == 'N/A'):
                    leyenda = "3"
        
        #TITULO = str(self.Titulo_leyenda.toPlainText())#.encode("utf-8").decode('cp1252')
        TITULO = "'"
        TITULO+= str(self.Titulo_leyenda.toPlainText())
        TITULO+= "'"
        TITULO = TITULO.replace(" ","%")
        
        LAT1_1 = str(self.val_LAT1_1.value())
        LAT2_1 = str(self.val_LAT2_1.value())
        LON1_1 = str(self.val_LON1_1.value())
        LON2_1 = str(self.val_LON2_1.value())
        
        LAT1_2 = str(self.val_LAT1_2.value())
        LAT2_2 = str(self.val_LAT2_2.value())
        LON1_2 = str(self.val_LON1_2.value())
        LON2_2 = str(self.val_LON2_2.value())
        
        if (self.check_superficiales.isChecked()==True):
            mostrar_sup = "si"
        else:
            mostrar_sup = "no"
        
        if (self.check_intermedios.isChecked()==True):
            mostrar_int = "si"
        else:
            mostrar_int = "no"
        
        if (self.check_profundos.isChecked()==True):
            mostrar_prof = "si"
        else:
            mostrar_prof = "no"
        
        comando_01 = "./1_sismicidad.csh"
        comando_01+= " "+mini_mapa+" "+fosa+" "+fractura_mendana+" "+dorsal_nazca+" "+lim_dptos_ext
        comando_01+= " "+lim_dptos_gmt+" "+nombres_dptos+" "+nombres_paises+" "+nombre_oceano
        comando_01+= " "+escala_color+" "+topo_bati+" "+leyenda+" "+LAT1_1+" "+LAT2_1
        comando_01+= " "+LON1_1+" "+LON2_1+" "+LAT1_2+" "+LAT2_2+" "+LON1_2+" "+LON2_2
        comando_01+= " "+CATALOGO+" "+grdfile+" "+grdgrad+" "+folder
        comando_01+= " "+mostrar_sup+" "+mostrar_int+" "+mostrar_prof
        comando_01+= " "+TITULO
        process = subprocess.Popen(comando_01, shell=True)

#============================================================================================================
#================================================ Coordenadas ===============================================
#============================================================================================================

    def reiniciar_parametros(self):
        self.val_LAT_i_01.setValue(-8.1)
        self.val_LON_i_01.setValue(-81.1)
        self.val_L_01.setValue(1000.0)
        self.val_W_01.setValue(500.0)
        self.val_angulo_01.setValue(32.0)
        
        self.val_LAT_i_02.setValue(-13.3)
        self.val_LON_i_02.setValue(-78.3)
        self.val_L_02.setValue(1000.0)
        self.val_W_02.setValue(500.0)
        self.val_angulo_02.setValue(35.0)
        
        self.val_LAT_i_03.setValue(-17.78)
        self.val_LON_i_03.setValue(-73.05)
        self.val_L_03.setValue(900.0)
        self.val_W_03.setValue(450.0)
        self.val_angulo_03.setValue(49.0)
    
    def Run_GrafSPS_02(self):
        
        lat01 = str(self.val_LAT_i_01.value())
        lon01 = str(self.val_LON_i_01.value())
        L1 = str(self.val_L_01.value())
        W1 = str(self.val_W_01.value())
        ang1 = str(self.val_angulo_01.value())
        
        lat02 = str(self.val_LAT_i_02.value())
        lon02 = str(self.val_LON_i_02.value())
        L2 = str(self.val_L_02.value())
        W2 = str(self.val_W_02.value())
        ang2 = str(self.val_angulo_02.value())
        
        lat03 = str(self.val_LAT_i_03.value())
        lon03 = str(self.val_LON_i_03.value())
        L3 = str(self.val_L_03.value())
        W3 = str(self.val_W_03.value())
        ang3 = str(self.val_angulo_03.value())

        comando_01 = "./2_coordenadas_perfil.sh"
        comando_01+= " "+lat01+" "+lon01+" "+L1+" "+W1+" "+ang1
        comando_01+= " "+lat02+" "+lon02+" "+L2+" "+W2+" "+ang2
        comando_01+= " "+lat03+" "+lon03+" "+L3+" "+W3+" "+ang3
        process = subprocess.Popen(comando_01, shell=True)

#============================================================================================================
#=============================================== Sismicidad 2 ===============================================
#============================================================================================================

    def Run_GrafSPS_03(self):
        
        CATALOGO = self.ruta_catalogo.toPlainText()
        grdfile = self.ruta_grdfile.toPlainText()
        grdgrad = self.ruta_grdgrad.toPlainText()
        folder = self.ruta_folder.toPlainText()
        
        if (self.check_minimapa.isChecked()==True):
            mini_mapa = "si"
        else:
            mini_mapa = "no"
        
        if (self.check_fosa.isChecked()==True):
            fosa = "si"
        else:
            fosa = "no"
        
        if (self.check_mendana.isChecked()==True):
            fractura_mendana = "si"
        else:
            fractura_mendana = "no"
        
        if (self.check_dorsal_nazca.isChecked()==True):
            dorsal_nazca = "si"
        else:
            dorsal_nazca = "no"
        
        if (self.check_lim_dptos_ext.isChecked()==True):
            lim_dptos_ext = "si"
        else:
            lim_dptos_ext = "no"
        
        if (self.check_lim_dptos_gmt.isChecked()==True):
            lim_dptos_gmt = "si"
        else:
            lim_dptos_gmt = "no"
        
        if (self.check_nombres_dptos.isChecked()==True):
            nombres_dptos = "si"
        else:
            nombres_dptos = "no"
        
        if (self.check_nombres_paises.isChecked()==True):
            nombres_paises = "si"
        else:
            nombres_paises = "no"
        
        if (self.check_nombres_oceano.isChecked()==True):
            nombre_oceano = "si"
        else:
            nombre_oceano = "no"
        ##
        if (self.check_escala_color.isChecked()==True):
            escala_color = "1"
        else:
            escala_color = "0"
            
        topo_bati_aux = self.combo_topo_bati.currentText()
        if (topo_bati_aux == 'N/A'):
            topo_bati = "1"
        else:
            if (topo_bati_aux == 'Simple'):
                topo_bati = "2"
            else:
                if (topo_bati_aux == 'Gradiente'):
                    topo_bati = "3"
        
        leyenda_aux = self.combo_leyenda.currentText()
        if (leyenda_aux == 'Leyenda 1'):
            leyenda = "1"
        else:
            if (leyenda_aux == 'Leyenda 2'):
                leyenda = "2"
            else:
                if (leyenda_aux == 'N/A'):
                    leyenda = "3"
        
        #TITULO = str(self.Titulo_leyenda.toPlainText())#.encode("utf-8").decode('cp1252')
        TITULO = "'"
        TITULO+= str(self.Titulo_leyenda.toPlainText())
        TITULO+= "'"
        TITULO = TITULO.replace(" ","%")
        
        LAT1_1 = str(self.val_LAT1_1.value())
        LAT2_1 = str(self.val_LAT2_1.value())
        LON1_1 = str(self.val_LON1_1.value())
        LON2_1 = str(self.val_LON2_1.value())
        
        LAT1_2 = str(self.val_LAT1_2.value())
        LAT2_2 = str(self.val_LAT2_2.value())
        LON1_2 = str(self.val_LON1_2.value())
        LON2_2 = str(self.val_LON2_2.value())
        
        if (self.check_superficiales.isChecked()==True):
            mostrar_sup = "si"
        else:
            mostrar_sup = "no"
        
        if (self.check_intermedios.isChecked()==True):
            mostrar_int = "si"
        else:
            mostrar_int = "no"
        
        if (self.check_profundos.isChecked()==True):
            mostrar_prof = "si"
        else:
            mostrar_prof = "no"
        ###
        if (self.check_rectangulo_norte.isChecked()==True):
            perfil_norte = "si"
        else:
            perfil_norte = "no"
        
        if (self.check_rectangulo_centro.isChecked()==True):
            perfil_centro = "si"
        else:
            perfil_centro = "no"
        
        if (self.check_rectangulo_sur.isChecked()==True):
            perfil_sur = "si"
        else:
            perfil_sur = "no"
        
        comando_01 = "./3_sismicidad_perfil.csh"
        comando_01+= " "+mini_mapa+" "+fosa+" "+fractura_mendana+" "+dorsal_nazca+" "+lim_dptos_ext
        comando_01+= " "+lim_dptos_gmt+" "+nombres_dptos+" "+nombres_paises+" "+nombre_oceano
        comando_01+= " "+escala_color+" "+topo_bati+" "+leyenda+" "+LAT1_1+" "+LAT2_1
        comando_01+= " "+LON1_1+" "+LON2_1+" "+LAT1_2+" "+LAT2_2+" "+LON1_2+" "+LON2_2
        comando_01+= " "+CATALOGO+" "+grdfile+" "+grdgrad+" "+folder
        comando_01+= " "+mostrar_sup+" "+mostrar_int+" "+mostrar_prof
        comando_01+= " "+perfil_norte+" "+perfil_centro+" "+perfil_sur
        comando_01+= " "+TITULO
        process = subprocess.Popen(comando_01, shell=True)

#============================================================================================================
#============================================ Perfiles sísmicos =============================================
#============================================================================================================

    def abrir_grdfile_2(self):
        #ruta_actual = str(subprocess.Popen("pwd", shell=True))
        #ruta_actual = os.getcwd()
        
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(self,directory=ruta_actual,filter="Archivos grd y nc (*.grd *.nc)")
        
        if (filePath != "" and filePath.find(".grd")>0 or filePath.find(".nc")>0): # Condición para que el archivo sea .grd y .nc.
            self.ruta_grdfile_2.setText(filePath)
            self.Run_Perfil_Sismico.setEnabled(True)
    
    def Run_GrafSPS_04(self):
        
        grdfile_2 = self.ruta_grdfile_2.toPlainText()
            
        perfil_region_aux = self.combo_perfil_region.currentText()
        if (perfil_region_aux == 'Norte'):
            perfil_region = "norte"
        else:
            if (perfil_region_aux == 'Centro'):
                perfil_region = "centro"
            else:
                if (perfil_region_aux == 'Sur'):
                    perfil_region = "sur"
        
        #TITULO = str(self.Titulo_leyenda.toPlainText())#.encode("utf-8").decode('cp1252')
        TITULO = "'"
        TITULO+= str(self.Titulo_perfil.toPlainText())
        TITULO+= "'"
        TITULO = TITULO.replace(" ","%")
        
        if (self.check_leyenda_02.isChecked()==True):
            leyenda = "si"
        else:
            leyenda = "no"
        
        Long1 = str(self.val_L_01.value())
        Long2 = str(self.val_L_02.value())
        Long3 = str(self.val_L_03.value())
        
        if (self.check_superficiales_2.isChecked()==True):
            mostrar_sup = "si"
        else:
            mostrar_sup = "no"
        
        if (self.check_intermedios_2.isChecked()==True):
            mostrar_int = "si"
        else:
            mostrar_int = "no"
        
        if (self.check_profundos_2.isChecked()==True):
            mostrar_prof = "si"
        else:
            mostrar_prof = "no"
        
        comando_01 = "./4_perfil_sismico.csh"
        comando_01+= " "+grdfile_2+" "+perfil_region+" "+leyenda+" "+Long1+" "+Long2+" "+Long3
        comando_01+= " "+mostrar_sup+" "+mostrar_int+" "+mostrar_prof
        comando_01+= " "+TITULO
        process = subprocess.Popen(comando_01, shell=True)

if __name__ == "__main__":
    app =  QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
