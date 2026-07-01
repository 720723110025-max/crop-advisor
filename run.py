#!/usr/bin/env python
"""
Main application runner for Crop Advisory System.
This file is the Gunicorn WSGI entry point: gunicorn run:app
"""

import os
from app import create_app

app = create_app(os.environ.get('FLASK_ENV', 'default'))

if __name__ == '__main__':
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', os.environ.get('FLASK_PORT', 5000)))
    debug = os.environ.get('FLASK_ENV', 'default') == 'development'
    app.run(host=host, port=port, debug=debug)
