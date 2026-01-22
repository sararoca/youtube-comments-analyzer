from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Motor para conexión con la BD
engine = create_engine(DATABASE_URL)

