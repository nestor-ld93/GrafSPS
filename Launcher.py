#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#==================================================================================
#   +==========================================================================+  #
#   |                              GrafSPS v1.2.0                              |  #
#   +==========================================================================+  #
#   | -Graficador de Sismicidad y Perfiles Sísmicos                            |  #
#   | -Interfaz gráfica: PyQt5                                                 |  #
#   | -Ultima actualizacion: 30/12/2022                                        |  #
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
#   en el Perú utilizando el catálogo sísmico del NEIC-USGS sin ','s (archivo CSV
#   sin comas).
# - Se recomienda modificar manualmente el título de la leyenda.

#==================================================================================
# - GMT4 o GMT6
# - sh & csh
# - gawk
# - ps2eps
# - evince
# - python3
# - python3-pyqt5
#==================================================================================

import sys
import os
import signal
import subprocess
from PyQt5 import uic, QtWidgets

ruta_actual = os.getcwd()

#=========================================== Catálogo sísmico ===============================================
#CATALOGO_i = "Ingrese_la_ruta"
CATALOGO_i = ruta_actual+"/"+"Catalogo_NEIC-Peru-1980-2019.csv"

#======================================= Topografía y batimetría ============================================
#grdfile_i = "Ingrese_la_ruta"
grdfile_i = "/media/nestor/Datos/Topografia_Batimetria/GEBCO_ONE/GRIDONE_2D.nc"
#grdfile_i = "/media/nestor/Datos/Topografia_Batimetria/GEBCO_ONE/GEBCO_Peru_2.nc"
#grdfile_i = "/media/nestor/Datos/Topografia_Batimetria/ETOPO1_Bedrock/ETOPO1_Bed_g_gmt4.grd"
#grdfile_i = "/media/nestor/Datos/Topografia_Batimetria/ETOPO1_Bedrock/etopo1_Peru.grd"

#grdfile_2_i = "Ingrese_la_ruta"
#grdfile_2_i = "/media/nestor/Datos/Topografia_Batimetria/GEBCO_ONE/GRIDONE_2D.nc"
#grdfile_2_i = "/media/nestor/Datos/Topografia_Batimetria/GEBCO_ONE/GEBCO_Peru_2.nc"
grdfile_2_i = "/media/nestor/Datos/Topografia_Batimetria/ETOPO1_Bedrock/ETOPO1_Bed_g_gmt4.grd"
#grdfile_2_i = "/media/nestor/Datos/Topografia_Batimetria/ETOPO1_Bedrock/etopo1_Peru.grd"

#================================ Gradiente de topografía y batimetría ======================================
#grdgrad_i = "Ingrese_la_ruta"
grdgrad_i = "/media/nestor/Datos/Topografia_Batimetria/GEBCO_ONE/GRIDONE_2D_GRAD.nc"
#grdgrad_i = "/media/nestor/Datos/Topografia_Batimetria/GEBCO_ONE/GEBCO_Peru_2_GRAD.nc"
#grdgrad_i = "/media/nestor/Datos/Topografia_Batimetria/ETOPO1_Bedrock/ETOPO1_Bed_g_gmt4_GRAD.grd"
#grdgrad_i = "/media/nestor/Datos/Topografia_Batimetria/ETOPO1_Bedrock/etopo1_Peru_GRAD.grd"
#============================================================================================================

#=============================== Carpeta contenedora de datos de contornos ==================================
folder_i = ruta_actual+"/"+"Datos_contornos"
#folder_i  = "/media/nestor/Datos/Datos_contornos"

#==================================== Paleta de colores personalizada =======================================
#cptfile_i = "Ingrese_la_ruta"
#cptfile_i = "/media/nestor/Datos/Topografia_Batimetria/CPT_files/Caribbean.cpt"
#cptfile_i = "/media/nestor/Datos/Topografia_Batimetria/CPT_files/ibcao.cpt"
#cptfile_i = "/media/nestor/Datos/Topografia_Batimetria/CPT_files/mby.cpt"
#cptfile_i = "/media/nestor/Datos/Topografia_Batimetria/CPT_files/Peru_v1.cpt"
cptfile_i = "/media/nestor/Datos/Topografia_Batimetria/CPT_files/Peru_v2.cpt"
#============================================================================================================

