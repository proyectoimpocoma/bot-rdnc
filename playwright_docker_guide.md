# 🎭 Guía: Playwright con Docker

## Estructura de Carpetas

```
bot-rdnc/
├── docker/
│   └── playwright/
│       ├── docker-compose.yml      # Configuración de Docker Compose
│       ├── .env.example            # Variables de entorno de ejemplo
│       └── scripts/
│           ├── run-tests.sh        # Ejecutar tests automatizados
│           └── interactive.sh      # Sesión interactiva/debugging
├── app/
├── tests/
├── .env                            # (existente — se monta al contenedor)
├── pyproject.toml
└── ...
```

> [!NOTE]
> La carpeta `docker/playwright/` está separada del código fuente para mantener la infraestructura desacoplada. El `docker-compose.yml` monta todo el proyecto raíz como `/app` dentro del contenedor.

---

## Imagen Utilizada

Se usa la imagen oficial de Microsoft:

```
mcr.microsoft.com/playwright/python:v1.52.0-noble
```

Esta imagen **ya incluye** todos los browsers (Chromium, Firefox, WebKit) pre-instalados, por lo que **no necesitas** ejecutar `playwright install` manualmente.

---

## Comandos de Uso

### 1️⃣ Levantar el contenedor

```bash
# Desde la raíz del proyecto:
docker compose -f docker/playwright/docker-compose.yml up -d
```

### 2️⃣ Ejecutar tests

```bash
# Opción A: Usar el script helper
docker compose -f docker/playwright/docker-compose.yml exec playwright \
  bash /app/docker/playwright/scripts/run-tests.sh

# Opción B: Ejecutar directamente
docker compose -f docker/playwright/docker-compose.yml exec playwright \
  python -m pytest tests/ -v
```

### 3️⃣ Sesión interactiva (debugging)

```bash
docker compose -f docker/playwright/docker-compose.yml exec playwright \
  bash /app/docker/playwright/scripts/interactive.sh
```

### 4️⃣ Ejecutar un script Python específico

```bash
docker compose -f docker/playwright/docker-compose.yml exec playwright \
  python mi_script.py
```

### 5️⃣ Usar Playwright codegen (grabar acciones)

```bash
docker compose -f docker/playwright/docker-compose.yml exec playwright \
  python -m playwright codegen https://ejemplo.com
```

> [!IMPORTANT]
> `codegen` necesita display. En Docker headless sin X11 forwarding, usa `--headless` o captura trazas/screenshots en su lugar.

### 6️⃣ Detener el contenedor

```bash
docker compose -f docker/playwright/docker-compose.yml down
```

---

## Tips y Notas

### Headless vs Headed

Dentro de Docker **siempre corre en modo headless**. Si necesitas ver el browser gráficamente, tienes dos opciones:

1. **X11 Forwarding** (Linux): Agrega estas variables al `docker-compose.yml`:
   ```yaml
   environment:
     - DISPLAY=${DISPLAY}
   volumes:
     - /tmp/.X11-unix:/tmp/.X11-unix
   ```

2. **VNC/noVNC**: Usar una imagen con VNC integrado (más complejo pero funciona en macOS).

3. **Trazas y screenshots** (recomendado): Configurar Playwright para guardar trazas:
   ```python
   context = browser.new_context()
   context.tracing.start(screenshots=True, snapshots=True)
   # ... acciones ...
   context.tracing.stop(path="trace.zip")
   ```

### Cache de uv

El volumen `uv-cache` persiste el cache de instalación de `uv` entre reinicios del contenedor, haciendo las instalaciones subsecuentes mucho más rápidas.

### Variables de Entorno

El contenedor carga automáticamente las variables de tu archivo `.env` en la raíz del proyecto. Si necesitas variables adicionales específicas para Docker, agrégalas en `docker/playwright/.env`.

### Alias útil (opcional)

Agrega a tu `~/.zshrc`:

```bash
alias pw-docker="docker compose -f docker/playwright/docker-compose.yml"
```

Así puedes usar:

```bash
pw-docker up -d
pw-docker exec playwright python mi_script.py
pw-docker down
```
