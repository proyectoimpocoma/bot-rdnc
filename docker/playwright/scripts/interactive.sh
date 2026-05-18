#!/usr/bin/env bash
# ==============================================
# Script para sesión interactiva de Playwright
# Útil para debugging y desarrollo
# ==============================================
set -euo pipefail

echo "🎭 Sesión interactiva de Playwright"
echo "======================================="

# Instalar dependencias
if command -v uv &> /dev/null; then
    echo "📦 Instalando dependencias con uv..."
    uv sync
else
    echo "📦 Usando pip..."
    pip install -e ".[dev]"
fi

echo ""
echo "✅ Entorno listo. Comandos útiles:"
echo ""
echo "  python -m playwright codegen           # Generar código grabando acciones"
echo "  python -m playwright open <url>         # Abrir URL en browser"
echo "  python -m playwright screenshot <url>   # Capturar screenshot"
echo "  python -c 'from playwright...'          # Ejecutar script Python"
echo ""

# Abrir shell interactivo
exec /bin/bash
