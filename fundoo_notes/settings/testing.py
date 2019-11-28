from .base import *
from dotenv import load_dotenv, find_dotenv
from pathlib import *
try:
    from .base import *
except ImportError:
    print("Import error")

load_dotenv(find_dotenv())

env_path = Path('.') / '.env'