def texto_caracteres_salida(i,texto_entrada):
    #TITULO = str(self.Titulo_leyenda.toPlainText())#.encode("utf-8").decode('cp1252')
    texto_salida = "'"
    texto_salida+= str(texto_entrada)
    texto_salida+= "'"
    if (i==1):
        texto_salida = texto_salida.replace(" ","%")
    else:
        if (i==2):
            texto_salida = texto_salida.replace(" ","{\\040}")
    texto_salida = texto_salida.replace("Á","{\\301}")
    texto_salida = texto_salida.replace("É","{\\311}")
    texto_salida = texto_salida.replace("Í","{\\315}")
    texto_salida = texto_salida.replace("Ó","{\\323}")
    texto_salida = texto_salida.replace("Ú","{\\332}")
    texto_salida = texto_salida.replace("Ñ","{\\321}")
    texto_salida = texto_salida.replace("á","{\\341}")
    texto_salida = texto_salida.replace("é","{\\351}")
    texto_salida = texto_salida.replace("í","{\\355}")
    texto_salida = texto_salida.replace("ó","{\\363}")
    texto_salida = texto_salida.replace("ú","{\\372}")
    texto_salida = texto_salida.replace("ñ","{\\361}")
    return texto_salida

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
        self.Run_Sismicidad_3.clicked.connect(self.Run_GrafSPS_01)
        self.Run_Perfil_Sismico.clicked.connect(self.Run_GrafSPS_04)
        
        self.Boton_examinar_1.clicked.connect(self.abrir_catalogo)
        self.Boton_examinar_2.clicked.connect(self.abrir_grdfile)
        self.Boton_examinar_3.clicked.connect(self.abrir_grdgrad)
        self.Boton_examinar_4.clicked.connect(self.abrir_grdfile_2)
        self.Boton_examinar_5.clicked.connect(self.select_directorio)
        self.Boton_examinar_6.clicked.connect(self.abrir_cptfile)
        
        self.Boton_reiniciar_coord.clicked.connect(self.reiniciar_coordenadas)
        self.Boton_reiniciar_coord_2.clicked.connect(self.reiniciar_parametros)
        self.Boton_reiniciar_coord_3.clicked.connect(self.reiniciar_coordenadas_2)
        
        self.check_folder_contorno.clicked.connect(self.check_folder)
        self.check_lim_dptos_ext.clicked.connect(self.graf_lim_dptos_01)
        self.check_lim_dptos_gmt.clicked.connect(self.graf_lim_dptos_02)
        self.check_minimapa.clicked.connect(self.mostrar_coord_minimapa)
        
        self.check_nombres_oceano.clicked.connect(self.mostrar_nombre_oceano_activacion)
        self.check_nombres_fosa.clicked.connect(self.mostrar_nombre_fosa_activacion)
        self.check_dorsal_nazca_2.clicked.connect(self.mostrar_nombre_dorsal_activacion)
        self.check_mendana_2.clicked.connect(self.mostrar_nombre_mendana_activacion)
        self.check_escala_mapa.clicked.connect(self.mostrar_escala_mapa_activacion)
        
        self.combo_topo_bati.currentIndexChanged.connect(self.tipo_topografia_activaciones)
        self.combo_leyenda.currentIndexChanged.connect(self.Texto_leyenda_activacion)
        self.check_superficiales.clicked.connect(self.Leyenda_NA_activacion)
        self.check_intermedios.clicked.connect(self.Leyenda_NA_activacion)
        self.check_profundos.clicked.connect(self.Leyenda_NA_activacion)
        self.check_superficiales_2.clicked.connect(self.Leyenda_NA_activacion_2)
        self.check_intermedios_2.clicked.connect(self.Leyenda_NA_activacion_2)
        self.check_profundos_2.clicked.connect(self.Leyenda_NA_activacion_2)
        self.check_CPT_file.clicked.connect(self.CPT_personalizado_activaciones)
        
        self.ruta_catalogo.setText(CATALOGO_i)
        self.ruta_grdfile.setText(grdfile_i)
        self.ruta_grdgrad.setText(grdgrad_i)
        self.ruta_grdfile_2.setText(grdfile_2_i)
        self.ruta_folder.setText(folder_i)
        self.ruta_cpt_file.setText(cptfile_i)
        
        # Condición para activar botones.
        if (self.ruta_catalogo.toPlainText()!="Ingrese_la_ruta"
            and self.ruta_grdfile.toPlainText()!="Ingrese_la_ruta"
            and self.ruta_grdgrad.toPlainText()!="Ingrese_la_ruta"
            and self.ruta_cpt_file.toPlainText()!="Ingrese_la_ruta"):
            self.Run_Sismicidad.setEnabled(True)        # Activar únicamente si se fijan archivos de las linea 56-92.
            self.Run_Sismicidad_2.setEnabled(True)      # Activar únicamente si se fijan archivos de las linea 56-92.
            self.Run_Sismicidad_3.setEnabled(True)      # Activar únicamente si se fijan archivos de las linea 56-92.
            self.Run_Perfil_Sismico.setEnabled(True)    # Activar únicamente si se fijan archivos de las linea 56-92.

#============================================================================================================
    def Borrar_resultados(self):
        comando_01 = "rm .gmt* gmt.conf gmt.history *.txt *.eps *.ps *.cpt"
        process = subprocess.Popen(comando_01, shell=True)
