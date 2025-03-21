import os

class Config:
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    
# API Key de Google Gemini (o cualquier otra API que uses)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyCEwBPj7AvUJTVjkcnqS9bq43Om6ZZd4Kg')

