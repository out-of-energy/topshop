from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime
from enum import Enum

class Region(str, Enum):
    NORTH_AMERICA = "north_america"
    EUROPE = "europe"
    MIDDLE_EAST = "middle_east"

class ShopStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"

class ShopBase(BaseModel):
    domain: str
    name: Optional[str] = None
    region: Region
    description: Optional[str] = None

class ShopCreate(ShopBase):
    pass

class ShopUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_shopify: Optional[bool] = None
    is_womens_fashion: Optional[bool] = None
    category_confidence: Optional[float] = None
    traffic_rank: Optional[int] = None
    monthly_visits: Optional[int] = None
    social_media_score: Optional[float] = None
    seo_score: Optional[float] = None
    overall_score: Optional[float] = None
    status: Optional[ShopStatus] = None

class Shop(ShopBase):
    id: int
    is_shopify: bool = False
    shopify_verified_at: Optional[datetime] = None
    is_womens_fashion: bool = False
    category_confidence: float = 0.0
    category_verified_at: Optional[datetime] = None
    traffic_rank: Optional[int] = None
    monthly_visits: Optional[int] = None
    social_media_score: float = 0.0
    seo_score: float = 0.0
    overall_score: float = 0.0
    status: ShopStatus = ShopStatus.ACTIVE
    last_checked: datetime
    created_at: datetime
    updated_at: datetime
    logo_url: Optional[str] = None
    screenshot_url: Optional[str] = None

    class Config:
        from_attributes = True

class ShopList(BaseModel):
    shops: List[Shop]
    total: int
    page: int
    size: int

class ShopRanking(BaseModel):
    shop: Shop
    rank: int
    previous_rank: Optional[int] = None
    rank_change: Optional[int] = None

class RegionRanking(BaseModel):
    region: Region
    rankings: List[ShopRanking]
    last_updated: datetime 