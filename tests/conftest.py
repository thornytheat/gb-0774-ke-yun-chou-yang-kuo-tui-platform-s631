import pytest

from app.main import create_app
from app.pipeline import run
from app.source import sources


@pytest.fixture
def tables():
    return sources({'sample':'dirty'})


@pytest.fixture
def dirty(tables):
    return run(tables)


@pytest.fixture
def client(tmp_path):
    return create_app(tmp_path/'survey.db').test_client()
