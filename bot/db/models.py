from sqlalchemy import Column, Integer, BigInteger, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()



class PlayerScore(Base):
    __tablename__ = "playerscore"

    user_id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    user_name = Column(String)
    score = Column(BigInteger, default=0)
