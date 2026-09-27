"""Operaciones para agregar, listar y completar tareas."""

from __future__ import annotations

from gestor_tareas.configuracion import Configuracion
from gestor_tareas.tarea import Tarea


class GestorTareas:
    """Administra la colección de tareas de la aplicación."""

    def __init__(self) -> None:
        self.config = Configuracion.obtener()
        self._tareas: list[Tarea] = []
        self._siguiente_id = 1

    def agregar_tarea(self, titulo: str) -> Tarea:
        """Crea una tarea pendiente y la agrega a la colección."""
        titulo_limpio = titulo.strip()
        if not titulo_limpio:
            raise ValueError("El título de la tarea no puede estar vacío.")
        tarea = Tarea(id=self._siguiente_id, titulo=titulo_limpio)
        self._siguiente_id += 1
        self._tareas.append(tarea)
        self.config.registrar(f"Tarea agregada: {tarea.id} - {tarea.titulo}")
        return tarea

    def listar_tareas(self) -> list[Tarea]:
        """Devuelve una copia de las tareas registradas."""
        return list(self._tareas)

    def completar_tarea(self, tarea_id: int) -> Tarea:
        """Marca como completada la tarea con el id indicado."""
        tarea = self._buscar(tarea_id)
        if tarea.completada:
            raise ValueError(f"La tarea {tarea_id} ya está completada.")
        tarea.completada = True
        self.config.registrar(f"Tarea completada: {tarea.id} - {tarea.titulo}")
        return tarea

    def _buscar(self, tarea_id: int) -> Tarea:
        for tarea in self._tareas:
            if tarea.id == tarea_id:
                return tarea
        raise ValueError(f"No existe una tarea con id {tarea_id}.")
