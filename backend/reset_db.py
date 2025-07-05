#!/usr/bin/env python3
"""
Database reset script
This script will drop and recreate all tables, then add sample data
Use this for development environment resets
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import recreate_tables, SessionLocal
from app.models.shop import Shop, Region, ShopStatus
from datetime import datetime

def reset_db():
    """Reset database with sample data"""
    print("Dropping and recreating tables...")
    recreate_tables()
    
    print("Adding sample data...")
    db = SessionLocal()
    
    try:
        # Sample shops data
        sample_shops = [
            {
                "domain": "fashionista-europe.com",
                "name": "Fashionista Europe",
                "region": Region.EUROPE,
                "is_shopify": True,
                "is_womens_fashion": True,
                "category_confidence": 0.95,
                "traffic_rank": 15000,
                "monthly_visits": 50000,
                "social_media_score": 8.5,
                "seo_score": 7.8,
                "overall_score": 8.2,
                "status": ShopStatus.ACTIVE,
                "description": "Premium women's fashion boutique in Europe"
            },
            {
                "domain": "style-middle-east.com",
                "name": "Style Middle East",
                "region": Region.MIDDLE_EAST,
                "is_shopify": True,
                "is_womens_fashion": True,
                "category_confidence": 0.92,
                "traffic_rank": 25000,
                "monthly_visits": 35000,
                "social_media_score": 7.9,
                "seo_score": 8.1,
                "overall_score": 8.0,
                "status": ShopStatus.ACTIVE,
                "description": "Luxury women's fashion in the Middle East"
            },
            {
                "domain": "north-america-fashion.com",
                "name": "North America Fashion",
                "region": Region.NORTH_AMERICA,
                "is_shopify": True,
                "is_womens_fashion": True,
                "category_confidence": 0.88,
                "traffic_rank": 12000,
                "monthly_visits": 75000,
                "social_media_score": 9.1,
                "seo_score": 8.5,
                "overall_score": 8.8,
                "status": ShopStatus.ACTIVE,
                "description": "Trendy women's fashion in North America"
            },
            {
                "domain": "europe-luxury.com",
                "name": "Europe Luxury Boutique",
                "region": Region.EUROPE,
                "is_shopify": True,
                "is_womens_fashion": True,
                "category_confidence": 0.97,
                "traffic_rank": 8000,
                "monthly_visits": 120000,
                "social_media_score": 9.3,
                "seo_score": 8.9,
                "overall_score": 9.1,
                "status": ShopStatus.ACTIVE,
                "description": "High-end luxury fashion in Europe"
            },
            {
                "domain": "middle-east-elegance.com",
                "name": "Middle East Elegance",
                "region": Region.MIDDLE_EAST,
                "is_shopify": True,
                "is_womens_fashion": True,
                "category_confidence": 0.94,
                "traffic_rank": 18000,
                "monthly_visits": 45000,
                "social_media_score": 8.2,
                "seo_score": 7.9,
                "overall_score": 8.1,
                "status": ShopStatus.ACTIVE,
                "description": "Elegant women's fashion in the Middle East"
            }
        ]
        
        for shop_data in sample_shops:
            shop = Shop(**shop_data)
            db.add(shop)
        
        db.commit()
        print(f"Successfully added {len(sample_shops)} sample shops")
        
    except Exception as e:
        print(f"Error adding sample data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("Resetting database...")
    reset_db()
    print("Database reset completed!") 