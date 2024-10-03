import os
from firebase_admin import credentials, initialize_app

cred = credentials.Certificate("serviceAccountKey.json")
initialize_app(cred)

API_KEY = os.environ.get("API_KEY")
