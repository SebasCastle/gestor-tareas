"""Operaciones para agregar, listar, completar y persistir tareas."""

from __future__ import annotations

import json
from pathlib import Path

from gestor_tareas.configuracion import Configuracion
from gestor_tareas.tarea import Tarea


class GestorTareas:
    """Administra la colección de tareas de la aplicación."""

    def __init__(self, autocargar: bool = True) -> None:
        self.config = Configuracion.obtener()
        self._tareas: list[Tarea] = []
        self._siguiente_id = 1
        if autocargar:
            self.cargar()

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

    def cargar(self) -> None:
        """Carga las tareas desde el archivo JSON configurado."""
        ruta = Path(self.config.archivo_datos)
        if not ruta.exists():
            self._tareas = []
            self._siguiente_id = 1
            self.config.registrar("No hay archivo de tareas; se inicia vacío.")
            return
        try:
            with ruta.open(encoding="utf-8") as archivo:
                datos = json.load(archivo)
        except json.JSONDecodeError as error:
            raise ValueError(f"El archivo de tareas está dañado: {ruta}") from error
        if not isinstance(datos, dict) or not isinstance(datos.get("tareas"), list):
            raise ValueError(f"El archivo de tareas tiene un formato inválido: {ruta}")
        self._tareas = [Tarea.desde_dict(item) for item in datos["tareas"]]
        siguiente = datos.get("siguiente_id")
        if isinstance(siguiente, int) and not isinstance(siguiente, bool) and siguiente > 0:
            self._siguiente_id = max(siguiente, self._maximo_id() + 1)
        else:
            self._siguiente_id = self._maximo_id() + 1
        self.config.registrar(f"Tareas cargadas: {len(self._tareas)}")

    def guardar(self) -> None:
        """Guarda las tareas en el archivo JSON configurado."""
        ruta = Path(self.config.archivo_datos)
        ruta.parent.mkdir(parents=True, exist_ok=True)
        contenido = {
            "siguiente_id": self._siguiente_id,
            "tareas": [tarea.a_dict() for tarea in self._tareas],
        }
        with ruta.open("w", encoding="utf-8") as archivo:
            json.dump(contenido, archivo, ensure_ascii=False, indent=2)
            archivo.write("\n")
        self.config.registrar(f"Tareas guardadas en {ruta}")

    def _buscar(self, tarea_id: int) -> Tarea:
        for tarea in self._tareas:
            if tarea.id == tarea_id:
                return tarea
        raise ValueError(f"No existe una tarea con id {tarea_id}.")

    def _maximo_id(self) -> int:
        if not self._tareas:
            return 0
        return max(tarea.id for tarea in self._tareas)
