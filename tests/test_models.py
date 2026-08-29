"""Unit tests for SQLAlchemy models."""
from app.extensions import db
from app.models import GameplaySession, User


def test_user_creation_and_password_hashing(app):
    """Test user creation, password hashing, and verification."""
    with app.app_context():
        user = User(username='NeoPlayer', is_guest=False)
        user.set_password('Synthwave2026!')
        db.session.add(user)
        db.session.commit()

        queried = User.query.filter_by(username='NeoPlayer').first()
        assert queried is not None
        assert queried.username == 'NeoPlayer'
        assert queried.password_hash is not None
        assert queried.password_hash != 'Synthwave2026!'
        assert queried.check_password('Synthwave2026!') is True
        assert queried.check_password('WrongPass!') is False
        assert queried.is_authenticated is True


def test_gameplay_session_relationship(app, test_user):
    """Test relationship between User and GameplaySession."""
    with app.app_context():
        user = db.session.get(User, test_user.id)
        session1 = GameplaySession(player_id=user.id, game_name='2048')
        session2 = GameplaySession(player_id=user.id, game_name='Flappy Bird')
        db.session.add_all([session1, session2])
        db.session.commit()

        assert user.total_plays == 2
        sessions = user.sessions.all()
        assert len(sessions) == 2
        game_names = [s.game_name for s in sessions]
        assert '2048' in game_names
        assert 'Flappy Bird' in game_names


def test_cascade_delete(app, test_user):
    """Test that deleting a user cascades to their gameplay sessions."""
    with app.app_context():
        user = db.session.get(User, test_user.id)
        session1 = GameplaySession(player_id=user.id, game_name='Maze')
        db.session.add(session1)
        db.session.commit()

        assert GameplaySession.query.filter_by(player_id=user.id).count() == 1

        db.session.delete(user)
        db.session.commit()

        assert GameplaySession.query.filter_by(player_id=test_user.id).count() == 0
