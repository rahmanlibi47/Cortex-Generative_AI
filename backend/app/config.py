import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_KEY = os.getenv('API_KEY')
    API_URL = 'https://api.textcortex.com/v1/texts/completions'
