import os
from dotenv import load_dotenv

load_dotenv()

# API de Gemini AI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configuración de Base de Datos
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "easygenapp")