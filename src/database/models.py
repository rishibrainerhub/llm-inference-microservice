from sqlalchemy import Column, Integer, String, Float, Boolean, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import ARRAY

Base = declarative_base()


class ReviewResult(Base):
    __tablename__ = "review_results"

    review_id = Column(Integer, primary_key=True, index=True)
    original_text = Column(String)
    sentiment = Column(String)
    confidence = Column(Float)
    entities = Column(ARRAY(String))
    text_length = Column(Integer)
    contains_product_mention = Column(Boolean)
    processed_at = Column(TIMESTAMP)
