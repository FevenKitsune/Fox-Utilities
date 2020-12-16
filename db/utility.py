from .base import Base
from .engine import engine


def create_all():
    Base.metadata.create_all(engine)
