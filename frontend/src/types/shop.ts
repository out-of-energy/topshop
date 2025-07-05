export enum Region {
  NORTH_AMERICA = "north_america",
  EUROPE = "europe",
  MIDDLE_EAST = "middle_east"
}

export enum ShopStatus {
  ACTIVE = "active",
  INACTIVE = "inactive",
  ERROR = "error"
}

export interface Shop {
  id: number;
  domain: string;
  name?: string;
  region: Region;
  description?: string;
  is_shopify: boolean;
  shopify_verified_at?: string;
  is_womens_fashion: boolean;
  category_confidence: number;
  category_verified_at?: string;
  traffic_rank?: number;
  monthly_visits?: number;
  social_media_score: number;
  seo_score: number;
  overall_score: number;
  status: ShopStatus;
  last_checked: string;
  created_at: string;
  updated_at: string;
  logo_url?: string;
  screenshot_url?: string;
}

export interface ShopCreate {
  domain: string;
  name?: string;
  region: Region;
  description?: string;
}

export interface ShopUpdate {
  name?: string;
  description?: string;
  is_shopify?: boolean;
  is_womens_fashion?: boolean;
  category_confidence?: number;
  traffic_rank?: number;
  monthly_visits?: number;
  social_media_score?: number;
  seo_score?: number;
  overall_score?: number;
  status?: ShopStatus;
}

export interface ShopList {
  shops: Shop[];
  total: number;
  page: number;
  size: number;
}

export interface ShopRanking {
  shop: Shop;
  rank: number;
  previous_rank?: number;
  rank_change?: number;
}

export interface RegionRanking {
  region: Region;
  rankings: ShopRanking[];
  last_updated: string;
} 