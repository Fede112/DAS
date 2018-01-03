# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 22:23:45 2017

@author: Marco
"""
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

a = np.float32


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def header_read(nombre_header, nombre_archivo):
    fid = open(nombre_header, "r")

    line = []
    header_size = 0

    header = {}

    while (1):
        line = fid.readline()
        if (line == 'Fin header \n'):
            break

        header_size += len(line.encode('utf-8'))
        valor = find_between(line, "'", "'")
        pos = line.find(':')
        campo = line[0:pos:]

        if not valor:
            valor = find_between(line, "[", "]")
            valor = float(valor)

        header[campo] = valor
        # exec(campo + " = valor") #paso los campos a variables
    fid.close()

    header_size += len(line.encode('utf-8'))

    file_size = os.path.getsize(nombre_archivo)

    data_size = file_size
    Fils = data_size / header['BytesPerDatum'] / header['Cols'] / header['NDatum']

    header['Fils'] = Fils
    header['Header_size'] = header_size

    return header


def data_read(nombre_header, nombre_archivo, vec_fils=np.array([]), vec_cols=np.array([])):

    header = header_read(nombre_header, nombre_archivo)

    if vec_fils.size == 0:
        vec_fils = np.array([0, header['Fils'] - 1], dtype=np.uint64)

    if vec_cols.size == 0:
        vec_cols = np.array([0, header['Cols'] - 1], dtype=np.uint64)

    offset_fils = vec_fils[0]
    fils_to_read = vec_fils[1] - vec_fils[0] + 1

    cols_to_read = vec_cols[1] - vec_cols[0] + 1

    offset_cols = vec_cols[0]
    fils_to_read = np.uint64(fils_to_read)
    cols_to_read = np.uint64(cols_to_read)
    cols_to_read1 = np.uint64(cols_to_read * header['NDatum'])

    data = []
    data = np.zeros((fils_to_read, cols_to_read1), dtype=eval(header['PythonNpDataType']))

    # Abro el archivo y salteo los primeros shots
    fid = open(nombre_archivo, 'rb')
    #fid.seek(header['Header_size'], 0)
    fid.seek(np.uint64(header['BytesPerDatum'] * header['Cols'] * header['NDatum'] * offset_fils), 1)
    fid.seek(np.uint64(header['BytesPerDatum'] * header['NDatum'] * offset_cols), 1)
    skipi1 = np.uint64((header['Cols'] - cols_to_read) * header['BytesPerDatum'] * header['NDatum'])

    j = 0
    for i in range(fils_to_read):
        D1 = np.fromfile(fid, dtype=eval(header['PythonNpDataType']), count=cols_to_read1)
        fid.seek(skipi1, 1)
        data[j, :] = D1
        j = j + 1
    # print Fils, Cols, PythonNpDataType

#    fid = open(nombre_archivo,'rb')
#    fid.seek(header_size, 0)
#    exec("D1 = np.fromfile(fid, dtype="+PythonNpDataType+",count=int(Fils*Cols))")
    fid.close

    return header, data


#nombre_archivo = "17_19_07_08_51_48.std"
#header_campo, header_valor, D1 = data_read(nombre_archivo)
# for i in range(0,len(header_campo)):
#    valor = header_valor[i]
#    campo = header_campo[i]
#    exec(campo + " = valor")
