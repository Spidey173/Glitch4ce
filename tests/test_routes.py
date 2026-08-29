"""Integration tests for arcade routes, game templates, and admin views."""


def test_root_redirect_unauthenticated(client):
    """Test unauthenticated user visiting / is redirected to /login."""
    response = client.get('/', follow_redirects=False)
    assert response.status_code == 302
    assert '/login' in response.headers['Location']


def test_root_redirect_authenticated(auth_client):
    """Test authenticated user visiting / is redirected to /games."""
    response = auth_client.get('/', follow_redirects=False)
    assert response.status_code == 302
    assert '/games' in response.headers['Location']


def test_games_dashboard_renders(auth_client):
    """Test that main arcade hub dashboard renders properly with games."""
    response = auth_client.get('/games')
    assert response.status_code == 200
    assert b'Arcade Hub' in response.data
    assert b'2048' in response.data
    assert b'Flappy Bird' in response.data
    assert b'Whack a Mole' in response.data
    assert b'SpeedType Pro' in response.data


def test_game_templates_render(client):
    """Test that direct game routes render valid HTML."""
    routes_to_test = [
        '/2048',
        '/FlappyBird',
        '/Maze',
        '/mazeeasy',
        '/pong',
        '/memorymatch',
        '/quiz',
        '/stonepapersissors',
        '/tictactoe',
        '/TowerBlock',
        '/tricky',
        '/mole',
        '/Candy_Crush',
        '/speedtype',
        '/speedtypepro'
    ]
    for route in routes_to_test:
        response = client.get(route)
        assert response.status_code == 200, f"Route {route} returned status {response.status_code}"


def test_admin_dashboard(auth_client):
    """Test that admin dashboard renders player metrics."""
    response = auth_client.get('/admin', follow_redirects=True)
    assert response.status_code == 200
    assert b'Admin Core' in response.data
    assert b'CyberTester' in response.data


def test_404_error_page(client):
    """Test custom 404 error page."""
    response = client.get('/non-existent-sector')
    assert response.status_code == 404
    assert b'404' in response.data
    assert b'SECTOR NOT FOUND' in response.data
