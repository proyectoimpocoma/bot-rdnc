# Python Base Project

Este proyecto fue generado usando `personal-cli`. Es una plantilla base minimalista configurada con las mejores prácticas de la industria, ideal para scripts, librerías, o proyectos customizados que no requieren de un framework web pesado.

## 🚀 Inicio Rápido

### Requisitos Previos
* [Python 3.12+](https://www.python.org/)
* [uv](https://github.com/astral-sh/uv)

### Desarrollo Local

1. Instalar las dependencias y sincronizar entorno:
   ```bash
   uv sync
   ```

2. Ejecutar la aplicación principal:
   ```bash
   uv run python app/main.py
   ```

3. Instalar hooks de validación en Git para código limpio antes de cada commit:
   ```bash
   pre-commit install
   ```

4. Comandos útiles de validación:
   ```bash
   uv run ruff check --fix .
   uv run ruff format .
   uv run mypy .
   ```

## 📁 Estructura del Proyecto

La estructura promueve la escalabilidad modular:
* `app/core/`: Configuración central (ej. variables de entorno, logging, monitoreo).
* `tests/`: Entorno preparado para pruebas automatizadas (excluido de linters estrictos).
