# AGENTS.md — Instrucciones para OpenCode

## Propósito del proyecto

Proyecto 0 del curso: introducción al benchmarking y al trabajo con agentes
de IA. Incluye información del computador, una multiplicación de matrices
con ciclos explícitos de Python, pruebas automáticas y un benchmark que
compara `mimatmul` con la operación optimizada `A @ B` de NumPy.

## Estructura del repositorio

```
P0-loyola-josefa/
├── README.md
├── AGENTS.md
├── requirements.txt
├── conftest.py
├── src/
│   ├── system_info.py
│   ├── mimatmul.py
│   └── benchmark.py
├── tests/
│   └── test_mimatmul.py
├── data/
│   ├── system_info.json
│   └── benchmark_results.csv
└── figures/
    └── benchmark.png
```

## Comandos

- Activar ambiente virtual: `venv\Scripts\activate` (Windows)
- Ejecutar las pruebas: `python -m pytest`
- Información del computador: `python src/system_info.py`
- Benchmark: `python src/benchmark.py`

## Reglas permanentes

- Mantener el código sencillo y claro; es un proyecto pedagógico.
- No inventar mediciones: los datos deben venir de ejecuciones reales.
- Conservar los datos originales; no editar manualmente los tiempos.
- Ejecutar `python -m pytest` después de modificar el código.
- No crear matrices tan grandes que agoten la memoria del computador.
- No ejecutar operaciones destructivas de Git (force push, rebase, reset
  --hard, borrado de historia).
- No subir credenciales, contraseñas ni claves de API.
- El estudiante debe revisar todos los cambios antes de commit o push.
