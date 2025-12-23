# create session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# this is for Postgresql and for this we need to install postgresql in our system
# db_url="postgresql://postgres:12345678@localhost:5432/db_name"
# engine=create_engine(db_url)
# session=sessionmaker(autocommit=False,autoflush=False,bind=engine)

# Use SQLite (no installation needed!)
DATABASE_URL = "sqlite:///./app.db"

# For SQLite, add this parameter
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Only for SQLite
)
# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Keep 'session' name for backward compatibility with your main.py
session = SessionLocal
