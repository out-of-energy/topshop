from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.schemas.shop import Shop, ShopCreate, ShopUpdate, ShopList, RegionRanking, Region
from app.models.shop import Shop as ShopModel, ShopStatus
from app.services.shopify_detector import ShopifyDetector
from app.services.fashion_classifier import FashionClassifier

router = APIRouter()

@router.get("/", response_model=ShopList)
def get_shops(
    region: Optional[Region] = Query(None, description="Filter by region"),
    is_shopify: Optional[bool] = Query(None, description="Filter by Shopify status"),
    is_womens_fashion: Optional[bool] = Query(None, description="Filter by women's fashion status"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size"),
    db: Session = Depends(get_db)
):
    """Get list of shops with optional filters"""
    query = db.query(ShopModel)
    
    if region:
        query = query.filter(ShopModel.region == region)
    if is_shopify is not None:
        query = query.filter(ShopModel.is_shopify == is_shopify)
    if is_womens_fashion is not None:
        query = query.filter(ShopModel.is_womens_fashion == is_womens_fashion)
    
    total = query.count()
    shops = query.offset((page - 1) * size).limit(size).all()
    
    return ShopList(
        shops=shops,
        total=total,
        page=page,
        size=size
    )

@router.get("/{shop_id}", response_model=Shop)
def get_shop(shop_id: int, db: Session = Depends(get_db)):
    """Get a specific shop by ID"""
    shop = db.query(ShopModel).filter(ShopModel.id == shop_id).first()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    return shop

@router.post("/", response_model=Shop)
def create_shop(shop: ShopCreate, db: Session = Depends(get_db)):
    """Create a new shop"""
    # Check if shop already exists
    existing_shop = db.query(ShopModel).filter(ShopModel.domain == shop.domain).first()
    if existing_shop:
        raise HTTPException(status_code=400, detail="Shop with this domain already exists")
    
    db_shop = ShopModel(**shop.dict())
    db.add(db_shop)
    db.commit()
    db.refresh(db_shop)
    return db_shop

@router.put("/{shop_id}", response_model=Shop)
def update_shop(shop_id: int, shop_update: ShopUpdate, db: Session = Depends(get_db)):
    """Update a shop"""
    db_shop = db.query(ShopModel).filter(ShopModel.id == shop_id).first()
    if not db_shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    
    update_data = shop_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_shop, field, value)
    
    db_shop.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_shop)
    return db_shop

@router.delete("/{shop_id}")
def delete_shop(shop_id: int, db: Session = Depends(get_db)):
    """Delete a shop"""
    db_shop = db.query(ShopModel).filter(ShopModel.id == shop_id).first()
    if not db_shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    
    db.delete(db_shop)
    db.commit()
    return {"message": "Shop deleted successfully"}

@router.post("/{shop_id}/verify-shopify")
def verify_shopify(shop_id: int, db: Session = Depends(get_db)):
    """Verify if a shop is built with Shopify"""
    db_shop = db.query(ShopModel).filter(ShopModel.id == shop_id).first()
    if not db_shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    
    detector = ShopifyDetector()
    result = detector.detect_shopify(db_shop.domain)
    
    # Update shop with results
    db_shop.is_shopify = result['is_shopify']
    db_shop.shopify_verified_at = datetime.utcnow()
    db_shop.last_checked = datetime.utcnow()
    
    db.commit()
    db.refresh(db_shop)
    
    return {
        "shop_id": shop_id,
        "verification_result": result,
        "updated_shop": db_shop
    }

@router.post("/{shop_id}/classify-fashion")
def classify_fashion(shop_id: int, db: Session = Depends(get_db)):
    """Classify if a shop sells women's fashion"""
    db_shop = db.query(ShopModel).filter(ShopModel.id == shop_id).first()
    if not db_shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    
    classifier = FashionClassifier()
    result = classifier.classify_fashion(db_shop.domain)
    
    # Update shop with results
    db_shop.is_womens_fashion = result['is_womens_fashion']
    db_shop.category_confidence = result['confidence']
    db_shop.category_verified_at = datetime.utcnow()
    db_shop.last_checked = datetime.utcnow()
    
    db.commit()
    db.refresh(db_shop)
    
    return {
        "shop_id": shop_id,
        "classification_result": result,
        "updated_shop": db_shop
    }

@router.get("/rankings/{region}", response_model=RegionRanking)
def get_region_rankings(
    region: Region,
    limit: int = Query(10, ge=1, le=50, description="Number of top shops to return"),
    db: Session = Depends(get_db)
):
    """Get top ranked shops for a specific region"""
    shops = db.query(ShopModel).filter(
        ShopModel.region == region,
        ShopModel.is_shopify == True,
        ShopModel.is_womens_fashion == True,
        ShopModel.status == ShopStatus.ACTIVE
    ).order_by(ShopModel.overall_score.desc()).limit(limit).all()
    
    rankings = []
    for i, shop in enumerate(shops, 1):
        rankings.append({
            "shop": shop,
            "rank": i,
            "previous_rank": None,  # TODO: Implement historical ranking
            "rank_change": None
        })
    
    return RegionRanking(
        region=region,
        rankings=rankings,
        last_updated=datetime.utcnow()
    ) 