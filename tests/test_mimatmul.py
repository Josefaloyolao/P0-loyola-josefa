"""Pruebas automáticas para la función mimatmul."""

import numpy as np
import pytest

from mimatmul import mimatmul


def test_caso_conocido():
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    esperado = [[19, 22], [43, 50]]
    assert mimatmul(A, B) == esperado


def test_matriz_identidad():
    A = [[1, 2, 3], [4, 5, 6]]
    I = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    assert mimatmul(A, I) == A


def test_matrices_cuadradas():
    A = [[2, 0], [0, 2]]
    B = [[1, 2], [3, 4]]
    assert mimatmul(A, B) == [[2, 4], [6, 8]]


def test_matrices_rectangulares():
    A = [[1, 2, 3], [4, 5, 6]]  # (2, 3)
    B = [[7, 8], [9, 10], [11, 12]]  # (3, 2)
    esperado = [[58, 64], [139, 154]]
    assert mimatmul(A, B) == esperado


def test_comparacion_con_numpy():
    rng = np.random.default_rng(42)
    A = rng.integers(0, 10, size=(4, 5)).tolist()
    B = rng.integers(0, 10, size=(5, 3)).tolist()
    resultado = np.asarray(mimatmul(A, B), dtype=float)
    esperado = np.asarray(A) @ np.asarray(B)
    np.testing.assert_allclose(resultado, esperado)


def test_dimensiones_incompatibles():
    A = [[1, 2, 3], [4, 5, 6]]  # 3 columnas
    B = [[1, 2], [3, 4]]  # 2 filas
    with pytest.raises(ValueError):
        mimatmul(A, B)
