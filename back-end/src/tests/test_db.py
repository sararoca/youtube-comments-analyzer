from src.config.database import engine

try:
    conn = engine.connect()
    print("Conexión a PostgreSQL correcta")
    conn.close()
except Exception as e:
    print("Error:", e)
