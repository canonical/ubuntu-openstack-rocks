#!/usr/bin/env python3
from skyline_apiserver.main import app
from a2wsgi import ASGIMiddleware

application = ASGIMiddleware(app)