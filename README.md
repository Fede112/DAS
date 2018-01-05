# DAS
Programa de adquisición DAS (falta subirlo) y scripts para el procesamiento de los datos, tanto STD como crudo.

## Table of contents
* [Scripts para el procesamiento de los datos](#scripts)
* [Buenas Prácticas para contribuir al GIT](#buenaspracticas)


## Scripts para el procesamiento de los datos <a name="scripts"></a>

Los Scripts para el procesamiento de los datos generados por el sensor DAS son tres:
1. funciones4.py
2. funciones_das.py
3. corre_funciones_das.py

Para generar las figuras/pelicula se necesita copiar los tres archivos donde están todas las carpetas con los datos, nombradas según el día en el que se inició la adquisición (Ej. '17_22_11_12_04_36').

Los scripts se corren individualmente desde corre_funciones_das.py.

### funciones4.py

Contiene las funciones básicas para levantar los datos generados por el DAS. Las columnas son los bines y las filas son los datos en función del tiempo para cada bin.

### funciones_das.py

Son las funciones que procesan los datos. Hasta el momento son:
- procesa_std_fft: genera la fft y la std a partir del dato crudo.
- carga_std: genera la figura a partir de los datos std.
- peli_std: genera una pelicula a partir de los datos std.

### corre_funciones_das.py

Son los scripts que hay que correr individualmente para generar tanto la pelicula de los datos STD, las figuras STD y el procesamiento del dato crudo.




## Buenas Prácticas para contribuir al GIT  <a name="buenaspracticas"></a>

### Como realizar los commits
[Guia Commits](https://codigofacilito.com/articulos/buenas-practicas-en-commits-de-git)
(lo robe de la primer pagina que encontre, no sé si es la mejor manera)

#### Tags de los commits:

- feat: Una nueva caracteristica.

- fix: Se soluciono un bug.

- docs: Se realizaron cambios en la documentacion.

- style: Se aplico formato, comas y puntos faltantes, etc; Sin cambios en el codigo.

- refactor: Refactorizacion del codigo en produccion.

- test: Se añadieron pruebas, refactorizacion de pruebas; Sin cambios en el codigo.

- chore: Actualizacion de tareas de build, configuracion del admin. de paquetes; Sin cambios en el codigo.


### Ejemplo de como comentar funciones
```python
def sqrt(x):
    """
    Compute the square root of x.

    For negative input elements, a complex value is returned
    (unlike `numpy.sqrt` which returns NaN).

    Parameters
    ----------
    x : array_like
       The input value(s).

    Returns
    -------
    out : ndarray or scalar
       The square root of `x`. If `x` was a scalar, so is `out`,
       otherwise an array is returned.

    See Also
    --------
    numpy.sqrt

    Examples
    --------
    For real, non-negative inputs this works just like `numpy.sqrt`:

    >>> np.lib.scimath.sqrt(1)
    1.0
    >>> np.lib.scimath.sqrt([1, 4])
    array([ 1.,  2.])

    But it automatically handles negative inputs:

    >>> np.lib.scimath.sqrt(-1)
    (0.0+1.0j)
    >>> np.lib.scimath.sqrt([-1,4])
    array([ 0.+1.j,  2.+0.j])

    """
    x = _fix_real_lt_zero(x)
    return nx.sqrt(x)
```

