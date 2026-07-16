"""Legacy industrial graph engine."""

# Intentionally avoid importing engine/storage at package level to prevent
# circular imports from app.models.schemas, which re-exports legacy schemas.
# Import concrete modules directly, e.g.:
#   from app.engines.legacy.engine import LegacyEngine
#   from app.engines.legacy import storage as legacy_storage
