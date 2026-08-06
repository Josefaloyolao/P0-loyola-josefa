# Proyecto 0 — Benchmarking con Python y OpenCode

## Descripción

Proyecto 0 del curso: prepara el ambiente de trabajo, investiga las
características del computador e implementa una multiplicación de matrices
con ciclos explícitos de Python (`mimatmul`) para compararla con la
operación optimizada de NumPy mediante un benchmark.

## Instalación

Requisitos: Python 3.14, Git y una cuenta de GitHub.

Crear el ambiente virtual:

```
python -m venv venv
```

Activarlo:

```
venv\Scripts\activate
```

Instalar las dependencias:

```
pip install -r requirements.txt
```

## Ejecución

Ejecutar las pruebas:

```
python -m pytest
```

Obtener información del computador:

```
python src/system_info.py
```

Ejecutar el benchmark:

```
python src/benchmark.py
```

## Computador

Las características se obtienen con `src/system_info.py` y se guardan en
`data/system_info.json`.

| Característica | Valor |
|---|---|
| Sistema operativo | Windows 11 (10.0.26200) |
| Arquitectura | AMD64 |
| Python | 3.14.3 |
| NumPy | 2.5.1 |
| Procesador | 12th Gen Intel Core i5-1235U |
| Núcleos físicos | 10 |
| Procesadores lógicos | 12 |
| RAM total | ~8.3 GB |
| GPU | Intel UHD Graphics |

## Resultados

*Pendientes para P0E2:* benchmark definitivo, `data/benchmark_results.csv`
y `figures/benchmark.png`.

## Uso de OpenCode

*Reflexión personal pendiente para la entrega final.*

## Estado actual

**P0E1 en desarrollo.** El ambiente funciona, se obtuvo la información del
computador y se implementó una primera versión de `mimatmul` con sus
pruebas iniciales.
