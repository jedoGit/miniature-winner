import os
from dotenv import load_dotenv

# Check what's the current environment. Defaults to development
enrivonment = os.getenv("MYAPP_ENV", "development")

 # Load environment variables from .env file
dotenv_path = f'.env-{enrivonment}'
load_dotenv(dotenv_path=dotenv_path)

# Assign the env files to global constants
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
