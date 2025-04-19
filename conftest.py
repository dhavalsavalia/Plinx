import pytest

from plinx import Plinx


# Application fixtures
@pytest.fixture
def app():
    return Plinx()


@pytest.fixture
def client(app):
    return app.test_session()