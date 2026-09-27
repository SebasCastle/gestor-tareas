"""Configuración global de la aplicación mediante el patrón Singleton."""

from __future__ import annotations

import os
from pathlib import Path


class Configuracion:
    """Gestiona la configuración global con una única instancia.

    El modo debug y la ruta del archivo de tareas se comparten en toda
    la aplicación. La variable de entorno GESTOR_DEBUG activa el modo
    debug cuando vale 1, true, si, yes u on.
    """

    _instancia: Configuracion | None = None

    def __new__(cls) -> Configuracion:
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia

    def __init__(self) -> None:
        if getattr(self, "_inicializada", False):
            return
        raiz = Path(__file__).resolve().parent.parent
        self.nombre_app = "Gestor de Tareas"
        self.modo_debug = _leer_modo_debug()
        self.archivo_datos = raiz / "data" / "tareas.json"
        self._inicializada = True

    @classmethod
    def obtener(cls) -> Configuracion:
        """Devuelve la instancia única de configuración."""
        return cls()

    @classmethod
    def reiniciar(cls) -> None:
        """Descarta la instancia actual. Pensado para pruebas unitarias."""
        cls._instancia = None

    def registrar(self, mensaje: str) -> None:
        """Imprime un mensaje solo cuando el modo debug está activo."""
        if self.modo_debug:
            print(f"[DEBUG] {mensaje}")


def _leer_modo_debug() -> bool:
    valor = os.environ.get("GESTOR_DEBUG", "").strip().lower()
    return valor in {"1", "true", "si", "sí", "yes", "on"}
