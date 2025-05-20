import os
from sqlalchemy import create_engine
from models.users import Base
from models.agents import Base
from models.attendeeDetails import Base
from models.callLog import Base
from models.billingDetails import Base
from  models.usage_history import Base
from models.call_records import Base
from models.conversation import Base
from models.custom_tools import Base
from models.knowledgeBases import Base
from models.phone_numbers import Base
from models.phone_provider import Base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
load_dotenv()
# Configure your database connection string
# It's recommended to use environment variables for sensitive information
DATABASE_URL = os.getenv("DATABASE_URL")

# Replace with your actual database connection string if not using environment variable
# Example: DATABASE_URL = "postgresql://postgres:mysecretpassword@localhost:5432/rtcl_db"

engine = create_engine(DATABASE_URL)

def create_db_tables():
    """Creates all tables defined in models.py in the database."""
    print(f"Attempting to connect to database: {DATABASE_URL.split('@')[-1]}...")
    try:
        # Check connection first (optional but helpful for debugging)
        with engine.connect() as connection:
            print("Database connection successful.")

        print("Creating database tables...")
        # Manually create each table
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully (if they didn't already exist).")

    except Exception as e:
        print(f"An error occurred during database connection or table creation: {e}")
        print("Please ensure your DATABASE_URL is correct and the PostgreSQL server is running.")

if __name__ == "__main__":
    create_db_tables()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print(f"An error occurred while accessing the database: {e}")
        raise
    finally:
        db.close()