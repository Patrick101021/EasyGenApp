import os

# Credenciales de la base de datos JawsDB
DB_HOST = os.getenv('DB_HOST', 'fnx6frzmhxw45qcb.cbetxkdyhwsb.us-east-1.rds.amazonaws.com')
DB_USER = os.getenv('DB_USER', 'njty1yh1vnpnxgsm')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'pqm2ynyft3owopt6')
DB_NAME = os.getenv('DB_NAME', 'p1o44euv559ey6de')

# API Key de Google Gemini (o cualquier otra API que uses)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'tu_api_key_de_google_gemini')
