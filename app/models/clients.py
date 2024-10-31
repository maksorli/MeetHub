from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.orm import relationship

from app.backend.db import Base


class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    gender = Column(String)
    avatar = Column(String)
    longitude = Column(Float)
    latitude = Column(Float)
    registration_date = Column(DateTime, default=datetime.now)

    daily_likes_count = Column(Integer, default=0)
    last_like_date = Column(DateTime, default=datetime.now)

    likes_given = relationship(
        "Match", foreign_keys="Match.liker_id", back_populates="liker", lazy="dynamic"
    )
    likes_received = relationship(
        "Match", foreign_keys="Match.liked_id", back_populates="liked", lazy="dynamic"
    )
