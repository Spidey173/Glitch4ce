"""Main arcade hub views and gameplay tracking API."""
from datetime import datetime, timezone

from flask import Blueprint, jsonify, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.extensions import csrf, db
from app.models import GameplaySession

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Root redirector based on authentication state."""
    if current_user.is_authenticated:
        return redirect(url_for('main.games'))
    return redirect(url_for('auth.login'))


@main_bp.route('/games')
@login_required
def games():
    """Render the main cyberpunk Arcade Hub dashboard."""
    user_sessions = (
        GameplaySession.query
        .filter_by(player_id=current_user.id)
        .order_by(GameplaySession.started_at.desc())
        .all()
    )

    # Format history tuples for template compatibility: (game_name, timestamp_str)
    game_history = [(s.game_name, s.formatted_timestamp) for s in user_sessions]
    game_count = len(game_history)

    return render_template(
        'Games/game.html',
        username=current_user.username,
        game_count=game_count,
        game_history=game_history
    )


@main_bp.route('/start_game/<path:game_name>', methods=['POST'])
@csrf.exempt  # Allow beacon and direct AJAX telemetry with current_user session
def start_game(game_name):
    """Log a new game launch event."""
    if not current_user.is_authenticated:
        return jsonify({'error': 'unauthorized'}), 401

    clean_game_name = game_name.strip()
    now_utc = datetime.now(timezone.utc)

    # Prevent duplicate logging within 2 seconds
    recent_session = (
        GameplaySession.query
        .filter_by(player_id=current_user.id, game_name=clean_game_name)
        .order_by(GameplaySession.id.desc())
        .first()
    )

    if recent_session and recent_session.started_at:
        # If started_at is naive, make it aware for comparison
        started_at = recent_session.started_at
        if started_at.tzinfo is None:
            started_at = started_at.replace(tzinfo=timezone.utc)
        if (now_utc - started_at).total_seconds() < 2:
            return jsonify({'status': 'deduped', 'game': clean_game_name, 'session_id': recent_session.id})

    new_session = GameplaySession(
        player_id=current_user.id,
        game_name=clean_game_name,
        started_at=now_utc
    )
    db.session.add(new_session)
    db.session.commit()

    return jsonify({'status': 'logged', 'game': clean_game_name, 'session_id': new_session.id})


@main_bp.route('/end_game/<path:game_name>', methods=['POST'])
@csrf.exempt
def end_game(game_name):
    """Log the end of a game session and compute duration."""
    if not current_user.is_authenticated:
        return jsonify({'error': 'unauthorized'}), 401

    clean_game_name = game_name.strip()
    now_utc = datetime.now(timezone.utc)

    # Find the most recent active session for this game
    active_session = (
        GameplaySession.query
        .filter_by(player_id=current_user.id, game_name=clean_game_name)
        .filter(GameplaySession.ended_at.is_(None))
        .order_by(GameplaySession.id.desc())
        .first()
    )

    if active_session:
        active_session.ended_at = now_utc
        if active_session.started_at:
            started_at = active_session.started_at
            if started_at.tzinfo is None:
                started_at = started_at.replace(tzinfo=timezone.utc)
            active_session.duration_seconds = int((now_utc - started_at).total_seconds())
        db.session.commit()

    return jsonify({'status': 'ended', 'game': clean_game_name})


@main_bp.route('/api/history')
def api_history():
    """JSON API endpoint returning real-time player history and counts."""
    if not current_user.is_authenticated:
        return jsonify({'error': 'unauthorized', 'history': [], 'count': 0}), 401

    user_sessions = (
        GameplaySession.query
        .filter_by(player_id=current_user.id)
        .order_by(GameplaySession.started_at.desc())
        .limit(100)
        .all()
    )

    history = [s.to_dict() for s in user_sessions]
    return jsonify({
        'username': current_user.username,
        'count': len(history),
        'history': history
    })
