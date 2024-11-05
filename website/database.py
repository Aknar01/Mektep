# Create a database URL for SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Local SQLite3 database url
SQLALCHEMY_DATABASE_URL = r'sqlite:////Users/aknar/PycharmProjects/Мектеп/website/database/db.db'

# # Remote PostgreSQL database url
# SQLALCHEMY_DATABASE_URL = "postgres://username:password@localhost:5432/DB_Name"

# # Remote MySQL database url
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://username:password@localhost:3306/DB_Name"

# check_same_thread:
# using normal functions (def) more than one thread could interact with the database for the same request,
# so we need to make SQLite know that it should allow that with
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Each instance of the SessionLocal class will be a database session. The class itself is not a database session yet
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is used to create each of the database models or classes (the ORM models)
Base = declarative_base()

