"""Glitch4ce Database Inspector Utility.

For the interactive web admin console, run `python app.py` and navigate to `/admin`.
"""
from app import create_app
from app.models import GameplaySession, User


def inspect_database():
    """Inspect and display summary of database players and logs."""
    app = create_app('development')
    with app.app_context():
        players = User.query.order_by(User.created_at.desc()).all()
        total_sessions = GameplaySession.query.count()

        print("\n" + "=" * 50)
        print("👾 GLITCH4CE DATABASE TELEMETRY")
        print("=" * 50)
        print(f"Total Players: {len(players)}")
        print(f"Total Gameplay Sessions: {total_sessions}\n")

        for player in players:
            status = "🔒 Secured" if player.password_hash else "👤 Guest"
            print(f" • {player.username:<20} | {player.total_plays} plays | {status}")

        print("=" * 50)
        print("Web Admin Portal is available at: http://localhost:5000/admin\n")


if __name__ == '__main__':
    inspect_database()