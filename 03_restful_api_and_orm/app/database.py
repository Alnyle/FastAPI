from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base




# SessionLocal: API for the user.
# Engine: coordinator that actually handles communication with the database.


# sqlite:// → use SQLite (a lightweight database stored in a file).
# ./todos.db → the database file is in the current directory.
# If the file doesn’t exist, SQLite will create it.
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'

# The engine is the heavy lifter under the hood.

    # It manages:
        # Database connections (like a connection pool).
        # Sending raw SQL to the database.
        # Getting results back.
        
# The engine knows how to connect to your database (SQLite in this case).
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})


# SessionLocal (it's like your API to talk to the DB)
# You (the user/code) mostly talk to the Session.
# It gives you a nice Pythonic way to query, insert, update, delete.
# It also keeps track of objects you’ve changed in memory (before sending them to the DB).
# Think of it like a friendly translator between you and the engine.

# autocommit=False → You need to explicitly call session.commit() to save changes.
# autoflush=False → SQLAlchemy won’t automatically push changes to the database until needed (you control when it flushes).
# bind=engine → Connect this session factory to your engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This creates the Base class for all your ORM models.
Base = declarative_base()