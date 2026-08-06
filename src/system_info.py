"""Investiga las características principales del computador y las guarda en
data/system_info.json.

Los datos se obtienen con la biblioteca estándar de Python y con comandos
del sistema operativo. Si algún dato no puede obtenerse, se registra como
"No disponible".
"""

import ctypes
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np


def _run_command(args):
    """Ejecuta un comando y devuelve su salida, o None si falla."""
    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=10,
            encoding="utf-8",
            errors="replace",
        )
        return result.stdout.strip()
    except (subprocess.SubprocessError, FileNotFoundError, OSError):
        return None


def _wmic_value(args):
    """Devuelve el primer valor no vacío de una consulta wmic, o None."""
    out = _run_command(args)
    if not out:
        return None
    for line in out.splitlines():
        line = line.strip()
        if line and not line.lower().startswith(args[-1].lower()):
            return line
    return None


def get_cpu_model():
    name = _wmic_value(["wmic", "cpu", "get", "name"])
    return name or platform.processor() or None


def get_gpu_model():
    out = _run_command(["wmic", "path", "win32_VideoController", "get", "name"])
    if not out:
        return None
    names = [line.strip() for line in out.splitlines() if line.strip()]
    if len(names) > 1:
        return " ; ".join(names[1:])
    return None


def get_ram_info():
    class MEMORYSTATUSEX(ctypes.Structure):
        _fields_ = [
            ("dwLength", ctypes.c_ulong),
            ("dwMemoryLoad", ctypes.c_ulong),
            ("ullTotalPhys", ctypes.c_ulonglong),
            ("ullAvailPhys", ctypes.c_ulonglong),
            ("ullTotalPageFile", ctypes.c_ulonglong),
            ("ullAvailPageFile", ctypes.c_ulonglong),
            ("ullTotalVirtual", ctypes.c_ulonglong),
            ("ullAvailVirtual", ctypes.c_ulonglong),
            ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
        ]

    status = MEMORYSTATUSEX()
    status.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
    ok = ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status))
    if not ok:
        return None, None
    total_bytes = status.ullTotalPhys
    avail_bytes = status.ullAvailPhys
    return total_bytes, avail_bytes


def main():
    total_ram, avail_ram = get_ram_info()
    disk = shutil.disk_usage(os.path.abspath("."))

    info = {
        "sistema_operativo": f"{platform.system()} {platform.release()} "
        f"({platform.version()})",
        "arquitectura": platform.machine(),
        "version_python": platform.python_version(),
        "version_numpy": np.__version__,
        "modelo_procesador": get_cpu_model() or "No disponible",
        "nucleos_fisicos": (
            _wmic_value(["wmic", "cpu", "get", "NumberOfCores"]) or os.cpu_count()
        ),
        "procesadores_logicos": (
            _wmic_value(["wmic", "cpu", "get", "NumberOfLogicalProcessors"])
            or os.cpu_count()
        ),
        "ram_total_bytes": total_ram if total_ram else "No disponible",
        "ram_disponible_bytes": avail_ram if avail_ram else "No disponible",
        "gpu": get_gpu_model() or "No disponible",
        "disco_total_bytes": disk.total,
        "disco_libre_bytes": disk.free,
    }

    out_dir = Path(__file__).resolve().parent.parent / "data"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "system_info.json"

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=4)

    print(json.dumps(info, ensure_ascii=False, indent=4))
    print(f"\nGuardado en: {out_path}")


if __name__ == "__main__":
    main()
