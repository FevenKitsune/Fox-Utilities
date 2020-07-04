from sqlalchemy import create_engine
from main import logger

# Create database in root folder outside of Git repository.
logger.info("Loading SQLAlchemy engine.")
engine = create_engine('sqlite:///../../db/db.db')
