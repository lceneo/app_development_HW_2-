from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    url = 'postgresql+psycopg2://postgres:postgres@localhost:5432/test_db',
    echo=True)

session_factory = sessionmaker(engine)