#============================================================================================================

#============================================================================================================
#================================================ Sismicidad ================================================
#============================================================================================================

    def mostrar_nombre_oceano_activacion(self):
        if (self.check_nombres_oceano.isChecked()==False):
            self.Titulo_oceano.setEnabled(False)
            self.val_LAT1_5.setEnabled(False)
            self.val_LON1_5.setEnabled(False)
            self.val_angulo_oce.setEnabled(False)
        else:
            self.Titulo_oceano.setEnabled(True)
            self.val_LAT1_5.setEnabled(True)
            self.val_LON1_5.setEnabled(True)
            self.val_angulo_oce.setEnabled(True)
            
    def mostrar_nombre_fosa_activacion(self):
        if (self.check_nombres_fosa.isChecked()==False):
            self.Titulo_fosa.setEnabled(False)
            self.val_LAT1_4.setEnabled(False)
            self.val_LON1_4.setEnabled(False)
            self.val_angulo_fosa.setEnabled(False)
        else:
            self.Titulo_fosa.setEnabled(True)
            self.val_LAT1_4.setEnabled(True)
            self.val_LON1_4.setEnabled(True)
            self.val_angulo_fosa.setEnabled(True)
            
    def mostrar_nombre_dorsal_activacion(self):
        if (self.check_dorsal_nazca_2.isChecked()==False):
            self.Titulo_dorsal.setEnabled(False)
            self.val_LAT1_8.setEnabled(False)
            self.val_LON1_8.setEnabled(False)
            self.val_angulo_dorsal.setEnabled(False)
        else:
            self.Titulo_dorsal.setEnabled(True)
            self.val_LAT1_8.setEnabled(True)
            self.val_LON1_8.setEnabled(True)
            self.val_angulo_dorsal.setEnabled(True)
            
    def mostrar_nombre_mendana_activacion(self):
        if (self.check_mendana_2.isChecked()==False):
            self.Titulo_mendana.setEnabled(False)
            self.val_LAT1_7.setEnabled(False)
            self.val_LON1_7.setEnabled(False)
            self.val_angulo_mend.setEnabled(False)
        else:
            self.Titulo_mendana.setEnabled(True)
            self.val_LAT1_7.setEnabled(True)
            self.val_LON1_7.setEnabled(True)
            self.val_angulo_mend.setEnabled(True)
            
    def mostrar_escala_mapa_activacion(self):
        if (self.check_escala_mapa.isChecked()==False):
            self.val_LAT1_3.setEnabled(False)
            self.val_LON1_3.setEnabled(False)
            self.Box_escala_mapa.setEnabled(False)
        else:
            self.val_LAT1_3.setEnabled(True)
            self.val_LON1_3.setEnabled(True)
            self.Box_escala_mapa.setEnabled(True)
