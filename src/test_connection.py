from sqlalchemy import create_engine, text
from src.config import DATABASE_URL


engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        print("PostgreSQL connection successful!")
        print(result.fetchone()[0])

except Exception as e:
    print("PostgreSQL connection failed!")
    print(e)