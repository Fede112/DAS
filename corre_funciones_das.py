######################################
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 09:32:54 2017

@author: Marco
"""

#################
# procesa_std_fft: esta función lee el dato crudo y procesa para obtener la STD y la FFT.

from funciones_das import procesa_std_fft
from funciones4 import header_read
from funciones4 import data_read
import numpy as np


parametros = {}
parametros['time_str'] = '17_30_11_10_59_49'
parametros['c'] = 299792458.
parametros['n'] = 1.46879964
parametros['c_f'] = parametros['c'] / parametros['n']
parametros['offset_m'] = 0
parametros['FrecLaser'] = 2000
parametros['zoom_i_m'] = 5300
parametros['zoom_f_m'] = 5600
parametros['c_axis_min'] = 0
parametros['c_axis_max'] = 0.08
parametros['punzados_m'] = np.array([])
parametros['colores_m'] = []
parametros['titulo_str'] = 'Villa Mercedes'
parametros['tiempo_ini'] = '2017-11-30 11:12:30'
parametros['tiempo_fin'] = '2017-11-30 11:13:30'
parametros['window_time_data'] = 20
parametros['window_bin_data'] = 1
parametros['window_bin'] = 5
parametros['window_bin_mean'] = 1
parametros['std_step_sec'] = 1
parametros['butter_filter'] = 'no'
parametros['butter_lp_frec'] = 1000
parametros['butter_hp_frec'] = 5
parametros['butter_order'] = 5
parametros['fft_step_sec'] = 10
parametros['c_axis_min_fft'] = 0
parametros['c_axis_max_fft'] = 10000
parametros['titulo_str_fft'] = 'FFT de retro a 4 m de la traza'
parametros['guarda_figuras'] = 'si'
parametros['carpeta_figuras'] = 'Figuras'
parametros['num_figura'] = 1

std, data_fft_tot, pos_bin_std, tiempo_filas_std, frq, pos_bin_fft, = procesa_std_fft(parametros)


##########################
# carga_std: carga los datos de la std en una matriz[filas=tiempo, col=bines].
from funciones_das import carga_std
from funciones4 import header_read
from funciones4 import data_read
import numpy as np
import os

parametros = {}
parametros['time_str'] = '17_22_11_12_04_36'
nombre_header = os.path.join(parametros['time_str'], 'STD', 'std.hdr')
nombre_archivo = os.path.join(parametros['time_str'], 'STD', '000000.std')
header = header_read(nombre_header, nombre_archivo)
parametros['c'] = 299792458.
parametros['n'] = 1.46879964
parametros['offset_m'] = 0
parametros['FrecLaser'] = 5000
parametros['c_f'] = parametros['c'] / parametros['n']
parametros['vector_offset'] = np.zeros(int(header['Cols']))
parametros['vector_norm'] = np.ones(int(header['Cols']))
parametros['c_axis_min'] = 0
parametros['c_axis_max'] = 0.2
parametros['zoom_i_m'] = 0
parametros['zoom_f_m'] = 13000
parametros['marcadores_m'] = np.array([1000, 2000, 3000])
parametros['marcadores_texto'] = []
parametros['marcadores_waterfall'] = 'no'
parametros['marcadores_color'] = ['r', 'r', 'r']
parametros['titulo_str'] = 'Oleoducto Restinga'
parametros['tiempo_ini'] = '2017-11-22 12:40:00'
parametros['tiempo_fin'] = '2017-11-22 12:50:00'
parametros['guarda_figuras'] = 'si'
parametros['carpeta_figuras'] = 'Figuras'
parametros['num_figura'] = 1

matriz, tiempo_filas_std, pos_bin, = carga_std(parametros)


###########################
from funciones_das import peli_std
from funciones4 import header_read
from funciones4 import data_read
import numpy as np
import os


parametros = {}
parametros['time_str'] = '17_22_11_12_04_36'
nombre_header = os.path.join(parametros['time_str'], 'STD', 'std.hdr')
nombre_archivo = os.path.join(parametros['time_str'], 'STD', '000000.std')
header = header_read(nombre_header, nombre_archivo)
parametros['output_movie'] = os.path.join(parametros['time_str'], 'STD', 'peli1232.mp4')
parametros['c'] = 299792458.
parametros['n'] = 1.46879964
parametros['offset_m'] = -187
parametros['FrecLaser'] = 10002.2
parametros['FilasPeli'] = 2000
parametros['StepPeli'] = 50
parametros['c_f'] = parametros['c'] / parametros['n']
parametros['vector_offset'] = np.zeros(int(header['Cols']))
parametros['vector_norm'] = np.ones(int(header['Cols']))
parametros['titulo_str'] = '%02d' % (1)
parametros['texto1'] = ''
parametros['texto2'] = ''
parametros['ini_file'] = 0
parametros['fin_file'] = []
parametros['c_axis_min'] = 0
parametros['c_axis_max'] = 0.08
parametros['zoom_i_m'] = 0
parametros['zoom_f_m'] = 13000
parametros['marcadores_m'] = np.array([1000, 2000, 3000])
parametros['marcadores_texto'] = ['V1', 'V2', 'V3']
parametros['marcadores_waterfall'] = 'no'
parametros['marcadores_color'] = ['r', 'r', 'r']
parametros['guarda_figuras'] = 'no'
parametros['carpeta_figuras'] = 'Figuras'

peli_std(parametros)