##########
    def CPT_personalizado_activaciones(self):
        if (self.check_CPT_file.isChecked()==False):
            self.ruta_cpt_file.setEnabled(False)
            self.Boton_examinar_6.setEnabled(False)
        else:
            if (self.check_CPT_file.isChecked()==True):
                self.ruta_cpt_file.setEnabled(True)
                self.Boton_examinar_6.setEnabled(True)

    def abrir_cptfile(self):
        #ruta_actual = os.getcwd()
        
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(self,directory=ruta_actual,filter="Archivos cpt (*.cpt)")
        
        if (filePath != "" and filePath.find(".cpt")>0): # Condición para que el archivo sea .cpt.
            self.ruta_cpt_file.setText(filePath)

    def reiniciar_coordenadas(self):
        self.val_LAT1_1.setValue(-21.0)
        self.val_LAT2_1.setValue(01.0)
        self.val_LON1_1.setValue(-67.0)
        self.val_LON2_1.setValue(-84.0)
        
        self.val_LAT1_2.setValue(-59.0)
        self.val_LAT2_2.setValue(15.0)
        self.val_LON1_2.setValue(-30.0)
        self.val_LON2_2.setValue(-90.0)
    
    def reiniciar_coordenadas_2(self):
        self.val_LAT1_5.setValue(-12.0)
        self.val_LON1_5.setValue(-82.5)
        self.val_angulo_oce.setValue(305.0)
        
        self.val_LAT1_4.setValue(-11.7)
        self.val_LON1_4.setValue(-80.0)
        self.val_angulo_fosa.setValue(306.0)
        
        self.val_LAT1_8.setValue(-20.0)
        self.val_LON1_8.setValue(-79.0)
        self.val_angulo_dorsal.setValue(47.0)
        
        self.val_LAT1_7.setValue(-13.0)
        self.val_LON1_7.setValue(-84.0)
        self.val_angulo_mend.setValue(30.0)
        
        self.val_LAT1_3.setValue(-19.8)
        self.val_LON1_3.setValue(-74.0)
        self.Box_escala_mapa.setValue(200)

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
            self.check_CPT_file.setEnabled(False)
            self.check_CPT_file.setChecked(False)
            self.ruta_cpt_file.setEnabled(False)
            self.Boton_examinar_6.setEnabled(False)
            
            if (archivo_catalogo != "" and archivo_catalogo.find(".csv")>0):
                self.Run_Sismicidad.setEnabled(True)
                self.Run_Sismicidad_2.setEnabled(True)
                self.Run_Sismicidad_3.setEnabled(True)
            else:
                self.Run_Sismicidad.setEnabled(False)
                self.Run_Sismicidad_2.setEnabled(False)
                self.Run_Sismicidad_3.setEnabled(False)
        else:
            if (topo_bati_aux == 'Simple'):
                self.ruta_grdfile.setEnabled(True)
                self.ruta_grdgrad.setEnabled(False)
                self.Boton_examinar_2.setEnabled(True)
                self.Boton_examinar_3.setEnabled(False)
                self.check_escala_color.setEnabled(True)
                self.check_CPT_file.setEnabled(True)
                
                if (archivo_grd != "" and archivo_grd.find(".grd")>0 or archivo_grd.find(".nc")>0):
                    if (archivo_catalogo != "" and archivo_catalogo.find(".csv")>0):
                        self.Run_Sismicidad.setEnabled(True)
                        self.Run_Sismicidad_2.setEnabled(True)
                        self.Run_Sismicidad_3.setEnabled(True)
                else:
                    self.Run_Sismicidad.setEnabled(False)
                    self.Run_Sismicidad_2.setEnabled(False)
                    self.Run_Sismicidad_3.setEnabled(False)
            else:
                if (topo_bati_aux == 'Gradiente'):
                    self.ruta_grdfile.setEnabled(True)
                    self.ruta_grdgrad.setEnabled(True)
                    self.Boton_examinar_2.setEnabled(True)
                    self.Boton_examinar_3.setEnabled(True)
                    self.check_escala_color.setEnabled(True)
                    self.check_CPT_file.setEnabled(True)
                    
                    if (archivo_grad != "" and archivo_grad.find(".grd")>0 or archivo_grad.find(".nc")>0):
                        if (archivo_grd != "" and archivo_grd.find(".grd")>0 or archivo_grd.find(".nc")>0):
                            if (archivo_catalogo != "" and archivo_catalogo.find(".csv")>0):
                                self.Run_Sismicidad.setEnabled(True)
                                self.Run_Sismicidad_2.setEnabled(True)
                                self.Run_Sismicidad_3.setEnabled(True)
                    else:
                        self.Run_Sismicidad.setEnabled(False)
                        self.Run_Sismicidad_2.setEnabled(False)
                        self.Run_Sismicidad_3.setEnabled(False)
    
    def Texto_leyenda_activacion(self):
        if (self.combo_leyenda.currentText() == "N/A"):
            self.Texto_leyenda_01.setEnabled(False)
            self.Texto_leyenda_02.setEnabled(False)
            self.Texto_leyenda_03.setEnabled(False)
            self.Texto2_leyenda_01.setEnabled(False)
            self.Texto2_leyenda_02.setEnabled(False)
        else:
            if (self.combo_leyenda.currentText() == "Leyenda 1"):
                self.Texto_leyenda_01.setEnabled(True)
                self.Texto_leyenda_02.setEnabled(True)
                self.Texto_leyenda_03.setEnabled(True)
                self.Texto2_leyenda_01.setEnabled(False)
                self.Texto2_leyenda_02.setEnabled(False)
            else:
                if (self.combo_leyenda.currentText() == "Leyenda 2"):
                    self.Texto_leyenda_01.setEnabled(False)
                    self.Texto_leyenda_02.setEnabled(False)
                    self.Texto_leyenda_03.setEnabled(False)
                    self.Texto2_leyenda_01.setEnabled(True)
                    self.Texto2_leyenda_02.setEnabled(True)
    
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
                    self.Run_Sismicidad_3.setEnabled(True)
                else:
                    self.Run_Sismicidad.setEnabled(False)
                    self.Run_Sismicidad_2.setEnabled(False)
                    self.Run_Sismicidad_3.setEnabled(False)
            else:
                if (topo_bati_aux == 'Simple'):
                    if (archivo_grd != "" and archivo_grd.find(".grd")>0 or archivo_grd.find(".nc")>0):
                        if (archivo_catalogo != "" and archivo_catalogo.find(".csv")>0):
                            self.Run_Sismicidad.setEnabled(True)
                            self.Run_Sismicidad_2.setEnabled(True)
                            self.Run_Sismicidad_3.setEnabled(True)
                    else:
                        self.Run_Sismicidad.setEnabled(False)
                        self.Run_Sismicidad_2.setEnabled(False)
                        self.Run_Sismicidad_3.setEnabled(False)
                else:
                    if (topo_bati_aux == 'Gradiente'):
                        if (archivo_grad != "" and archivo_grad.find(".grd")>0 or archivo_grad.find(".nc")>0):
                            if (archivo_grd != "" and archivo_grd.find(".grd")>0 or archivo_grd.find(".nc")>0):
                                if (archivo_catalogo != "" and archivo_catalogo.find(".csv")>0):
                                    self.Run_Sismicidad.setEnabled(True)
                                    self.Run_Sismicidad_2.setEnabled(True)
                                    self.Run_Sismicidad_3.setEnabled(True)
                        else:
                            self.Run_Sismicidad.setEnabled(False)
                            self.Run_Sismicidad_2.setEnabled(False)
                            self.Run_Sismicidad_3.setEnabled(False)
            
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
                    self.Run_Sismicidad_3.setEnabled(True)
                else:
                    self.Run_Sismicidad.setEnabled(False)
                    self.Run_Sismicidad_2.setEnabled(False)
                    self.Run_Sismicidad_3.setEnabled(False)
            else:
                if (topo_bati_aux == 'Simple'):
                    if (archivo_grd != "" and archivo_grd.find(".grd")>0 or archivo_grd.find(".nc")>0):
                        if (archivo_catalogo != "" and archivo_catalogo.find(".csv")>0):
                            self.Run_Sismicidad.setEnabled(True)
                            self.Run_Sismicidad_2.setEnabled(True)
                            self.Run_Sismicidad_3.setEnabled(True)
                    else:
                        self.Run_Sismicidad.setEnabled(False)
                        self.Run_Sismicidad_2.setEnabled(False)
                        self.Run_Sismicidad_3.setEnabled(False)
                else:
                    if (topo_bati_aux == 'Gradiente'):
                        if (archivo_grad != "" and archivo_grad.find(".grd")>0 or archivo_grad.find(".nc")>0):
                            if (archivo_grd != "" and archivo_grd.find(".grd")>0 or archivo_grd.find(".nc")>0):
                                if (archivo_catalogo != "" and archivo_catalogo.find(".csv")>0):
                                    self.Run_Sismicidad.setEnabled(True)
                                    self.Run_Sismicidad_2.setEnabled(True)
                                    self.Run_Sismicidad_3.setEnabled(True)
                        else:
                            self.Run_Sismicidad.setEnabled(False)
                            self.Run_Sismicidad_2.setEnabled(False)
                            self.Run_Sismicidad_3.setEnabled(False)
            
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
                    self.Run_Sismicidad_3.setEnabled(True)
                else:
                    self.Run_Sismicidad.setEnabled(False)
                    self.Run_Sismicidad_2.setEnabled(False)
                    self.Run_Sismicidad_3.setEnabled(False)
            else:
                if (topo_bati_aux == 'Simple'):
                    if (archivo_grd != "" and archivo_grd.find(".grd")>0 or archivo_grd.find(".nc")>0):
                        if (archivo_catalogo != "" and archivo_catalogo.find(".csv")>0):
                            self.Run_Sismicidad.setEnabled(True)
                            self.Run_Sismicidad_2.setEnabled(True)
                            self.Run_Sismicidad_3.setEnabled(True)
                    else:
                        self.Run_Sismicidad.setEnabled(False)
                        self.Run_Sismicidad_2.setEnabled(False)
                        self.Run_Sismicidad_3.setEnabled(False)
                else:
                    if (topo_bati_aux == 'Gradiente'):
                        if (archivo_grad != "" and archivo_grad.find(".grd")>0 or archivo_grad.find(".nc")>0):
                            if (archivo_grd != "" and archivo_grd.find(".grd")>0 or archivo_grd.find(".nc")>0):
                                if (archivo_catalogo != "" and archivo_catalogo.find(".csv")>0):
                                    self.Run_Sismicidad.setEnabled(True)
                                    self.Run_Sismicidad_2.setEnabled(True)
                                    self.Run_Sismicidad_3.setEnabled(True)
                        else:
                            self.Run_Sismicidad.setEnabled(False)
                            self.Run_Sismicidad_2.setEnabled(False)
                            self.Run_Sismicidad_3.setEnabled(False)
    
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
        
        TITULO = texto_caracteres_salida(1,self.Titulo_leyenda.toPlainText())
        
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
        
        ######################### NUEVO #################################
        if (self.check_nombres_oceano.isChecked()==True):
            nombre_oceano = "si"
        else:
            nombre_oceano = "no"
        LAT_oceano = str(self.val_LAT1_5.value())
        LON_oceano = str(self.val_LON1_5.value())
        VAL_angulo_oceano = str(self.val_angulo_oce.value())
        
        TITULO_oceano_sh = texto_caracteres_salida(1,self.Titulo_oceano.toPlainText())
        
        if (self.check_nombres_fosa.isChecked()==True):
            nombre_fosa = "si"
        else:
            nombre_fosa = "no"
        LAT_fosa = str(self.val_LAT1_4.value())
        LON_fosa = str(self.val_LON1_4.value())
        VAL_angulo_fosa = str(self.val_angulo_fosa.value())
        
        TITULO_fosa_sh = texto_caracteres_salida(1,self.Titulo_fosa.toPlainText())
        
        if (self.check_dorsal_nazca_2.isChecked()==True):
            nombre_dorsal = "si"
        else:
            nombre_dorsal = "no"
        LAT_dorsal = str(self.val_LAT1_8.value())
        LON_dorsal = str(self.val_LON1_8.value())
        VAL_angulo_dorsal = str(self.val_angulo_dorsal.value())

        TITULO_dorsal_sh = texto_caracteres_salida(1,self.Titulo_dorsal.toPlainText())
        
        if (self.check_mendana_2.isChecked()==True):
            nombre_mendana = "si"
        else:
            nombre_mendana = "no"
        LAT_mendana = str(self.val_LAT1_7.value())
        LON_mendana = str(self.val_LON1_7.value())
        VAL_angulo_mendana = str(self.val_angulo_mend.value())
        
        TITULO_mendana_sh = texto_caracteres_salida(1,self.Titulo_mendana.toPlainText())
        
        div_lat = str(self.Box_div_LAT.value())
        grid_lat = str(self.Box_div_LAT_grid.value())
        div_lon = str(self.Box_div_LON.value())
        grid_lon = str(self.Box_div_LON_grid.value())
        
        if (self.check_CPT_file.isChecked()==True):
            usar_cpt_file = "si"
        else:
            usar_cpt_file = "no"
        archivo_cpt = self.ruta_cpt_file.toPlainText()
        
        if (self.check_escala_mapa.isChecked()==True):
            usar_escala_mapa = "si"
        else:
            usar_escala_mapa = "no"
        LAT_escala = str(self.val_LAT1_3.value())
        LON_escala = str(self.val_LON1_3.value())
        VAL_escala = str(self.Box_escala_mapa.value())
        
        Texto_leyenda_01_sh = texto_caracteres_salida(1,self.Texto_leyenda_01.toPlainText())
        Texto_leyenda_02_sh = texto_caracteres_salida(1,self.Texto_leyenda_02.toPlainText())
        Texto_leyenda_03_sh = texto_caracteres_salida(1,self.Texto_leyenda_03.toPlainText())
        
        texto2_leyenda_01_sh = texto_caracteres_salida(1,self.Texto2_leyenda_01.toPlainText())
        texto2_leyenda_02_sh = texto_caracteres_salida(1,self.Texto2_leyenda_02.toPlainText())
        
        ####################### FIN DE NUEVO ############################
        comando_01 = "./1_sismicidad.csh"
        comando_01+= " "+mini_mapa+" "+fosa+" "+fractura_mendana+" "+dorsal_nazca+" "+lim_dptos_ext
        comando_01+= " "+lim_dptos_gmt+" "+nombres_dptos+" "+nombres_paises+" "+nombre_oceano
        comando_01+= " "+escala_color+" "+topo_bati+" "+leyenda+" "+LAT1_1+" "+LAT2_1
        comando_01+= " "+LON1_1+" "+LON2_1+" "+LAT1_2+" "+LAT2_2+" "+LON1_2+" "+LON2_2
        comando_01+= " "+CATALOGO+" "+grdfile+" "+grdgrad+" "+folder
        comando_01+= " "+mostrar_sup+" "+mostrar_int+" "+mostrar_prof
        comando_01+= " "+TITULO
        comando_01+= " "+div_lon+" "+grid_lon+" "+div_lat+" "+grid_lat+" "+usar_cpt_file+ " "+archivo_cpt
        comando_01+= " "+usar_escala_mapa+" "+LAT_escala+" "+LON_escala+" "+VAL_escala
        comando_01+= " "+LAT_oceano+" "+LON_oceano+" "+VAL_angulo_oceano+" "+TITULO_oceano_sh
        comando_01+= " "+nombre_fosa+" "+nombre_dorsal+" "+nombre_mendana
        comando_01+= " "+LAT_fosa+" "+LON_fosa+" "+VAL_angulo_fosa+" "+TITULO_fosa_sh
        comando_01+= " "+LAT_dorsal+" "+LON_dorsal+" "+VAL_angulo_dorsal+" "+TITULO_dorsal_sh
        comando_01+= " "+LAT_mendana+" "+LON_mendana+" "+VAL_angulo_mendana+" "+TITULO_mendana_sh
        comando_01+= " "+Texto_leyenda_01_sh+" "+Texto_leyenda_02_sh+" "+Texto_leyenda_03_sh
        comando_01+= " "+texto2_leyenda_01_sh+" "+texto2_leyenda_02_sh
        process = subprocess.Popen(comando_01, shell=True)

