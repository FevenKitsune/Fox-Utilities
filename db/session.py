from .engine import engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)

session = Session()