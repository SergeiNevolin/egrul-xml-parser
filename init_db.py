from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
import models
import os
import dotenv

dotenv.load_dotenv()

login = os.getenv("POSTGRES_LOGIN")
passw = os.getenv("POSTGRES_PASS")

engine = create_engine("postgresql://user:hackme@localhost")

session = sessionmaker(bind=engine)

models.Base.metadata.drop_all(engine)
models.Base.metadata.create_all(engine)
