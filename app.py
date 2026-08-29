"""Glitch4ce Main WSGI Entrypoint & Application Factory."""
import os

from app import create_app

# WSGI Application instance for Gunicorn, Render, and development server
app = create_app(os.environ.get('FLASK_ENV', 'development'))

if __name__ == '__main__':
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', '5000'))
    debug = os.environ.get('FLASK_DEBUG', '1') == '1'
    app.run(host=host, port=port, debug=debug)