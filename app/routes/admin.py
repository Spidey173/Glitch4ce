"""Admin dashboard routes for player and telemetry management."""
from flask import Blueprint, flash, redirect, render_template, url_for
from sqlalchemy import func

from app.extensions import db
from app.models import GameScore, GameplaySession, User

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('')
@admin_bp.route('/')
def index():
    """Admin dashboard overview of all registered players and stats."""
    players = User.query.order_by(User.created_at.desc()).all()
    total_players = len(players)
    total_sessions = GameplaySession.query.count()
    total_scores = GameScore.query.count()

    # Calculate top 5 most played games
    top_games = (
        db.session.query(
            GameplaySession.game_name,
            func.count(GameplaySession.id).label('play_count')
        )
        .group_by(GameplaySession.game_name)
        .order_by(func.count(GameplaySession.id).desc())
        .limit(5)
        .all()
    )

    # Calculate top high scores overall
    top_scores = (
        GameScore.query
        .order_by(GameScore.score.desc())
        .limit(5)
        .all()
    )

    return render_template(
        'admin/index.html',
        players=players,
        total_players=total_players,
        total_sessions=total_sessions,
        total_scores=total_scores,
        top_games=top_games,
        top_scores=top_scores
    )



@admin_bp.route('/player/<string:username>')
def player_detail(username):
    """View detailed gameplay records for a specific player."""
    player = User.query.filter_by(username=username).first_or_404()
    sessions = (
        GameplaySession.query
        .filter_by(player_id=player.id)
        .order_by(GameplaySession.started_at.desc())
        .all()
    )

    return render_template('admin/player_detail.html', player=player, sessions=sessions)


@admin_bp.route('/player/<string:username>/delete', methods=['POST'])
def delete_player(username):
    """Securely delete a player and all associated gameplay logs (POST with CSRF)."""
    player = User.query.filter_by(username=username).first_or_404()
    db.session.delete(player)
    db.session.commit()
    flash(f"Player '{username}' and all associated history have been removed.", "success")
    return redirect(url_for('admin.index'))
