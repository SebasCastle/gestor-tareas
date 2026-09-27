"""Pruebas unitarias de agregar, listar y completar tareas."""

from __future__ import annotations

import unittest

from gestor_tareas.configuracion import Configuracion
from gestor_tareas.gestor import GestorTareas


class TestGestorTareas(unittest.TestCase):
    """Verifica las operaciones principales del gestor."""

    def setUp(self) -> None:
        Configuracion.reiniciar()
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


if __name__ == "__main__":
    unittest.main()
