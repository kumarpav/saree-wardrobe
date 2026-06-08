from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class Saree(Base):
    __tablename__ = "sarees"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(64), index=True, default="")
    name = Column(String(200), default="")
    saree_name = Column(String(200), default="")
    body_color = Column(String(60), default="")
    border_color = Column(String(60), default="")
    region_name = Column(String(120), default="")
    color = Column(String(60), default="")
    fabric = Column(String(80), default="")
    occasion = Column(String(120), default="")
    price = Column(String(40), default="")
    purchase_date = Column(String(20), default="")
    notes = Column(Text, default="")
    image = Column(Text, default="")  # base64 data URL or URL
    created_at = Column(DateTime, default=datetime.utcnow)


class Blouse(Base):
    __tablename__ = "blouses"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(64), index=True, default="")
    name = Column(String(200), default="")
    color = Column(String(60), default="")
    fabric = Column(String(80), default="")
    occasion = Column(String(120), default="")
    price = Column(String(40), default="")
    purchase_date = Column(String(20), default="")
    notes = Column(Text, default="")
    image = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)


class Config(Base):
    __tablename__ = "config"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(64), index=True, default="")
    display_name = Column(String(120), default="")


class Outfit(Base):
    __tablename__ = "outfits"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(64), index=True, default="")
    name = Column(String(200), default="")
    saree_id = Column(Integer, nullable=True)
    blouse_id = Column(Integer, nullable=True)
    occasion = Column(String(120), default="")
    last_worn = Column(String(20), default="")
    created_at = Column(DateTime, default=datetime.utcnow)
