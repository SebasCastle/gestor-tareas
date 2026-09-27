"""Punto de entrada de la aplicación de gestión de tareas."""

from __future__ import annotations

import sys

from gestor_tareas.configuracion import Configuracion
from gestor_tareas.gestor import GestorTareas
from gestor_tareas.tarea import Tarea


def main() -> None:
    """Carga las tareas guardadas, muestra el menú y guarda al salir."""
    config = Configuracion.obtener()
    _configurar_salida()
    try:
        gestor = GestorTareas()
    except ValueError as error:
        print(error)
        return
    print(f"=== {config.nombre_app} ===")
    config.registrar(f"Archivo de datos: {config.archivo_datos}")
    try:
        _menu(gestor)
    except KeyboardInterrupt:
        print("\nSaliendo.")
    finally:
        gestor.guardar()
        print("Cambios guardados.")


def _menu(gestor: GestorTareas) -> None:
    opciones = {
        "1": lambda: _agregar(gestor),
        "2": lambda: _listar(gestor),
        "3": lambda: _completar(gestor),
    }
    while True:
        print()
        print("1. Agregar tarea")
        print("2. Listar tareas")
        print("3. Marcar tarea como completada")
        print("4. Salir")
        opcion = _leer("Elige una opción: ")
        if opcion is None or opcion == "4":
            if opcion == "4":
                print("Hasta luego.")
            return
        accion = opciones.get(opcion)
        if accion is None:
            print("Opción no válida.")
            continue
        accion()


def _agregar(gestor: GestorTareas) -> None:
    titulo = _leer("Título de la tarea: ")
    if titulo is None:
        return
    try:
        tarea = gestor.agregar_tarea(titulo)
    except ValueError as error:
        print(error)
        return
    print(f"Tarea {tarea.id} agregada.")


def _listar(gestor: GestorTareas) -> None:
    tareas = gestor.listar_tareas()
    if not tareas:
        print("No hay tareas registradas.")
        return
    print(f"{'ID':<6}{'Estado':<14}Título")
    for tarea in tareas:
        print(f"{tarea.id:<6}{_marca(tarea):<14}{tarea.titulo}")


def _completar(gestor: GestorTareas) -> None:
    if not gestor.listar_tareas():
        print("No hay tareas para completar.")
        return
    entrada = _leer("ID de la tarea: ")
    if entrada is None:
        return
    if not entrada.isdigit():
        print("El ID debe ser un número entero.")
        return
    try:
        tarea = gestor.completar_tarea(int(entrada))
    except ValueError as error:
        print(error)
        return
    print(f"Tarea {tarea.id} marcada como completada.")


def _leer(mensaje: str) -> str | None:
    """Lee una línea. Si la entrada no es una terminal, la repite en pantalla."""
    try:
        valor = input(mensaje)
    except EOFError:
        print()
        return None
    if not sys.stdin.isatty():
        print(valor)
    return valor.strip()


def _marca(tarea: Tarea) -> str:
    return "[x]" if tarea.completada else "[ ]"


def _configurar_salida() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is None:
            continue
        try:
            reconfigure(encoding="utf-8")
        except (OSError, ValueError):
            return


if __name__ == "__main__":
    main()
