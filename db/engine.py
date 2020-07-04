from sqlalchemy import create_engine

# Create database in root folder outside of Git repository.
engine = create_engine('sqlite:////usr/src/app/db/db.db')
