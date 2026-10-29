"""Memory.close must release owned PGVector connection pools."""

from unittest.mock import MagicMock

import pytest

from mem0.vector_stores.pgvector import PGVector, PSYCOPG_VERSION


def test_pgvector_close_closes_psycopg3_pool_once():
    store = PGVector.__new__(PGVector)
    pool = MagicMock()
    store.connection_pool = pool

    if PSYCOPG_VERSION != 3:
        pytest.skip("this assertion targets the psycopg3 close() path")

    store.close()
    pool.close.assert_called_once_with()
    assert store.connection_pool is None

    store.close()  # idempotent
    pool.close.assert_called_once_with()


def test_memory_close_invokes_vector_store_close(monkeypatch):
    from mem0.memory.main import Memory

    mem = Memory.__new__(Memory)
    mem.db = MagicMock()
    mem.vector_store = MagicMock()
    mem._entity_store = MagicMock()
    mem._telemetry_vector_store = MagicMock()

    mem.close()

    mem.db.close.assert_called_once_with()
    mem.vector_store.close.assert_called_once_with()
    mem._entity_store.close.assert_called_once_with()
    mem._telemetry_vector_store.close.assert_called_once_with()
