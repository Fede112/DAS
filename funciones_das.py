# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 12:02:22 2017

@author: Marco
"""

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import Tkinter as Tk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.pyplot import text

# from multiprocessing import Process
# from timeit import default_timer as timer
import datetime
from funciones4 import header_read
from funciones4 import data_read
import os
from scipy import signal
import sys


def update_progress(progress):
    barLength = 10  # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength * progress))
    text = "\rPercent: [{0}] {1}% {2}".format("#" * block + "-" * (barLength - block), progress * 100, status)
    sys.stdout.write(text)
    sys.stdout.flush()


def peli_std(parametros):
    '''
    Esta función realiza la película de los archivos procesados .std del equipo de medición DAS.
    Para su funcionamiento es necesaria la instalación de la librería ffmpeg (https://es.wikihow.com/instalar-FFmpeg-en-Windows).

    Parameters
    ----------
    time_str: carpeta donde se guarda la adquisición en formato: yy_dd_mm_HH_MM_SS
    c: velocidad de la luz en el vacio
    n: índice de refracción en la fibra
    c_f: velocidad de la luz efectiva (en la fibra)
    offset_m: offset en metros utilizado para la puesta en profundidad/distancia. Utilizado de manera que el cero coincida con la boca de pozo.
    FrecLaser: frecuencia del láser en Hz.
    carpeta: carpeta donde se encuentran las carpetas de adquisición
    texto1: texto que se pone en el video
    texto2: texto que se pone en el video
    zoom_i_m: posición en metros de inicio del video
    zoom_f_m: posición en metros del final del video
    c_axis_min: umbral inferior de la escala de color de la imagen STD
    c_axis_max: umbral superior de la escala de color de la imagen STD
    marcadores_m: array de numpy con la posición en metros de los marcadores verticales del grafico que muestra la intensidad promedio por bin.
    marcadores_texto: lista con los nombres de los marcadores.
    marcadores_waterfall: si uno quiere que los marcadores también aparezcan en el waterfall.
    marcadores_color: lista del mismo tamaño de marcadores_m con los colores que indican los punzados
    titulo_str: título del vdeo
    tiempo_ini: inicio de la carga en formato 'yyyy-mm-dd HH:MM:SS'
    tiempo_fin: fin de la carga en formato 'yyyy-mm-dd HH:MM:SS'
    vector_offset: array de numpy con el offset para la std de tamaño igual al número de columnas de la STD.
    vector_norm:  array de numpy con la normalización para la std de tamaño igual al número de columnas de la STD.
    guarda_figuras: 'si' o 'no'
    carpeta_figuras: Carpeta que se crea dentro de la carpeta STD donde se guardan la figuras. Si la carpeta no existe, se crea.
    output_movie: path donde se guarda el video. El nombre del video debe tener la extensión .mp4

    Output
    ------


    Example
    -------

    from funciones_das import peli_std
    from funciones4 import header_read
    from funciones4 import data_read
    import numpy as np
    import os


    parametros = {}
    parametros['time_str'] = '17_17_11_15_29_20'
    nombre_header = os.path.join(parametros['time_str'], 'STD', 'std.hdr')
    nombre_archivo = os.path.join(parametros['time_str'], 'STD', '000000.std')  # De no tener el 000000.std poner el archivo .std inicial que se tenga.
    header = header_read(nombre_header, nombre_archivo)
    parametros['carpeta'] = ''
    parametros['output_movie'] = os.path.join(parametros['carpeta'], parametros['time_str'], 'STD', 'peli2.mp4')
    parametros['c'] = 299792458.
    parametros['n'] = 1.46879964
    parametros['offset_m'] = 0
    parametros['FrecLaser'] = 2000
    parametros['FilasPeli'] = 2000
    parametros['StepPeli'] = 50
    parametros['c_f'] = parametros['c'] / parametros['n']
    parametros['vector_offset'] = np.zeros(int(header['Cols']))
    parametros['vector_norm'] = np.ones(int(header['Cols']))
    parametros['titulo_str'] = '%02d' % (Titulo)
    parametros['texto1'] = ''
    parametros['texto2'] = ''
    parametros['tiempo_ini'] = '2017-11-17 15:30:00'
    parametros['tiempo_fin'] = '2017-11-18 12:00:00'
    parametros['c_axis_min'] = 0
    parametros['c_axis_max'] = 0.2
    parametros['zoom_i_m'] = 0
    parametros['zoom_f_m'] = 7000
    parametros['marcadores_m'] = np.array([1000, 2000, 3000])
    parametros['marcadores_texto'] = ['V1', 'V2', 'V3']
    parametros['marcadores_waterfall'] = 'no'
    parametros['marcadores_color'] = ['r', 'r', 'r']
    parametros['guarda_figuras'] = 'no'
    parametros['carpeta_figuras'] = 'Figuras'

    peli_std(parametros)


    '''

    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=7, metadata=dict(artist='Marco'), bitrate=-1)

    FrecLaser = parametros['FrecLaser']
    c = parametros['c']
    n = parametros['n']
    c_f = parametros['c_f']

    tiempo_ini = parametros['tiempo_ini']
    tiempo_fin = parametros['tiempo_fin']

    time_str = parametros['time_str']
    marcadores_m = parametros['marcadores_m']
    marcadores_waterfall = parametros['marcadores_waterfall']
    marcadores_texto = parametros['marcadores_texto']
    marcadores_color = parametros['marcadores_color']
    offset_m = parametros['offset_m']
    carpeta_figuras = parametros['carpeta_figuras']

    # Lista los archivos del directorio y se queda con el .std mas grande
    for file in sorted(os.listdir(os.path.join(parametros['time_str'], 'STD')), reverse=True):
        print file
        if file.endswith(".std"):
            path_last_file = os.path.join(time_str, 'STD', file)
            last_file = int(file[:-4])
            break

    # Lista los archivos del directorio y se queda con el .std mas chico (eg. 000000.std)
    for file in sorted(os.listdir(os.path.join(parametros['time_str'], 'STD')), reverse=False):
        print file
        if file.endswith(".std"):
            path_first_file = os.path.join(time_str, 'STD', file)
            break

    header_path = os.path.join(time_str, 'STD', 'std.hdr')
    direfig = os.path.join(time_str, 'STD', carpeta_figuras)
    filas = parametros['FilasPeli']
    step = float(parametros['StepPeli'])
    guarda_figuras = parametros['guarda_figuras']
    vector_offset = parametros['vector_offset']
    vector_norm = parametros['vector_norm']
    zoom_i_m = parametros['zoom_i_m']
    zoom_f_m = parametros['zoom_f_m']
    c_axis_min = parametros['c_axis_min']
    c_axis_max = parametros['c_axis_max']
    output_movie = parametros['output_movie']
    titulo_str = parametros['titulo_str']

    # Abro el header tomando el last_file para ver su tamano en filas
    header = header_read(header_path, path_last_file)
    delta_t = header['FreqRatio'] * 5e-9
    delta_x = c_f * delta_t / 2
    filas_last_file = header['Fils']

    # Abro el header tomando el first_file para ver como se ve un archivo completo
    header = header_read(header_path, path_first_file)
    filas_0 = header['Fils']
    nShotsChk = header['nShotsChk']

    sec_per_fila = nShotsChk / FrecLaser
    sec_per_file = filas_0 * sec_per_fila
    print "sec_per_file %.2f" % sec_per_file
    print "sec_per_fila %.2f" % sec_per_fila

    zoom_i = (zoom_i_m - offset_m) / delta_x
    zoom_f = (zoom_f_m - offset_m) / delta_x

    marcadores_bin = (marcadores_m - offset_m) / delta_x

    if guarda_figuras == 'si':
        if (os.path.isdir(direfig) == 0):
            os.mkdir(direfig)

    ano = time_str[0:2]
    ano = '20' + ano

    dia = time_str[3:5]
    mes = time_str[6:8]

    hora = time_str[9:11]
    minuto = time_str[12:14]
    seg = time_str[15:17]

    # este paso lo hace porque el programa guarda la carpeta como ano + dia + mes en lugar de ano + mes + dia
    tiempo_0 = ano + '-' + mes + '-' + dia + ' ' + hora + ':' + minuto + ':' + seg
    tiempo_0_date = datetime.datetime.strptime(tiempo_0, '%Y-%m-%d %H:%M:%S')

    if tiempo_ini == '':
        tiempo_ini_date = tiempo_0_date
    else:
        tiempo_ini_date = datetime.datetime.strptime(tiempo_ini, '%Y-%m-%d %H:%M:%S')

    if tiempo_fin == '':
        # le agrego a tiempo_0_date la cantidad de archivos*sec_per_file. Le resto 1 segundo para que no se pase.
        tiempo_fin_date = tiempo_0_date + datetime.timedelta(0, (last_file) * sec_per_file + filas_last_file * sec_per_fila - 1)  # agrega segundos a datetime como: timedelta(days, seconds, then other fields).
    else:
        tiempo_fin_date = datetime.datetime.strptime(tiempo_fin, '%Y-%m-%d %H:%M:%S')

    tiempo_actual = tiempo_ini_date

    dif_time_date_ini = tiempo_ini_date - tiempo_0_date
    dif_time_date_fin = tiempo_fin_date - tiempo_0_date
    dif_time_date_ini_sec = dif_time_date_ini.total_seconds()
    dif_time_date_fin_sec = dif_time_date_fin.total_seconds()

    dif_time_sec = dif_time_date_fin_sec - dif_time_date_ini_sec

    print 'dif_time_date_fin_sec: %.2f' % dif_time_date_fin_sec
    print 'dif_time_date_ini_sec: %.2f' % dif_time_date_ini_sec
    ini_file = int(dif_time_date_ini_sec / sec_per_file)
    ini_fila = (dif_time_date_ini_sec % sec_per_file) / sec_per_fila
    # Hago que ini_fila sea multiplo del step
    ini_fila = filas_0 - np.ceil((filas_0 - ini_fila) / step) * step  # redondeo para que ini_fila sea divisor entero de filas_0
    fin_file = int(dif_time_date_fin_sec / sec_per_file)
    fin_fila = (dif_time_date_fin_sec % sec_per_file) / sec_per_fila
    # Hago que fin_fila sea multiplo del step
    fin_fila = filas_0 - np.floor((filas_0 - fin_fila) / step) * step

    print 'dif_time_sec: %.2f' % dif_time_sec
    print 'dif_time_sec_from_files: %.2f' % ((float(fin_file - ini_file + 1)) * float(filas_0) * sec_per_fila)

    print "ini_file: %.2f" % ini_file
    print "fin_file: %.2f" % fin_file

    print "ini_fila: %.2f" % ini_fila
    print "fin_fila: %.2f" % fin_fila

    print 'fecha final total: ' + datetime.datetime.strftime(tiempo_0_date + datetime.timedelta(0, last_file * sec_per_file + filas_last_file * sec_per_fila - 1), '%Y-%m-%d %H:%M:%S')

    # ERRORES en los parametros de entrada:

    # StepPeli
    if (filas_0 % step) != 0:
        sys.exit(u'StepPeli debe ser divisor de la cantidad filas en un archivo: %.1f' % filas_0)

    # marcadores
    if len(marcadores_m) != len(marcadores_color):
        sys.exit(u'La cantidad de lineas verticales, [marcadores_m], no coincide con la cantidad de colores especificados, [marcadores_color], para dichas lineas.')

    # Verificaciones del tiempo inicial y final
    if tiempo_fin_date <= tiempo_ini_date:
        sys.exit(u'El tiempo inicial debe ser menor al tiempo final.')

    if fin_file > last_file:
        sys.exit(u'No existen datos hasta esa fecha final. Hay datos hasta el ' + datetime.datetime.strftime(tiempo_0_date + datetime.timedelta(0, (last_file + 1.) * sec_per_file - 1), '%Y-%m-%d %H:%M:%S'))

    if dif_time_date_ini_sec < 0:
        sys.exit(u'No existen datos anteriores a el: ' + datetime.datetime.strftime(tiempo_0_date, '%Y-%m-%d %H:%M:%S'))

    vec_cols = np.array([0, header['Cols'] - 1], dtype=np.uint64)
    cols_to_read = vec_cols[1] - vec_cols[0] + 1
    columnas = int(cols_to_read)

    data = np.zeros((int(filas), columnas), dtype=eval(header['PythonNpDataType']))
    promedio = np.zeros(columnas, dtype=np.float32)

    vec_fils = np.array([0, int(step) - 1], dtype=np.uint64)
    header, vector = data_read(header_path, path_first_file, vec_fils, vec_cols)

    data[0:int(step):] = vector

    def updatefig(j, offset_m, tiempo_actual):
        global pl1, pl2

        file_num = ini_file + (ini_fila + j * step) / filas_0  # numero del archivo
        file_num_str = '%06d' % (file_num)  # lo paso a string
        path = os.path.join(time_str, 'STD', file_num_str + '.std')

        inicio = (j * step + ini_fila) % filas_0  # indice de la primer fila a leer en cada iteración
        vec_fils = np.array([inicio, inicio + step - 1], dtype=np.uint64)  # define el rango de filas a leer (lee el # de filas determinado en 'step')

        header, vector = data_read(header_path, path, vec_fils, vec_cols)  # lee los datos y los recupera en el vector 2d

        for k in range(int(step)):
            vector[k, :] = (vector[k, :] - vector_offset) * vector_norm  # le resta el offset y le agrega una normalización

        f = j % (filas / step)  # resto de iteración / iteraciones en un waterfall completo

        data = root.data
        if (f == 0):
            data = np.zeros((filas, columnas), dtype=eval(header['PythonNpDataType']))

        data[int(f * step):int((f + 1) * step):] = vector  # va sumandole a data las filas (# = step) obtenidas en cada iteración
        root.data = data

        # Actualización del Subplot Waterfall
        im.set_array(data)
        im.set_clim([c_axis_min, c_axis_max])
        ticks = ax.get_xticks()
        ax.set_xticklabels(np.round(ticks * delta_x + float(offset_m)))
        ax.set_xlim([zoom_i, zoom_f])
        ticks = ax.get_yticks()
        ax.set_yticklabels(np.round(ticks * header['nShotsChk'] / FrecLaser))
        ax.set_xlabel(u'Posición [m]')
        ax.set_ylabel('Tiempo [seg]')

        # j = j + 1  # no hace falta el + 1
        tiempo_actual = tiempo_actual + datetime.timedelta(seconds=(j + 1) * step * header['nShotsChk'] / FrecLaser)
        time_str1 = datetime.datetime.strftime(tiempo_actual, '%Y-%m-%d %H:%M:%S')

        tiempo_label.set_text(time_str1)

        promedio = root.promedio

        actual = np.mean(vector, axis=0)
        promedio = (promedio * (j) + actual) / (j + 1)

        root.promedio = promedio

        # Actualización del Subplot de los Promedios
        ax1.cla()
        pl1 = ax1.plot(promedio)
        pl2 = ax1.plot(actual, 'r')
        if len(marcadores_texto) == 0:
            ax1.xaxis.set_ticklabels([0] * len(marcadores_bin))
        else:
            ax1.xaxis.set_ticklabels(marcadores_texto)
        ax1.xaxis.set_ticks(marcadores_bin)
        ax1.xaxis.set_ticks_position('top')

        ax1.set_xlim([zoom_i, zoom_f])
        ax1.set_ylim([c_axis_min, c_axis_max])

        # Grafico lineas verticales en ambos subplots
        for k in range(marcadores_bin.shape[0]):
            ax1.axvline(x=marcadores_bin[k], color=marcadores_color[k])
            if marcadores_waterfall == 'si':
                ax.axvline(x=marcadores_bin[k], color=marcadores_color[k])

        inttostr = '%05d' % (j + 1)

        if guarda_figuras == 'si':
            figname = direfig + "figura_" + inttostr
            fig.savefig(figname + '.png', dpi=250)

        if (j == frames_tot):
            ani.event_source.stop()
            plt.close('all')

        print '%2.2f' % (float(j + 1) / float(frames_tot) * 100.), ' %'

    #    ax2.cla()
    #    pl2 = ax2.plot(actual-promedio)
    #    ax2.set_ylim([-0.15,0.15])
    #    ax2.axes.xaxis.set_ticklabels([])
    #    ax2.set_xlim([0,columnas])

    root = Tk.Tk()

    # root.overrideredirect(True)
    # root.overrideredirect(False)
    # root.attributes('-fullscreen',True)

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)
    root.grid_columnconfigure(3, weight=1)
    root.grid_columnconfigure(4, weight=1)
    root.grid_columnconfigure(5, weight=1)
    root.grid_columnconfigure(6, weight=1)
    root.grid_columnconfigure(7, weight=1)
    root.grid_columnconfigure(8, weight=1)
    root.grid_columnconfigure(9, weight=1)

    # Inicio la figura
    label = Tk.Label(root, text="ADQUISICION DAS").grid(column=0, row=0, columnspan=10)
    fig = Figure(figsize=(14, 6), dpi=250)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().grid(column=0, row=1, columnspan=10)

    # Suplot del Waterfall
    ax = fig.add_axes([.1, .1, .8, .62])
    im = ax.imshow(data, cmap=plt.get_cmap('jet'), aspect='auto', interpolation='none')
    fig.colorbar(im)
    tiempo_label = ax.text(1.02, 1.1, 'T:' + str(0), horizontalalignment='left', transform=ax.transAxes, color='k')
#    cierre_label = ax.text(1.02,1.25,'Cierre de pozo: ' + cierre_str,horizontalalignment='left', transform=ax.transAxes, color='k')
#    abre_label = ax.text(1.02,1.20,'Apertura de pozo: ' + ap_str,horizontalalignment='left', transform=ax.transAxes, color='k')
    titulo = ax.text(1.02, 1.35, titulo_str, horizontalalignment='left', transform=ax.transAxes, color='k')

    # Suplot de los promedios
    ax1 = fig.add_axes([.1, .76, .64, .15])
    pl1 = ax1.plot(promedio)
    ax1.set_xlim([0, columnas])
    ax1.set_ylim([-0.001, 0.001])
    if (len(marcadores_texto) == 0):
        ax1.xaxis.set_ticklabels([] * len(marcadores_bin))
    else:
        ax1.xaxis.set_ticklabels(marcadores_texto)
    ax1.xaxis.set_ticks(marcadores_bin)
    ax1.xaxis.set_ticks_position('top')
    root.promedio = promedio
    root.data = data

    # ax2 = fig.add_axes([.1,.88,.64,.11])
    # pl2 = ax1.plot(promedio)
    # ax2.axes.xaxis.set_ticklabels([])
    # ax2.set_xlim([0,columnas])
    # ax2.set_ylim([-0.001,0.001])

    # i = ini_file
    # total_filas = 0
    # header_i = header_read(header_path, path)
    # if not fin_file:
    #     while (1):
    #         file_num = '%06d' % (i)
    #         path = os.path.join(time_str, 'STD', file_num + '.std')
    #         if (os.path.isfile(path)):
    #             header_i = header_read(header_path, path)
    #             total_filas += header_i['Fils']
    #         else:
    #             break
    #         i = i + 1
    # else:
    #     total_filas = header_i['Fils'] * (fin_file - ini_file + 1)

    # frames_tot = int(total_filas / step - 1)

    frames_tot = int((((fin_file - ini_file + 1) * filas_0 - (ini_fila) - (filas_0 - fin_fila)) / step))
    # frames_tot = int((fin_file - ini_file) * filas_0)

    print "frames_tot: %.2f" % frames_tot
    print "filas: %.2f" % filas  # filas peli
    print "filas_0: %.2f" % filas_0  # filas por archivo
    print "filas inicial:  %.2f" % ini_fila
    print "filas final:  %.2f" % fin_fila
    print "frames total:  %.2f" % frames_tot
    print tiempo_ini
    print tiempo_fin
    print "total time: %.2f" % (frames_tot * step * sec_per_fila / 60.)
    ani = animation.FuncAnimation(fig, updatefig, interval=0.2, blit=False, fargs=(offset_m, tiempo_actual), frames=frames_tot, repeat=False)
    ani.save(output_movie, writer=writer, dpi=250)
    # plt.show()
    # Tk.mainloop()


def carga_std(parametros):
    '''
    Esta función carga la matriz STD (filas=tiempo, col=bines) de los archivos procesados .std del equipo de medición DAS.
    Aparte genera un grafico de los datos que guarda en un directorio nuevo llamado 'Figuras'.

    Parameters
    ----------
    time_str: carpeta donde se guarda la adquisición en formato: yy_dd_mm_HH_MM_SS
    c: velocidad de la luz en el vacio
    n: índice de refracción en la fibra
    c_f: velocidad de la luz efectiva (en la fibra)
    offset_m: offset en metros utilizado para la puesta en profundidad/distancia. Utilizado de manera que el cero coincida con la boca de pozo.
    FrecLaser: frecuencia del láser en Hz.
    zoom_i_m: posición en metros de inicio del video
    zoom_f_m: posición en metros del final del video
    c_axis_min: umbral inferior de la escala de color de la imagen STD
    c_axis_max: umbral superior de la escala de color de la imagen STD
    marcadores_m: array de numpy con la posición en metros de los marcadores verticales del grafico que muestra la intensidad promedio por bin.
    marcadores_texto: lista con los nombres de los marcadores.
    marcadores_waterfall: si uno quiere que los marcadores también aparezcan en el waterfall.
    marcadores_color: lista del mismo tamaño de marcadores_m con los colores que indican los punzados
    titulo_str: título del video
    vector_offset: array de numpy con el offset para la std de tamaño igual al número de columnas de la STD.
    vector_norm:  array de numpy con la normalización para la std de tamaño igual al número de columnas de la STD.
    tiempo_ini: inicio de la carga en formato 'yyyy-mm-dd HH:MM:SS'
    tiempo_fin: fin de la carga en formato 'yyyy-mm-dd HH:MM:SS'
    guarda_figuras: 'si' o 'no'
    carpeta_figuras: Carpeta que se crea dentro de la carpeta STD donde se guardan la figuras. Si la carpeta no existe, se crea.
    num_figura: número de la figura a guardar

    Output
    ------
    matriz: matriz STD. El número de columnas es el de toda la STD. El número de filas, el correspondiente entre los tiempo_ini y tiempo_fin
    tiempo_filas_std: lista con los tiempos correspondientes a cada fila. El tamaño de la lista es igual al número de filas de la matriz.
    pos_bin: numpy array con la posición en metros correspondiente a cada bin. El tamaño del vector es igual al número de columnas de la matriz.


    Example
    -------
    # Verificar FrecLaser, tiempo_ini y tiempo_fin
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
    parametros['marcadores_texto'] = ['V1', 'V2', 'V3']
    parametros['marcadores_waterfall'] = 'no'
    parametros['marcadores_color'] = ['r', 'r', 'r']
    parametros['titulo_str'] = 'Oleoducto Restinga'
    parametros['tiempo_ini'] = '2017-11-22 12:40:00'
    parametros['tiempo_fin'] = '2017-11-22 12:50:00'
    parametros['guarda_figuras'] = 'si'
    parametros['carpeta_figuras'] = 'Figuras'
    parametros['num_figura'] = 1

    matriz, tiempo_filas_std, pos_bin, = carga_std(parametros)



    '''

    time_str = parametros['time_str']
    FrecLaser = parametros['FrecLaser']
    tiempo_ini = parametros['tiempo_ini']
    tiempo_fin = parametros['tiempo_fin']
    vector_offset = parametros['vector_offset']
    vector_norm = parametros['vector_norm']

    ano = time_str[0:2]
    ano = '20' + ano

    dia = time_str[3:5]
    mes = time_str[6:8]

    hora = time_str[9:11]
    minuto = time_str[12:14]
    seg = time_str[15:17]

    # los files se guardan como ano+dia+mes => reacomodo el string para que sea compatible con datetime
    tiempo_0 = ano + '-' + mes + '-' + dia + ' ' + hora + ':' + minuto + ':' + seg
    tiempo_0_date = datetime.datetime.strptime(tiempo_0, '%Y-%m-%d %H:%M:%S')

    tiempo_ini_date = datetime.datetime.strptime(tiempo_ini, '%Y-%m-%d %H:%M:%S')
    tiempo_fin_date = datetime.datetime.strptime(tiempo_fin, '%Y-%m-%d %H:%M:%S')

    dif_time_date_ini = tiempo_ini_date - tiempo_0_date
    dif_time_date_fin = tiempo_fin_date - tiempo_0_date
    dif_time_date_ini_sec = dif_time_date_ini.total_seconds()
    dif_time_date_fin_sec = dif_time_date_fin.total_seconds()

    # dif_time = dif_time_date_fin - dif_time_date_ini
    dif_time_sec = dif_time_date_fin_sec - dif_time_date_ini_sec

    nombre_header = os.path.join(time_str, 'STD', 'std.hdr')
    nombre_archivo = os.path.join(time_str, 'STD', '000000.std')
    header = header_read(nombre_header, nombre_archivo)

    nShotsChk = header['nShotsChk']
    sec_per_fila = nShotsChk / FrecLaser
    filas = header['Fils']
    sec_per_file = filas * sec_per_fila

    ini_file = int(dif_time_date_ini_sec / sec_per_file)
    ini_fila = (dif_time_date_ini_sec % sec_per_file) / sec_per_fila
    fin_file = int(dif_time_date_fin_sec / sec_per_file)
    fin_fila = (dif_time_date_fin_sec % sec_per_file) / sec_per_fila

    filas_tot = int(dif_time_sec / sec_per_fila)
    cols = int(header['Cols'])

    matriz = np.zeros([filas_tot, cols])
    vec_cols = np.array([0, cols - 1], dtype=np.uint64)
    ind_fila = 0

    print 'Cargando STD: '
    for i in range(ini_file, fin_file + 1):
        file_num = '%06d' % i
        print file_num
        path = os.path.join(time_str, 'STD', file_num + '.std')
        header = header_read(nombre_header, path)

        if (ini_file == fin_file):
            vec_fils = np.array([ini_fila, fin_fila - 1])
        else:
            if (i == ini_file):
                vec_fils = np.array([ini_fila, header['Fils'] - 1])
            elif (i == fin_file):
                vec_fils = np.array([0, fin_fila - 1])
            else:
                vec_fils = np.array([0, header['Fils'] - 1])

        header, vector = data_read(nombre_header, path, vec_fils, vec_cols)

        for k in range(vector.shape[0]):
            vector[k, :] = (vector[k, :] - vector_offset) * vector_norm

        fila = vector.shape[0]

        matriz[ind_fila:ind_fila + fila, :] = vector
        ind_fila = ind_fila + fila

        update_progress((i + 1) / (fin_file + 1 - ini_file))

    # Cargo parametros para graficar
    titulo_str = parametros['titulo_str']
    zoom_i_m = parametros['zoom_i_m']
    zoom_f_m = parametros['zoom_f_m']
    c = parametros['c']
    n = parametros['n']
    c_f = parametros['c_f']
    offset_m = parametros['offset_m']
    carpeta_figuras = parametros['carpeta_figuras']
    c_axis_min = parametros['c_axis_min']
    c_axis_max = parametros['c_axis_max']
    guarda_figuras = parametros['guarda_figuras']
    direfig = os.path.join(time_str, 'STD', carpeta_figuras)
    num_figura = parametros['num_figura']
    marcadores_m = parametros['marcadores_m']
    marcadores_waterfall = parametros['marcadores_waterfall']
    marcadores_texto = parametros['marcadores_texto']
    marcadores_color = parametros['marcadores_color']

    # Busco errores en los parametros
    if len(marcadores_m) != len(marcadores_color):
        sys.exit(u'La cantidad de lineas verticales, [marcadores_m], no coincide con la cantidad de colores especificados, [marcadores_color], para dichas lineas.')

    if guarda_figuras == 'si':
        if (os.path.isdir(direfig) == 0):
            os.mkdir(direfig)

    delta_t = header['FreqRatio'] * 5e-9
    delta_x = c_f * delta_t / 2
    zoom_i = (zoom_i_m - offset_m) / delta_x
    zoom_f = (zoom_f_m - offset_m) / delta_x
    marcadores_bin = (marcadores_m - offset_m) / delta_x

    # Grafico
    promedio = np.mean(matriz, axis=0)
    fig = plt.figure(figsize=(16, 8))
    fig.patch.set_facecolor('white')

    # Subplot Waterfall
    ax = fig.add_axes([.15, .1, .8, .62])
    im = ax.imshow(matriz, cmap=plt.get_cmap('jet'), aspect='auto', interpolation='none')
    im.set_clim([c_axis_min, c_axis_max])
    fig.colorbar(im)
    tiempo_label = ax.text(1.02, 1.1, 'T:' + tiempo_ini, horizontalalignment='left', transform=ax.transAxes, color='k')
    ax.text(1.02, 1.35, titulo_str, horizontalalignment='left', transform=ax.transAxes, color='k', weight='bold')
    ax.set_xlim([zoom_i, zoom_f])
    ticks = ax.get_xticks()
    ax.set_xticklabels(np.round(ticks * delta_x + float(offset_m)))
    ticks = ax.get_yticks()
    tiempo_inii = datetime.datetime.strptime(tiempo_ini, '%Y-%m-%d %H:%M:%S')
    tiempo_ini_t = []
    for i in range(len(ticks)):
        tt = tiempo_inii + datetime.timedelta(seconds=ticks[i] * header['nShotsChk'] / FrecLaser)
        tiempo_ini_t.append(tt)

    ax.set_yticklabels(tiempo_ini_t)
    ax.set_xlabel(u'Posición [m]')
    ax.set_ylabel('Tiempo')

    # Subplot Promedio Superior
    ax1 = fig.add_axes([.15, .76, .64, .15])
    ax1.plot(promedio)
    if (len(marcadores_texto) == 0):
        ax1.xaxis.set_ticklabels([] * len(marcadores_bin))
    else:
        ax1.xaxis.set_ticklabels(marcadores_texto)
    ax1.xaxis.set_ticks(marcadores_bin)
    ax1.xaxis.set_ticks_position('top')

    ax1.set_xlim([zoom_i, zoom_f])
    ax1.set_ylim([c_axis_min, c_axis_max])

    # Grafico lineas verticales en ambos subplots
    for k in range(marcadores_bin.shape[0]):
        ax1.axvline(x=marcadores_bin[k], color=marcadores_color[k])
        if marcadores_waterfall == 'si':
            ax.axvline(x=marcadores_bin[k], color=marcadores_color[k])

    tiempo_label.set_text(tiempo_ini)

    inttostr = '%05d' % (num_figura)

    if guarda_figuras == 'si':
        figname = "figura_" + inttostr + '.png'
        # print figname
        figpath = os.path.join(direfig, figname)
        # print figpath
        fig.savefig(figpath, dpi=300)

    # Posicion de los bines
    bines = np.linspace(0, cols, num=cols)
    pos_bin = bines * delta_x + float(offset_m)

    # Filas tiempo
    tiempo_filas_std = []
    tiempo_inii = datetime.datetime.strptime(tiempo_ini, '%Y-%m-%d %H:%M:%S')
    for i in range(filas_tot):
        tt = tiempo_inii + datetime.timedelta(seconds=i * header['nShotsChk'] / FrecLaser)
        tiempo_filas_std.append(tt)

    # plt.show()

    return matriz, tiempo_filas_std, pos_bin,


# plt.imshow(matriz, cmap=plt.get_cmap('jet'), aspect='auto', interpolation='none')


from scipy.signal import butter, lfilter, filtfilt


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data, axis=0)
    return y


def procesa_std_fft(parametros):
    '''
    Esta función realiza el procesamiento del dato crudo con los parámetros especificados y luego realiza la STD. También realiza la FFT del dato filtrado.

    Parameters
    ----------
    time_str: carpeta donde se guarda la adquisición en formato: yy_dd_mm_HH_MM_SS
    c: velocidad de la luz en el vacio
    n: índice de refracción en la fibra
    c_f: velocidad de la luz efectiva (en la fibra)
    offset_m: offset en metros utilizado para la puesta en profundidad/distancia. Utilizado de manera que el cero coincida con la boca de pozo.
    FrecLaser: frecuencia del láser en Hz.
    zoom_i_m: posición en metros de inicio del video
    zoom_f_m: posición en metros del final del video
    c_axis_min: umbral inferior de la escala de color de la imagen STD
    c_axis_max: umbral superior de la escala de color de la imagen STD
    marcadores_m: array de numpy con la posición en metros de los marcadores
    colores_m: lista del mismo tamaño de marcadores_m con los colores que indican los punzados
    titulo_str: título del vdeo
    vector_offset: array de numpy con el offset para la std de tamaño igual al número de columnas de la STD.
    vector_norm:  array de numpy con la normalización para la std de tamaño igual al número de columnas de la STD.
    tiempo_ini: inicio de la carga en formato 'yyyy-mm-dd HH:MM:SS'
    tiempo_fin: fin de la carga en formato 'yyyy-mm-dd HH:MM:SS'
    guarda_figuras: 'si' o 'no'
    carpeta_figuras: Carpeta que se crea dentro de la carpeta STD donde se guardan la figuras. Si la carpeta no existe, se crea.
    num_figura = número de la figura a guardar
    window_time_data: cantidad de shots de dato crudo que se promedian
    window_bin_data: cantidad de bines de dato crudo que se promedian
    window_bin: ventana del moving average que se realiza de la STD
    window_bin_mean: ventana del moving_average que se realiza del valor medio de la señal, utilizado para normalizar la STD.
    std_step_sec: periodo de muestreo de la matriz STD
    butter_filter: 'si' o 'no' aplica filtro pasabanda de tipo butterworth. Falta chequear que lo hace bien, por ahora poner 'no'.
    butter_lp_frec: frecuencia de corte pasabajos
    butter_hp_frec: frecuencia de corte pasaaltos
    butter_order: orden del filtro
    fft_step_sec: intervalo en segundos donde se realiza la FFT. El archivo total se divide en intervalos de duración FFT_step_sec y luego se realiza el promedio entre ellos.
                    Si está vacio ([]) es la FFT sin promediar
    c_axis_min_fft: umbral inferior de la escala de color de la imagen FFT
    c_axis_max_fft: umbral superior de la escala de color de la imagen FFT
    titulo_str_fft: título de la figura FFT

    Output
    ------
    std: matriz STD. El número de columnas es el correspondiente al rango [zoom_i_m, zoom_f_m]. El número de filas, el correspondiente entre los tiempo_ini y tiempo_fin
    data_fft_tot: matriz FFT. El número de columnas es el correspondiente al rango [zoom_i_m, zoom_f_m]. El número de filas, el correspondiente entre las frecuencias 0 y FrecLaser/2
    tiempo_filas_std: lista con los tiempos correspondientes a cada fila. El tamaño de la lista es igual al número de filas de la matriz STD.
    pos_bin_std: numpy array con la posición en metros correspondiente a cada bin. El tamaño del vector es igual al número de columnas de la matriz STD.
    frq: numpy array con las frecuencias de la FFT. El tamaño del vector es igual al número de filas de la matriz FFT.
    pos_bin_fft: numpy array con la posición en metros correspondiente a cada bin de la FFT. El tamaño del vector es igual al número de columnas de la matriz FFT.

    Example
    -------
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
    parametros['zoom_f_m'] = 5900
    parametros['c_axis_min'] = 0
    parametros['c_axis_max'] = 0.08
    parametros['punzados_m'] = np.array([])  # np.array([3800,3795,3689,3665,3580,3565,3499,3478,3462,3425,3411])
    parametros['colores_m'] = []  # ['r','r','g','g','k','k','r','r','r','c','c']
    parametros['titulo_str'] = 'Retro a 4 m de la traza'
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


    '''

    time_str = parametros['time_str']
    FrecLaser = parametros['FrecLaser']
    tiempo_ini = parametros['tiempo_ini']
    tiempo_fin = parametros['tiempo_fin']
    zoom_i_m = parametros['zoom_i_m']
    zoom_f_m = parametros['zoom_f_m']
    offset_m = parametros['offset_m']
    c = parametros['c']
    n = parametros['n']
    c_f = parametros['c_f']
    c_axis_min = parametros['c_axis_min']
    c_axis_max = parametros['c_axis_max']

    ano = time_str[0: 2]
    ano = '20' + ano

    dia = time_str[3: 5]
    mes = time_str[6: 8]

    hora = time_str[9: 11]
    minuto = time_str[12: 14]
    seg = time_str[15: 17]

    tiempo_0 = ano + '-' + mes + '-' + dia + ' ' + hora + ':' + minuto + ':' + seg
    tiempo_0_date = datetime.datetime.strptime(tiempo_0, '%Y-%m-%d %H:%M:%S')

    tiempo_ini_date = datetime.datetime.strptime(tiempo_ini, '%Y-%m-%d %H:%M:%S')
    tiempo_fin_date = datetime.datetime.strptime(tiempo_fin, '%Y-%m-%d %H:%M:%S')

    dif_time_date_ini = tiempo_ini_date - tiempo_0_date
    dif_time_date_fin = tiempo_fin_date - tiempo_0_date
    dif_time_date_ini_sec = dif_time_date_ini.total_seconds()
    dif_time_date_fin_sec = dif_time_date_fin.total_seconds()

    dif_time = dif_time_date_fin - dif_time_date_ini
    dif_time_sec = dif_time.total_seconds()

    header_path = os.path.join(time_str, 'RAW_CH0', 'ch0.hdr')
    file_path = os.path.join(time_str, 'RAW_CH0', '000000.bin')
    header = header_read(header_path, file_path)

    delta_t = header['FreqRatio'] * 5e-9
    delta_x = c_f * delta_t / 2
    zoom_i = int((zoom_i_m - offset_m) / delta_x)
    zoom_f = int((zoom_f_m - offset_m) / delta_x)
    vec_cols = np.array([zoom_i, zoom_f], dtype=np.uint64)

    nShotsChk = header['nShotsChk']
    sec_per_fila = 1 / float(FrecLaser)
    filas = header['Fils']
    sec_per_file = filas * sec_per_fila

    ini_file = int(dif_time_date_ini_sec / sec_per_file)
    ini_fila = dif_time_date_ini_sec % sec_per_file / sec_per_fila
    fin_file = int(dif_time_date_fin_sec / sec_per_file)
    fin_fila = dif_time_date_fin_sec % sec_per_file / sec_per_fila

    filas_tot = int(dif_time_sec / sec_per_fila)
    cols = int(vec_cols[1] - vec_cols[0] + 1)

    data = np.zeros([filas_tot, cols])
    ind_fila = 0
    print 'Cargando Dato Crudo: '
    for i in range(ini_file, fin_file + 1):
        file_num = '%06d' % (i)
        file_i_path = os.path.join(time_str, 'RAW_CH0', file_num + '.bin')
        header = header_read(header_path, file_i_path)

        if (ini_file == fin_file):
            vec_fils = np.array([ini_fila, fin_fila - 1])
        else:
            if (i == ini_file):
                vec_fils = np.array([ini_fila, header['Fils'] - 1])
            elif (i == fin_file):
                vec_fils = np.array([0, fin_fila - 1])
            else:
                vec_fils = np.array([0, header['Fils'] - 1])

        header, vector = data_read(header_path, file_i_path, vec_fils, vec_cols)

        fila = vector.shape[0]
        data[ind_fila: ind_fila + fila, :] = vector
        ind_fila = ind_fila + fila

        update_progress((i + 1) / (fin_file + 1 - ini_file))

    window_time_data = parametros['window_time_data']
    window_bin_data = parametros['window_bin_data']
    window_bin = parametros['window_bin']
    window_bin_mean = parametros['window_bin_mean']
    std_step_sec = parametros['std_step_sec']

    # Filtro 2d con kernel uniforme
    kernel = np.ones([window_time_data, window_bin_data])
    kernel = kernel / float(window_time_data) / float(window_bin_data)
    data_mean = signal.convolve2d(data, kernel, mode='valid')

    carpeta_figuras = parametros['carpeta_figuras']
    guarda_figuras = parametros['guarda_figuras']
    num_figura = parametros['num_figura']
    direfig = os.path.join(time_str, 'RAW_CH0', carpeta_figuras)
    if guarda_figuras == 'si':
        if (os.path.isdir(direfig) == 0):
            os.mkdir(direfig)

    # Filtro Butterworth
    butter_filter = parametros['butter_filter']
    butter_lp_frec = parametros['butter_lp_frec']
    butter_hp_frec = parametros['butter_hp_frec']
    butter_order = parametros['butter_order']

    if butter_filter == 'si':
        data_mean = butter_bandpass_filter(data_mean, butter_lp_frec, butter_hp_frec, FrecLaser, order=butter_order)

    filas_tot = data_mean.shape[0]
    cols_tot = data_mean.shape[1] - window_bin + 1
    steps = int(filas_tot / FrecLaser / std_step_sec)

    std = np.zeros([steps, cols_tot])
    v_conv = np.ones(window_bin) / window_bin

    v_conv_m = np.ones(window_bin_mean) / window_bin_mean

    # Hace la STD
    print 'Procesando STD: '
    for i in range(steps):
        norm_factor = np.mean(data_mean[int(i * FrecLaser * std_step_sec): int((i + 1) * FrecLaser * std_step_sec), :], axis=0)
        norm_factor = np.convolve(norm_factor, v_conv_m, mode='same')
        std_i = np.std(data_mean[int(i * FrecLaser * std_step_sec): int((i + 1) * FrecLaser * std_step_sec), :], axis=0) / norm_factor
        std_i = np.convolve(std_i, v_conv, mode='valid')
        std[i, :] = std_i
        update_progress((i + 1) / steps)

    titulo_str = parametros['titulo_str']
    titulo_str_fft = parametros['titulo_str_fft']

    # Figura STD
    fig = plt.figure(figsize=(16, 8))
    ax = fig.add_axes([.15, .1, .8, .62])
    im = ax.imshow(std, cmap=plt.get_cmap('jet'), aspect='auto', interpolation='none')
    im.set_clim([c_axis_min, c_axis_max])
    fig.colorbar(im)
    ticks = ax.get_xticks()
    tiempo_label = ax.text(1.02, 1.1, 'T:' + tiempo_ini, horizontalalignment='left', transform=ax.transAxes, color='k')
    ax.text(1.02, 1.35, titulo_str, horizontalalignment='left', transform=ax.transAxes, color='k')
    ax.set_xticklabels(np.round(ticks * delta_x + vec_cols[0] * delta_x + float(offset_m)))
    ticks = ax.get_yticks()
    tiempo_inii = datetime.datetime.strptime(tiempo_ini, '%Y-%m-%d %H:%M:%S')
    tiempo_ini_t = []
    for i in range(len(ticks)):
        tt = tiempo_inii + datetime.timedelta(seconds=ticks[i] * std_step_sec)
        tiempo_ini_t.append(tt)
    ax.set_yticklabels(tiempo_ini_t)
    ax.set_xlabel(u'Posición [m]')
    ax.set_ylabel('Tiempo')

    std_mean = np.mean(std, axis=0)
    ax1 = fig.add_axes([.15, .76, .64, .15])
    ax1.plot(std_mean, '-b')
    ax1.set_xlim([0, std_mean.shape[0] - 1])
    ax1.axes.xaxis.set_ticklabels([])
    ax1.set_ylim([c_axis_min, c_axis_max])

    # Guarda figura
    inttostr = '%05d' % (num_figura)
    if guarda_figuras == 'si':
        figname = os.path.join(direfig, 'figura_' + inttostr + '_std.png')
        fig.savefig(figname, dpi=300)

    # Posicion de los bines std
    bines = np.linspace(0, cols_tot, num=cols_tot)
    pos_bin_std = bines * delta_x + vec_cols[0] * delta_x + float(offset_m)

    # Filas tiempo
    tiempo_filas_std = []
    tiempo_inii = datetime.datetime.strptime(tiempo_ini, '%Y-%m-%d %H:%M:%S')
    for i in range(steps):
        tt = tiempo_inii + datetime.timedelta(seconds=i * std_step_sec)
        tiempo_filas_std.append(tt)

    # FFT
    fft_step_sec = parametros['fft_step_sec']
    c_axis_min_fft = parametros['c_axis_min_fft']
    c_axis_max_fft = parametros['c_axis_max_fft']

    if not fft_step_sec:
        fft_step_sec = filas_tot / FrecLaser

    steps = int(filas_tot / (FrecLaser * fft_step_sec))
    data_fft_tot = []
    print 'Procesando FFT: '
    for i in range(steps):
        data_mean_i = data_mean[i * FrecLaser * fft_step_sec: (i + 1) * FrecLaser * fft_step_sec, :]
        data_fft = np.fft.fft(data_mean_i, axis=0)
        data_fft = abs(data_fft)
        n = data_mean_i.shape[0]
        data_fft = data_fft[range(n / 2 + 1), :]
        data_fft_tot = + data_fft

        update_progress((i + 1) / steps)

    data_fft_tot = data_fft_tot / (i + 1)
    frq = np.linspace(0, FrecLaser / 2, num=n / 2 + 1)

    fig2 = plt.figure(figsize=(16, 8))
    ax2 = fig2.add_axes([.15, .1, .8, .62])
    im = ax2.imshow(data_fft_tot, cmap=plt.get_cmap('jet'), aspect='auto', interpolation='none')
    fig2.colorbar(im)
    im.set_clim([c_axis_min_fft, c_axis_max_fft])
    ticks = ax2.get_xticks()
    ax2.text(1.02, 1.35, titulo_str_fft, horizontalalignment='left', transform=ax2.transAxes, color='k')
    tiempo_label = ax2.text(1.02, 1.1, 'T:' + tiempo_ini, horizontalalignment='left', transform=ax2.transAxes, color='k')
    ax2.set_xticklabels(np.round(ticks * delta_x + vec_cols[0] * delta_x + float(offset_m)))
    ax2.set_ylim(0, data_fft_tot.shape[0])
    ticks = ax2.get_yticks()
    frq_t = []
    for i in range(len(ticks) - 1):
        tt = '%3.2f' % (frq[int(ticks[i])])
        frq_t.append(tt)

    ax2.set_yticklabels(frq_t)
    ax2.set_xlabel(u'Posición [m]')
    ax2.set_ylabel('Frecuencia [Hz]')

    fft_mean = np.mean(data_fft_tot[1::, :], axis=0)
    ax3 = fig2.add_axes([.15, .76, .64, .15])
    ax3.plot(fft_mean, '-b')
    ax3.set_xlim([0, fft_mean.shape[0] - 1])
    ax3.axes.xaxis.set_ticklabels([])
    ax3.set_ylim([c_axis_min_fft, c_axis_max_fft])

    # Posicion de los bines  fft
    bines = np.linspace(0, data_fft_tot.shape[1], num=data_fft_tot.shape[1])
    pos_bin_fft = bines * delta_x + vec_cols[0] * delta_x + float(offset_m)

    # Guarda figura
    inttostr = '%05d' % (num_figura)
    if guarda_figuras == 'si':
        figname = os.path.join(direfig, 'figura' + inttostr + '_fft.png')
        fig2.savefig(figname, dpi=300)

    return std, data_fft_tot, pos_bin_std, tiempo_filas_std, frq, pos_bin_fft,


def carga_matriz_std(parametros):
    '''
    Esta función carga la matriz STD (filas=tiempo, col=bines) de los archivos procesados .std del equipo de medición DAS.
    Aparte genera un grafico de los datos que guarda en un directorio nuevo llamado 'Figuras'.

    Parameters
    ----------
    time_str: carpeta donde se guarda la adquisición en formato: yy_dd_mm_HH_MM_SS
    c: velocidad de la luz en el vacio
    n: índice de refracción en la fibra
    c_f: velocidad de la luz efectiva (en la fibra)
    offset_m: offset en metros utilizado para la puesta en profundidad/distancia. Utilizado de manera que el cero coincida con la boca de pozo.
    FrecLaser: frecuencia del láser en Hz.
    zoom_i_m: posición en metros de inicio del video
    zoom_f_m: posición en metros del final del video
    tiempo_ini: inicio de la carga en formato 'yyyy-mm-dd HH:MM:SS'
    tiempo_fin: fin de la carga en formato 'yyyy-mm-dd HH:MM:SS'


    Output
    ------
    matriz: matriz STD. El número de columnas es el de toda la STD. El número de filas, el correspondiente entre los tiempo_ini y tiempo_fin
    tiempo_filas_std: lista con los tiempos correspondientes a cada fila. El tamaño de la lista es igual al número de filas de la matriz.
    pos_bin: numpy array con la posición en metros correspondiente a cada bin. El tamaño del vector es igual al número de columnas de la matriz.


    Example
    -------
    from funciones_das import carga_matriz_std
    from funciones4 import header_read
    from funciones4 import data_read
    import numpy as np


    parametros = {}
    parametros['time_str'] = '17_30_11_10_59_49'
    nombre_header = os.path.join(parametros['time_str'], 'STD', 'std.hdr')
    nombre_archivo = os.path.join(parametros['time_str'], 'STD', '000000.std')
    header = header_read(nombre_header,nombre_archivo)
    parametros['c'] = 299792458.
    parametros['n'] = 1.46879964
    parametros['offset_m'] = 0
    parametros['FrecLaser'] = 2000
    parametros['c_f'] = parametros['c']/parametros['n']
    parametros['zoom_i_m'] = 5300
    parametros['zoom_f_m'] = 5600
    parametros['tiempo_ini'] = '2017-11-30 11:12:30'
    parametros['tiempo_fin'] = '2017-11-30 11:13:00'


    matriz, tiempo_filas_std, pos_bin,  = carga_matriz_std(parametros)

    '''

    time_str = parametros['time_str']
    FrecLaser = parametros['FrecLaser']
    tiempo_ini = parametros['tiempo_ini']
    tiempo_fin = parametros['tiempo_fin']

    # Cargo parametros para graficar
    zoom_i_m = parametros['zoom_i_m']
    zoom_f_m = parametros['zoom_f_m']
    c = parametros['c']
    n = parametros['n']
    c_f = parametros['c_f']
    offset_m = parametros['offset_m']

    ano = time_str[0:2]
    ano = '20' + ano

    dia = time_str[3:5]
    mes = time_str[6:8]

    hora = time_str[9:11]
    minuto = time_str[12:14]
    seg = time_str[15:17]

    tiempo_0 = ano + '-' + mes + '-' + dia + ' ' + hora + ':' + minuto + ':' + seg
    tiempo_0_date = datetime.datetime.strptime(tiempo_0, '%Y-%m-%d %H:%M:%S')

    tiempo_ini_date = datetime.datetime.strptime(tiempo_ini, '%Y-%m-%d %H:%M:%S')
    tiempo_fin_date = datetime.datetime.strptime(tiempo_fin, '%Y-%m-%d %H:%M:%S')

    dif_time_date_ini = tiempo_ini_date - tiempo_0_date
    dif_time_date_fin = tiempo_fin_date - tiempo_0_date
    dif_time_date_ini_sec = dif_time_date_ini.total_seconds()
    dif_time_date_fin_sec = dif_time_date_fin.total_seconds()

    dif_time = dif_time_date_fin - dif_time_date_ini
    dif_time_sec = dif_time.total_seconds()

    nombre_header = os.path.join(time_str, 'STD', 'std.hdr')
    nombre_archivo = os.path.join(time_str, 'STD', '000000.std')
    header = header_read(nombre_header, nombre_archivo)

    nShotsChk = header['nShotsChk']
    sec_per_fila = nShotsChk / FrecLaser
    filas = header['Fils']
    sec_per_file = filas * sec_per_fila

    ini_file = int(dif_time_date_ini_sec / sec_per_file)
    ini_fila = int(dif_time_date_ini_sec % sec_per_file / sec_per_fila)
    fin_file = int(dif_time_date_fin_sec / sec_per_file)
    fin_fila = int(dif_time_date_fin_sec % sec_per_file / sec_per_fila)

    filas_tot = int(dif_time_sec / sec_per_fila)

    delta_t = header['FreqRatio'] * 5e-9
    delta_x = c_f * delta_t / 2
    zoom_i = int((zoom_i_m - offset_m) / delta_x)
    zoom_f = int((zoom_f_m - offset_m) / delta_x)

    matriz = np.zeros([filas_tot, zoom_f - zoom_i + 1])
    vec_cols = np.array([zoom_i, zoom_f], dtype=np.uint64)
    ind_fila = 0

    j = 0
    print 'Cargando STD: '
    for i in range(ini_file, fin_file + 1):
        file_num = '%06d' % i
        # print file_num
        path = os.path.join(time_str, 'STD', file_num + '.std')
        header = header_read(nombre_header, path)

        if (ini_file == fin_file):
            vec_fils = np.array([ini_fila, fin_fila - 1])
        else:
            if (i == ini_file):
                vec_fils = np.array([ini_fila, header['Fils'] - 1])
            elif (i == fin_file):
                vec_fils = np.array([0, fin_fila - 1])
            else:
                vec_fils = np.array([0, header['Fils'] - 1])

        header, vector = data_read(nombre_header, path, vec_fils, vec_cols)

        fila = vector.shape[0]

        matriz[ind_fila:ind_fila + fila, :] = vector
        ind_fila = ind_fila + fila

        j = j + 1
        if (j / 10. == j / 10):
            print '%2.2f' % (float(j) / float(fin_file - ini_file) * 100.), ' %'

    # Posicion de los bines
    bines = np.linspace(zoom_i, zoom_f, num=zoom_f - zoom_i + 1)
    pos_bin = bines * delta_x + float(offset_m)

    # Filas tiempo
    tiempo_filas_std = []
    tiempo_inii = datetime.datetime.strptime(tiempo_ini, '%Y-%m-%d %H:%M:%S')
    for i in range(filas_tot):
        tt = tiempo_inii + datetime.timedelta(seconds=i * header['nShotsChk'] / FrecLaser)
        tiempo_filas_std.append(tt)

    return matriz, tiempo_filas_std, pos_bin,
