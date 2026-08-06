"""Multiplicación de matrices con ciclos explícitos de Python.

La función mimatmul(A, B) implementa el producto matricial usando tres
ciclos anidados, sin utilizar operaciones optimizadas de NumPy
(A @ B, np.matmul, np.dot o np.einsum). Es una versión pedagógica y
lenta; su propósito es compararse con la operación optimizada de NumPy.
"""


def mimatmul(A, B):
    """Multiplica dos matrices A y B usando ciclos explícitos de Python.

    Parámetros
    ----------
    A, B : listas de listas de números (o matrices convertibles a ellas)
        A debe tener forma (n, k) y B forma (k, m).

    Retorna
    -------
    C : lista de listas
        Producto matricial C = A * B, con forma (n, m).

    Levanta
    -------
    ValueError
        Si las dimensiones no son compatibles para multiplicar.
    """
    filas_a = len(A)
    columnas_b = len(B[0]) if len(B) > 0 else 0
    filas_b = len(B)

    if filas_a == 0 or filas_b == 0 or columnas_b == 0:
        raise ValueError(
            "Las matrices no pueden estar vacías para multiplicarlas."
        )

    if len(A[0]) != filas_b:
        raise ValueError(
            f"Dimensiones incompatibles: A tiene {len(A[0])} columnas "
            f"pero B tiene {filas_b} filas."
        )

    C = [[0] * columnas_b for _ in range(filas_a)]

    for i in range(filas_a):
        for j in range(columnas_b):
            suma = 0
            for k in range(filas_b):
                suma += A[i][k] * B[k][j]
            C[i][j] = suma

    return C
