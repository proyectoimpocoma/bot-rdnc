from diskcache import Cache

from app.core import sicetac_cache


def test_sicetac_cache_operations():
    # Probar que podemos escribir y leer del caché persistente global
    test_key = "test_origen:test_destino:3s3:cargado:estacas:general:1"
    test_value = "$ 1,500,000"

    # Asegurar que esté vacío para esta clave antes de la prueba
    if test_key in sicetac_cache:
        del sicetac_cache[test_key]

    # Verificar que retorne None al inicio
    assert sicetac_cache.get(test_key) is None

    # Guardar valor
    sicetac_cache.set(test_key, test_value, expire=10)

    # Recuperar valor
    assert sicetac_cache.get(test_key) == test_value

    # Limpiar al finalizar
    del sicetac_cache[test_key]


def test_cache_persistence_on_disk(tmp_path):
    # Crear un directorio temporal para simular la persistencia
    cache_path = tmp_path / "temp_cache"

    # Abrir la caché y guardar un valor
    with Cache(str(cache_path)) as cache1:
        cache1.set("key1", "value1")
        assert cache1.get("key1") == "value1"

    # Reabrir la caché en el mismo directorio temporal y comprobar persistencia
    with Cache(str(cache_path)) as cache2:
        assert cache2.get("key1") == "value1"
