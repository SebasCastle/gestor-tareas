"""Pruebas unitarias de agregar, listar, completar y persistir tareas."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from gestor_tareas.configuracion import Configuracion
from gestor_tareas.gestor import GestorTareas


class TestGestorTareas(unittest.TestCase):
    """Verifica las operaciones principales del gestor."""

    def setUp(self) -> None:
        Configuracion.reiniciar()
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        config = Configuracion.obtener()
        config.archivo_datos = Path(self._tmp.name) / "tareas.json"
        self.gestor = GestorTareas()

    def test_agregar_tarea(self) -> None:
        tarea = self.gestor.agregar_tarea("Estudiar patrones de diseño")

        self.assertEqual(tarea.id, 1)
        self.assertEqual(tarea.titulo, "Estudiar patrones de diseño")
        self.assertFalse(tarea.completada)
        self.assertEqual(tarea.estado, "pendiente")
        listadas = self.gestor.listar_tareas()
        self.assertEqual(len(listadas), 1)
        self.assertEqual(listadas[0].titulo, "Estudiar patrones de diseño")

    def test_agregar_varias_tareas_asigna_ids_consecutivos(self) -> None:
        primera = self.gestor.agregar_tarea("Primera")
        segunda = self.gestor.agregar_tarea("  Segunda  ")

        self.assertEqual(primera.id, 1)
        self.assertEqual(segunda.id, 2)
        self.assertEqual(segunda.titulo, "Segunda")
        self.assertEqual(len(self.gestor.listar_tareas()), 2)

    def test_agregar_tarea_vacia_lanza_error(self) -> None:
        with self.assertRaises(ValueError):
            self.gestor.agregar_tarea("   ")
        self.assertEqual(self.gestor.listar_tareas(), [])

    def test_completar_tarea(self) -> None:
        tarea = self.gestor.agregar_tarea("Hacer commit")

        completada = self.gestor.completar_tarea(tarea.id)

        self.assertTrue(completada.completada)
        self.assertEqual(completada.estado, "completada")
        self.assertTrue(self.gestor.listar_tareas()[0].completada)

    def test_completar_tarea_inexistente(self) -> None:
        self.gestor.agregar_tarea("Solo una")
        with self.assertRaises(ValueError):
            self.gestor.completar_tarea(99)
        self.assertFalse(self.gestor.listar_tareas()[0].completada)

    def test_completar_tarea_ya_completada(self) -> None:
        tarea = self.gestor.agregar_tarea("Repetir")
        self.gestor.completar_tarea(tarea.id)
        with self.assertRaises(ValueError):
            self.gestor.completar_tarea(tarea.id)

    def test_listar_no_expone_la_lista_interna(self) -> None:
        self.gestor.agregar_tarea("Aislar")
        copia = self.gestor.listar_tareas()
        copia.clear()
        self.assertEqual(len(self.gestor.listar_tareas()), 1)

    def test_guardar_y_cargar_conserva_tareas(self) -> None:
        self.gestor.agregar_tarea("Persistir")
        completada = self.gestor.agregar_tarea("Cerrar sesión")
        self.gestor.completar_tarea(completada.id)
        self.gestor.guardar()

        Configuracion.reiniciar()
        config = Configuracion.obtener()
        config.archivo_datos = Path(self._tmp.name) / "tareas.json"
        restaurado = GestorTareas()

        tareas = restaurado.listar_tareas()
        self.assertEqual(
            [tarea.titulo for tarea in tareas],
            ["Persistir", "Cerrar sesión"],
        )
        self.assertFalse(tareas[0].completada)
        self.assertTrue(tareas[1].completada)
        nueva = restaurado.agregar_tarea("Continuar")
        self.assertEqual(nueva.id, 3)

    def test_cargar_archivo_inexistente_inicia_vacio(self) -> None:
        self.assertEqual(self.gestor.listar_tareas(), [])

    def test_cargar_archivo_danado_lanza_error(self) -> None:
        ruta = Path(self._tmp.name) / "tareas.json"
        ruta.write_text("{ esto no es json", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.gestor.cargar()


class TestConfiguracionSingleton(unittest.TestCase):
    """Verifica que la configuración global sea una única instancia."""

    def setUp(self) -> None:
        Configuracion.reiniciar()

    def test_devuelve_la_misma_instancia(self) -> None:
        primera = Configuracion.obtener()
        segunda = Configuracion()
        self.assertIs(primera, segunda)

    def test_reiniciar_crea_una_instancia_nueva(self) -> None:
        primera = Configuracion.obtener()
        Configuracion.reiniciar()
        segunda = Configuracion.obtener()
        self.assertIsNot(primera, segunda)

    def test_el_modo_debug_se_comparte(self) -> None:
        primera = Configuracion.obtener()
        primera.modo_debug = True
        segunda = Configuracion.obtener()
        self.assertTrue(segunda.modo_debug)


if __name__ == "__main__":
    unittest.main()
