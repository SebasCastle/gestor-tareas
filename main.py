"""Punto de entrada de la aplicación de gestión de tareas."""

from gestor_tareas.configuracion import Configuracion


def main() -> None:
    """Inicia la aplicación usando la configuración global."""
    config = Configuracion.obtener()
    print(f"=== {config.nombre_app} ===")
    config.registrar(f"Archivo de datos: {config.archivo_datos}")
    if config.modo_debug:
        print("Modo debug activo.")


if __name__ == "__main__":
    main()
