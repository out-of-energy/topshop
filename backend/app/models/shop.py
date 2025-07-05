from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, Enum
from sqlalchemy.sql import func
import enum
from app.core.database import Base

class Region(enum.Enum):
    NORTH_AMERICA = "north_america"
    EUROPE = "europe"
    MIDDLE_EAST = "middle_east"

class ShopStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"

class Shop(Base):
    __tablename__ = "shops"
    
    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=True)
    region = Column(Enum(Region), nullable=False)
    
    # Shopify verification
    is_shopify = Column(Boolean, default=False)
    shopify_verified_at = Column(DateTime, nullable=True)
    
    # Category classification
    is_womens_fashion = Column(Boolean, default=False)
    category_confidence = Column(Float, default=0.0)
    category_verified_at = Column(DateTime, nullable=True)
    
    # Ranking metrics
    traffic_rank = Column(Integer, nullable=True)
    monthly_visits = Column(Integer, nullable=True)
    social_media_score = Column(Float, default=0.0)
    seo_score = Column(Float, default=0.0)
    overall_score = Column(Float, default=0.0)
    
    # Status and metadata
    status = Column(Enum(ShopStatus), default=ShopStatus.ACTIVE)
    last_checked = Column(DateTime, default=func.now())
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Additional data
    description = Column(Text, nullable=True)
    logo_url = Column(String(500), nullable=True)
    screenshot_url = Column(String(500), nullable=True)
    
    def __repr__(self):
        return f"<Shop(domain='{self.domain}', region='{self.region}', is_shopify={self.is_shopify})>" 