"""Modelo de una tarea."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Tarea:
    """Tarea identificada por un id numérico."""

    id: int
    titulo: str
    completada: bool = False

    @property
    def estado(self) -> str:
        """Etiqueta legible del estado de la tarea."""
        return "completada" if self.completada else "pendiente"
