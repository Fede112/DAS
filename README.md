# DAS
Programa de adquisición DAS y scripts para el procesamiento de los datos, tanto STD como crudo.

## Buenas Practicas en los Commits
[Guia Commits](https://codigofacilito.com/articulos/buenas-practicas-en-commits-de-git)
(lo robe de la primer pagina que encontre, no sé si es la mejor manera)

## Tags de los commits:

- feat: Una nueva caracteristica.

- fix: Se soluciono un bug.

- docs: Se realizaron cambios en la documentacion.

- style: Se aplico formato, comas y puntos faltantes, etc; Sin cambios en el codigo.

- refactor: Refactorizacion del codigo en produccion.

- test: Se añadieron pruebas, refactorizacion de pruebas; Sin cambios en el codigo.

- chore: Actualizacion de tareas de build, configuracion del admin. de paquetes; Sin cambios en el codigo.


## Ejemplo de como comentar funciones
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

