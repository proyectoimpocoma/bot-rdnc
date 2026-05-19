# Bot RNDC / Sictac Automation

Este repositorio es un proyecto de automatización y prototipo de chatbot para consultar rutas y costos en los portales RNDC y Sictac usando Playwright y Streamlit.

## 🚀 Qué hace hoy

- `main.py` es el punto de entrada principal.
- `app/UI/` contiene la interfaz de usuario con Streamlit.
- `app/scrapper/` contiene los scrapers para:
  - `rndc.py` — automatiza el portal RNDC y descarga un archivo Excel.
  - `sicetac.py` — automatiza el portal Sictac para configuración de ruta y cálculo de costo.
- `app/core/logging.py` centraliza el logging en consola y en JSON.
- `app/services/query_service.py` es la base de la lógica de consulta sobre datos cargados.
- `app/nlp/` es el esqueleto de extracción de texto y normalización de términos.

## 📦 Requisitos

- Python 3.12+
- `uv` (recomendado para el manejo de comandos)
- Dependencias definidas en `pyproject.toml`

## ⚙️ Instalación

```bash
cd c:\Users\TEMPORAL\Documents\Automation\bot-rdnc
uv sync
```

## ▶️ Cómo ejecutar

### Interfaz Streamlit

```bash
uv run streamlit run main.py
```

### Alternativa sin `uv`

```bash
python -m streamlit run main.py
```

## 🧠 Estado actual

- `app/scrapper/rndc.py` ya contiene la lógica para:
  - abrir el portal RNDC
  - resolver el captcha numérico
  - completar la fecha del mes anterior
  - descargar un Excel a `data/RNDC.xlsx`
- `app/scrapper/sicetac.py` tiene el flujo inicial del formulario Sictac y la lógica de selección de `<select>`.
- El scraper RNDC se ejecuta hoy solo el primer día del mes cuando se lanza `main.py`.
- El scraper Sictac se intenta ejecutar en cada arranque actual, pero está en fase de validación del flujo.

## 📁 Estructura del proyecto

```text
app/
  bot/
  config/
  core/
  data/
  nlp/
  scrapper/
  services/
  UI/
main.py
pyproject.toml
README.md
docker/playwright/
```

### Carpetas clave

- `app/bot/` — formatea respuestas y gestiona la lógica de bot.
- `app/core/` — utilidades comunes, logging y configuración.
- `app/data/` — carga y procesamiento de datos.
- `app/nlp/` — extracción y normalización de texto natural.
- `app/scrapper/` — automatización de navegadores con Playwright.
- `app/UI/` — interfaz Streamlit.
- `docker/playwright/` — configuración para ejecutar Playwright en contenedor.

## 🧩 Módulos importantes

- `main.py` — arranca la app y llama al scraper RNDC el día 1 del mes.
- `app/scrapper/browser.py` — configuración del navegador Playwright y descargas.
- `app/scrapper/selectors.py` — selectores CSS/constantes usados por los scrapers.
- `app/scrapper/utils.py` — utilidades auxiliares como extracción de números y cálculo de fecha anterior.
- `app/scrapper/rndc.py` — flujo RNDC.
- `app/scrapper/sicetac.py` — flujo Sictac.

## 📘 Contenido heredado del README base

Este proyecto originalmente partió de una plantilla base generada con `personal-cli`. La documentación base y el checklist guardan el estado del desarrollo y ayudan a mantener el roadmap visible.

### Python Base Project

Este proyecto fue generado usando `personal-cli`. Es una plantilla base minimalista configurada con las mejores prácticas de la industria, ideal para scripts, librerías, o proyectos customizados que no requieren de un framework web pesado.

### Fase 0 — Preparación del repositorio

- [x] Inicializar entorno: `uv sync` y activar venv <!-- id:phase0_init_env -->
- [x] Entradas básicas y README: Documentación inicial <!-- id:phase0_docs -->
- [ ] Archivos clave: [main.py](main.py#L1), [pyproject.toml](pyproject.toml#L1) <!-- id:phase0_files -->

### Fase 1 — NLP (Procesamiento de lenguaje natural)

- [x] Definir entidades: ciudades, departamentos, tipo vehículo <!-- id:phase1_def_entities -->
  - Referencia: [nlp/extractor.py](app/nlp/extractor.py#L1), [nlp/normalizer.py](app/nlp/normalizer.py#L1)
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

## ✅ Cómo contribuir

- Actualiza selectores en `app/scrapper/selectors.py` si cambia la página.
- Añade validación de `page.wait_for_selector(...)` en los scrapers para robustecer el flujo.
- Implementa `app/nlp/` para mejorar el parseo de consultas en el bot.
- Añade tests para `app/scrapper/` y `app/nlp/`.

## 🧪 Comandos útiles

```bash
uv run ruff check --fix .
uv run ruff format .
uv run mypy .
pre-commit install
```

## 🔍 Notas específicas

- El proyecto usa `pyproject.toml` con dependencias como `playwright`, `streamlit`, `polars`, `spacy` y `rich`.
- Para usar Playwright en Docker, revisa `docker/playwright/docker-compose.yml` y `docker/playwright/scripts/`.
- Si el scraper falla en Streamlit, captura las excepciones en el nivel superior y muestra un mensaje amigable en lugar de dejar escapar la traza completa.

---

Si quieres, puedo seguir con:
- documentar un flujo completo de `rncd` + `sictac` en README;
- actualizar el `main.py` para que el comportamiento actual sea más claro;
- añadir un ejemplo de uso con `streamlit` y un comando de ejecución mensual.
