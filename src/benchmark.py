"""Benchmark que compara mimatmul con la multiplicación optimizada de NumPy.

Para cada tamaño de matriz cuadrada (float64) se mide el tiempo de
mimatmul (ciclos de Python) y de A @ B (NumPy), repitiendo cada medición
varias veces. Los resultados se guardan en data/benchmark_results.csv y el
gráfico en figures/benchmark.png.

Tamaños elegidos pensando en la RAM libre (~0.5 GB) y en que mimatmul es
O(n^3) con ciclos de Python: matrices mayores ralentizarían la ejecución
sin aportar información útil para este proyecto.
"""

import csv
import sys
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from mimatmul import mimatmul

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
FIGURES_DIR = ROOT / "figures"

TAMANOS = [50, 75, 100, 150, 200]
REPETICIONES = 3
SEED = 123


def generar_matrices(n, rng):
    """Genera dos matrices cuadradas float64 de tamaño n x n."""
    A = rng.random((n, n))
    B = rng.random((n, n))
    return A, B


def medir(fn, A, B):
    """Mide el tiempo de una sola multiplicación en segundos."""
    inicio = time.perf_counter()
    fn(A, B)
    fin = time.perf_counter()
    return fin - inicio


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(SEED)

    # Calentamiento: ejecuta cada método una vez para que los números se
    # carguen en caché y no afecten las primeras mediciones.
    A_warm, B_warm = generar_matrices(TAMANOS[0], rng)
    medir(mimatmul, A_warm.tolist(), B_warm.tolist())
    medir(lambda a, b: a @ b, A_warm, B_warm)

    filas = []
    for n in TAMANOS:
        A, B = generar_matrices(n, rng)
        A_lista = A.tolist()

        # Verifica que mimatmul coincida con NumPy antes de medir.
        resultado = np.asarray(mimatmul(A_lista, B.tolist()), dtype=float)
        np.testing.assert_allclose(resultado, A @ B)

        B_lista = B.tolist()
        for rep in range(1, REPETICIONES + 1):
            t_mimatmul = medir(mimatmul, A_lista, B_lista)
            filas.append(["mimatmul", n, rep, t_mimatmul])

            t_numpy = medir(lambda a, b: a @ b, A, B)
            filas.append(["numpy", n, rep, t_numpy])

            print(f"n={n} rep={rep}: mimatmul={t_mimatmul:.6f}s  numpy={t_numpy:.6f}s")

    csv_path = DATA_DIR / "benchmark_results.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["metodo", "tamano", "repeticion", "tiempo_segundos"])
        writer.writerows(filas)

    # Gráfico con escala logarítmica: la diferencia entre ambos métodos es
    # de varios órdenes de magnitud.
    fig, ax = plt.subplots(figsize=(8, 5))
    for metodo, color in [("mimatmul", "tab:red"), ("numpy", "tab:blue")]:
        datos = [row for row in filas if row[0] == metodo]
        x = [row[1] for row in datos]
        y = [row[3] for row in datos]
        ax.plot(x, y, marker="o", linestyle="-", label=metodo, color=color)

    ax.set_yscale("log")
    ax.set_xlabel("Tamaño de la matriz (n x n)")
    ax.set_ylabel("Tiempo de ejecución (segundos, escala log)")
    ax.set_title("Benchmark: mimatmul vs NumPy")
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)

    png_path = FIGURES_DIR / "benchmark.png"
    fig.tight_layout()
    fig.savefig(png_path, dpi=150)
    print(f"\nResultados guardados en: {csv_path}")
    print(f"Gráfico guardado en: {png_path}")


if __name__ == "__main__":
    main()
