#!/usr/bin/env python3
"""
Startup script that ensures .env is loaded before running the app.
"""
import os
import sys
from pathlib import Path

# Get the directory where this script is located
script_dir = Path(__file__).parent.resolve()
env_file = script_dir / ".env"

# Load environment variables from .env file
if env_file.exists():
    print(f"[START] Loading env from: {env_file}")
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value
                if 'API_KEY' in key:
                    print(f"[START] Loaded {key}: {value[:20]}...")
else:
    print(f"[START] WARNING: .env not found at {env_file}")

# Change to script directory
os.chdir(script_dir)

# Now import and run the app
print("[START] Starting Flask app...")
from app import app

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
