"""Pytest test fixtures and setup for Glitch4ce."""
import pytest

from app import create_app
from app.extensions import db
from app.models import User


@pytest.fixture
def app():
    """Create test application configured for testing."""
    test_app = create_app('testing')

    with test_app.app_context():
        db.create_all()
        yield test_app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Test HTTP client."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Test CLI runner."""
    return app.test_cli_runner()


@pytest.fixture
def test_user(app):
    """Create a sample registered user in test db."""
    with app.app_context():
        user = User(username='CyberTester', is_guest=False)
        user.set_password('SecretPass123!')
        db.session.add(user)
        db.session.commit()
        return db.session.get(User, user.id)


@pytest.fixture
def auth_client(client, test_user):
    """Test HTTP client logged in as test_user."""
    client.post('/login', data={
        'username': 'CyberTester',
        'password': 'SecretPass123!'
    }, follow_redirects=True)
    return client