#============================================================================================================
#================================================ Coordenadas ===============================================
#============================================================================================================

    def reiniciar_parametros(self):
        self.val_LAT_i_01.setValue(-8.1)
        self.val_LON_i_01.setValue(-81.1)
        self.val_L_01.setValue(1000.0)
        self.val_W_01.setValue(450.0)
        self.val_angulo_01.setValue(32.0)
        
        self.val_LAT_i_02.setValue(-13.3)
        self.val_LON_i_02.setValue(-78.3)
        self.val_L_02.setValue(1000.0)
        self.val_W_02.setValue(400.0)
        self.val_angulo_02.setValue(35.0)
        
        self.val_LAT_i_03.setValue(-17.78)
        self.val_LON_i_03.setValue(-73.05)
        self.val_L_03.setValue(900.0)
        self.val_W_03.setValue(400.0)
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
        
        TITULO = texto_caracteres_salida(1,self.Titulo_leyenda.toPlainText())
        
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
        
        ######################### NUEVO #################################
        if (self.check_nombres_oceano.isChecked()==True):
            nombre_oceano = "si"
        else:
            nombre_oceano = "no"
        LAT_oceano = str(self.val_LAT1_5.value())
        LON_oceano = str(self.val_LON1_5.value())
        VAL_angulo_oceano = str(self.val_angulo_oce.value())
        
        TITULO_oceano_sh = texto_caracteres_salida(1,self.Titulo_oceano.toPlainText())
        
        if (self.check_nombres_fosa.isChecked()==True):
            nombre_fosa = "si"
        else:
            nombre_fosa = "no"
        LAT_fosa = str(self.val_LAT1_4.value())
        LON_fosa = str(self.val_LON1_4.value())
        VAL_angulo_fosa = str(self.val_angulo_fosa.value())
        
        TITULO_fosa_sh = texto_caracteres_salida(1,self.Titulo_fosa.toPlainText())
        
        if (self.check_dorsal_nazca_2.isChecked()==True):
            nombre_dorsal = "si"
        else:
            nombre_dorsal = "no"
        LAT_dorsal = str(self.val_LAT1_8.value())
        LON_dorsal = str(self.val_LON1_8.value())
        VAL_angulo_dorsal = str(self.val_angulo_dorsal.value())
        
        TITULO_dorsal_sh = texto_caracteres_salida(1,self.Titulo_dorsal.toPlainText())
        
        if (self.check_mendana_2.isChecked()==True):
            nombre_mendana = "si"
        else:
            nombre_mendana = "no"
        LAT_mendana = str(self.val_LAT1_7.value())
        LON_mendana = str(self.val_LON1_7.value())
        VAL_angulo_mendana = str(self.val_angulo_mend.value())
        
        TITULO_mendana_sh = texto_caracteres_salida(1,self.Titulo_mendana.toPlainText())
        
        div_lat = str(self.Box_div_LAT.value())
        grid_lat = str(self.Box_div_LAT_grid.value())
        div_lon = str(self.Box_div_LON.value())
        grid_lon = str(self.Box_div_LON_grid.value())
        
        if (self.check_CPT_file.isChecked()==True):
            usar_cpt_file = "si"
        else:
            usar_cpt_file = "no"
        archivo_cpt = self.ruta_cpt_file.toPlainText()
        
        if (self.check_escala_mapa.isChecked()==True):
            usar_escala_mapa = "si"
        else:
            usar_escala_mapa = "no"
        LAT_escala = str(self.val_LAT1_3.value())
        LON_escala = str(self.val_LON1_3.value())
        VAL_escala = str(self.Box_escala_mapa.value())
        
        Texto_leyenda_01_sh = texto_caracteres_salida(1,self.Texto_leyenda_01.toPlainText())
        Texto_leyenda_02_sh = texto_caracteres_salida(1,self.Texto_leyenda_02.toPlainText())
        Texto_leyenda_03_sh = texto_caracteres_salida(1,self.Texto_leyenda_03.toPlainText())
        
        texto2_leyenda_01_sh = texto_caracteres_salida(1,self.Texto2_leyenda_01.toPlainText())
        texto2_leyenda_02_sh = texto_caracteres_salida(1,self.Texto2_leyenda_02.toPlainText())
        
        ####################### FIN DE NUEVO ############################
        comando_01 = "./3_sismicidad_perfil.csh"
        comando_01+= " "+mini_mapa+" "+fosa+" "+fractura_mendana+" "+dorsal_nazca+" "+lim_dptos_ext
        comando_01+= " "+lim_dptos_gmt+" "+nombres_dptos+" "+nombres_paises+" "+nombre_oceano
        comando_01+= " "+escala_color+" "+topo_bati+" "+leyenda+" "+LAT1_1+" "+LAT2_1
        comando_01+= " "+LON1_1+" "+LON2_1+" "+LAT1_2+" "+LAT2_2+" "+LON1_2+" "+LON2_2
        comando_01+= " "+CATALOGO+" "+grdfile+" "+grdgrad+" "+folder
        comando_01+= " "+mostrar_sup+" "+mostrar_int+" "+mostrar_prof
        comando_01+= " "+TITULO
        comando_01+= " "+div_lon+" "+grid_lon+" "+div_lat+" "+grid_lat+" "+usar_cpt_file+ " "+archivo_cpt
        comando_01+= " "+usar_escala_mapa+" "+LAT_escala+" "+LON_escala+" "+VAL_escala
        comando_01+= " "+LAT_oceano+" "+LON_oceano+" "+VAL_angulo_oceano+" "+TITULO_oceano_sh
        comando_01+= " "+nombre_fosa+" "+nombre_dorsal+" "+nombre_mendana
        comando_01+= " "+LAT_fosa+" "+LON_fosa+" "+VAL_angulo_fosa+" "+TITULO_fosa_sh
        comando_01+= " "+LAT_dorsal+" "+LON_dorsal+" "+VAL_angulo_dorsal+" "+TITULO_dorsal_sh
        comando_01+= " "+LAT_mendana+" "+LON_mendana+" "+VAL_angulo_mendana+" "+TITULO_mendana_sh
        comando_01+= " "+Texto_leyenda_01_sh+" "+Texto_leyenda_02_sh+" "+Texto_leyenda_03_sh
        comando_01+= " "+texto2_leyenda_01_sh+" "+texto2_leyenda_02_sh
        comando_01+= " "+perfil_norte+" "+perfil_centro+" "+perfil_sur
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
        
        TITULO = texto_caracteres_salida(1,self.Titulo_perfil.toPlainText())
        
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
        
        Texto_leyenda_01_sh = texto_caracteres_salida(1,self.Texto_leyenda_01.toPlainText())
        Texto_leyenda_02_sh = texto_caracteres_salida(1,self.Texto_leyenda_02.toPlainText())
        Texto_leyenda_03_sh = texto_caracteres_salida(1,self.Texto_leyenda_03.toPlainText())
        
        Texto_eje_x_sh = texto_caracteres_salida(2,self.Etiqueta_perfil_x.toPlainText())
        Texto_eje_y1_sh = texto_caracteres_salida(2,self.Etiqueta_perfil_y1.toPlainText())
        Texto_eje_y2_sh = texto_caracteres_salida(2,self.Etiqueta_perfil_y2.toPlainText())
        TITULO_perfil_sh = texto_caracteres_salida(2,self.Titulo_perfil_02.toPlainText())
        
        div_x = str(self.Box_div_x.value())
        grid_x = str(self.Box_div_x_grilla.value())
        div_y1 = str(self.Box_div_y1.value())
        grid_y1 = str(self.Box_div_y1_grilla.value())
        div_y2 = str(self.Box_div_y2.value())
        grid_y2 = str(self.Box_div_y2_grilla.value())
        
        min_y1 = str(self.Box_min_y1.value())
        max_y1 = str(self.Box_max_y1.value())
        min_y2 = str(self.Box_min_y2.value())
        max_y2 = str(self.Box_max_y2.value())
        
        comando_01 = "./4_perfil_sismico.csh"
        comando_01+= " "+grdfile_2+" "+perfil_region+" "+leyenda+" "+Long1+" "+Long2+" "+Long3
        comando_01+= " "+mostrar_sup+" "+mostrar_int+" "+mostrar_prof
        comando_01+= " "+TITULO
        comando_01+= " "+Texto_leyenda_01_sh+" "+Texto_leyenda_02_sh+" "+Texto_leyenda_03_sh
        comando_01+= " "+Texto_eje_x_sh+" "+Texto_eje_y1_sh+" "+Texto_eje_y2_sh+" "+TITULO_perfil_sh
        comando_01+= " "+div_x+" "+grid_x+" "+div_y1+" "+grid_y1+" "+div_y2+" "+grid_y2
        comando_01+= " "+min_y1+" "+max_y1+" "+min_y2+" "+max_y2
        process = subprocess.Popen(comando_01, shell=True)

if __name__ == "__main__":
    app =  QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
