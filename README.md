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

## **Descripción del Proyecto**

- **Nombre:** Bot Queries sictac
- **Objetivo:** Chatbot que recibe consultas en lenguaje natural (origen, destino, tipo de vehículo) y devuelve comparativas de costo entre Sictac y RNDC.
- **Entrada:** Mensaje de chat con origen, destino y configuración de vehículo.
- **Salida:** Respuesta formateada con costo en Sictac, precio RNDC y recomendación.
- **Estado actual:** Código base y módulos principales creados; muchas piezas del MVP implementadas (ver checklist).

Fuente principal de requerimientos: [Template Automation.txt](Template%20Automation.txt#L1).

## **Checklist de Fases (Paso a paso)**

Puedes marcar o desmarcar tareas usando la lista de tareas siguiente. También hay un script CLI `tools/checklist.py` para alternar tareas por su identificador (ver sección "Uso" abajo).

### Fase 0 — Preparación del repositorio

- [x] Inicializar entorno: `uv sync` y activar venv <!-- id:phase0_init_env -->
- [x] Entradas básicas y README: Documentación inicial <!-- id:phase0_docs -->
- [ ] Archivos clave: [main.py](main.py#L1), [pyproject.toml](pyproject.toml#L1) <!-- id:phase0_files -->

### Fase 1 — NLP (Procesamiento de lenguaje natural)

- [x] Definir entidades: ciudades, departamentos, tipo vehículo <!-- id:phase1_def_entities -->
  - Referencia: [nlp/extractor.py](nlp/extractor.py#L1), [nlp/normalizer.py](nlp/normalizer.py#L1)
- [ ] Entrenamiento / matcher de ciudades (spaCy o alternativa) <!-- id:phase1_training -->
- [ ] Pruebas unitarias de parsing (`test_example.py`) <!-- id:phase1_tests -->

### Fase 2 — Scraping / Automatización web

- [ ] Explorar HTML de Sictac/RNDC y diseñar selectores <!-- id:phase2_explore_selectors -->
- [ ] Implementar flows Playwright/Selenium (docker/playwright) <!-- id:phase2_implement_playwright -->
  - Referencia: `docker/playwright/docker-compose.yml`, `docker/playwright/scripts/`
- [ ] Extraer Costo Total del Viaje (Sictac) y Precio RNDC <!-- id:phase2_extract_costs -->

### Fase 3 — Mapeo y Procesamiento de datos

- [x] Cargar y limpiar datos (esqueleto) <!-- id:phase3_load_clean -->
  - Referencia: [data/loader.py](data/loader.py#L1), [data/processor.py](data/processor.py#L1)
- [ ] Calcular comparativos (promedios, diferencias) <!-- id:phase3_compute -->
- [ ] Persistencia / caché (SQLite / CSV / Polar) <!-- id:phase3_persistence -->

### Fase 4 — Servicios / Backend

- [x] Servicio de consulta para UI/Chatbot (base) <!-- id:phase4_service -->
- [ ] API / webhook para bot (Telegram / WhatsApp) <!-- id:phase4_webhook -->

### Fase 5 — Interfaz de usuario / Chat

- [x] Página web de pruebas (Streamlit) / chat local (prototipo) <!-- id:phase5_streamlit -->
- [ ] Integración con plataformas de mensajería (Telegram / Twilio) <!-- id:phase5_platforms -->

### Fase 6 — Formato de salida y experiencia

- [x] Respuesta formateada con comparativos y recomendación (`app/bot/formatter.py`) <!-- id:phase6_formatter -->
- [ ] Manejo de errores y mensajes de fallback (robustecer) <!-- id:phase6_errors -->

### Fase 7 — Pruebas, métricas y operación

- [ ] Pruebas unitarias e integración (completar) <!-- id:phase7_tests -->
- [x] Logs y monitoreo (básico) <!-- id:phase7_logging -->
- [ ] KPI / métricas (implementación) <!-- id:phase7_kpis -->

### Fase 8 — Despliegue y mantenimiento

- [ ] Contenerización / despliegue (Docker) <!-- id:phase8_docker -->
- [ ] Documentación de operación (runbooks) <!-- id:phase8_runbooks -->


## **Pasos recomendados inmediatos (prioritarios para MVP)**

- 1) Completar el pipeline NLP: validar extractor con ejemplos reales y añadir matcher de ciudades.
- 2) Implementar el scraping Playwright para Sictac y RNDC (end-to-end) y pruebas básicas.
- 3) Conectar `services/query_service.py` con el scraper y el formatter para responder a consultas.
- 4) Exponer un webhook mínimo para probar con Telegram (bot gratuito) y la UI Streamlit.

## **Dónde está el código relevante**

- `main.py` — punto de entrada.
- [app/bot/handler.py](app/bot/handler.py#L1) — lógica del bot.
- [app/bot/formatter.py](app/bot/formatter.py#L1) — formateo de respuestas.
- [nlp/extractor.py](nlp/extractor.py#L1), [nlp/normalizer.py](nlp/normalizer.py#L1) — NLP.
- [data/loader.py](data/loader.py#L1), [data/processor.py](data/processor.py#L1) — ingest y procesamiento.
- `docker/playwright/` — orquestación Playwright para scraping.

---

Si quieres, puedo:
- Ejecutar pruebas unitarias y reportar fallos.
- Implementar el scraper básico (Playwright) para Sictac como siguiente paso.
- Crear issues/checklist en Git con las tareas pendientes.

