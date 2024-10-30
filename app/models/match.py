 
from sqlalchemy import Boolean, Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.backend.db import Base
from datetime import datetime

class Match(Base):
    __tablename__ = 'matches'
    id = Column(Integer, primary_key=True, index=True)
    liker_id = Column(Integer, ForeignKey('clients.id'))
    liked_id = Column(Integer, ForeignKey('clients.id'))
    timestamp = Column(DateTime, default=datetime.now)
    is_mutual = Column(Boolean, default=False) 

    liker = relationship('Client', foreign_keys=[liker_id], back_populates='likes_given')
    liked = relationship('Client', foreign_keys=[liked_id], back_populates='likes_received')
