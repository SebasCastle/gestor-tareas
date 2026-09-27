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

    def a_dict(self) -> dict[str, int | str | bool]:
        """Serializa la tarea para guardarla en JSON."""
        return {
            "id": self.id,
            "titulo": self.titulo,
            "completada": self.completada,
        }

    @classmethod
    def desde_dict(cls, datos: dict) -> Tarea:
        """Reconstruye una tarea a partir de un objeto JSON."""
        try:
            completada = datos.get("completada", False)
            if not isinstance(completada, bool):
                raise TypeError
            return cls(
                id=int(datos["id"]),
                titulo=str(datos["titulo"]).strip(),
                completada=completada,
            )
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError("El archivo de tareas tiene un formato inválido.") from error
