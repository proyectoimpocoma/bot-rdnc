#!/usr/bin/env bash
# ==============================================
# Script para ejecutar tests de Playwright
# dentro del contenedor Docker
# ==============================================
set -euo pipefail

echo "🎭 Ejecutando tests de Playwright..."
echo "======================================="

# Instalar dependencias del proyecto con uv
if command -v uv &> /dev/null; then
    echo "📦 Instalando dependencias con uv..."
    uv sync
else
    echo "📦 uv no encontrado, usando pip..."
    pip install -e ".[dev]"
fi

# Verificar que Playwright está disponible
python -c "from playwright.sync_api import sync_playwright; print('✅ Playwright importado correctamente')"

# Ejecutar tests (ajusta la ruta según tu estructura)
echo ""
echo "🧪 Ejecutando tests..."
python -m pytest tests/ -v --tb=short "$@"

echo ""
echo "✅ Tests completados."
