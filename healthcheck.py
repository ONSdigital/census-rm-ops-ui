import os

import requests

response = requests.get(f'http://localhost:{os.getenv("PORT", "8243")}/health/')
response.raise_for_status()
