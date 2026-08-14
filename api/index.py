import sys
import os

# Ensure backend package is importable when running in Vercel serverless environment
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BACKEND_PATH = os.path.join(ROOT, 'backend')
if BACKEND_PATH not in sys.path:
    sys.path.insert(0, BACKEND_PATH)

from app.main import app

# Vercel's Python runtime will use the `app` ASGI application exported here.
