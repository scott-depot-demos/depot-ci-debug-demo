import pytest
import os
from app.main import app, get_db_connection


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health(client):
    """Health endpoint should always return 200."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_database_url_is_set():
    """DATABASE_URL must be present in the environment."""
    db_url = os.environ.get("DATABASE_URL")
    assert db_url is not None, (
        "DATABASE_URL is not set. "
        "Make sure it is configured as a secret in Depot CI."
    )


def test_database_connection():
    """Should be able to connect to the database."""
    try:
        conn = get_db_connection()
        conn.close()
    except RuntimeError as e:
        pytest.fail(str(e))
    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")


def test_users_endpoint(client):
    """Users endpoint should return a list."""
    response = client.get("/users")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
