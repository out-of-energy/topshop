import axios from 'axios';
import { Shop, ShopCreate, ShopUpdate, ShopList, RegionRanking, Region } from '../types/shop';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const API_URL = `${API_BASE_URL}/api/v1`;

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Shops API
export const shopsApi = {
  // Get shops with filters
  getShops: async (params?: {
    region?: Region;
    is_shopify?: boolean;
    is_womens_fashion?: boolean;
    page?: number;
    size?: number;
  }): Promise<ShopList> => {
    const response = await api.get('/shops', { params });
    return response.data;
  },

  // Get a specific shop
  getShop: async (id: number): Promise<Shop> => {
    const response = await api.get(`/shops/${id}`);
    return response.data;
  },

  // Create a new shop
  createShop: async (shop: ShopCreate): Promise<Shop> => {
    const response = await api.post('/shops', shop);
    return response.data;
  },

  // Update a shop
  updateShop: async (id: number, shop: ShopUpdate): Promise<Shop> => {
    const response = await api.put(`/shops/${id}`, shop);
    return response.data;
  },

  // Delete a shop
  deleteShop: async (id: number): Promise<void> => {
    await api.delete(`/shops/${id}`);
  },

  // Verify Shopify
  verifyShopify: async (id: number): Promise<any> => {
    const response = await api.post(`/shops/${id}/verify-shopify`);
    return response.data;
  },

  // Classify fashion
  classifyFashion: async (id: number): Promise<any> => {
    const response = await api.post(`/shops/${id}/classify-fashion`);
    return response.data;
  },

  // Get region rankings
  getRegionRankings: async (region: Region, limit: number = 10): Promise<RegionRanking> => {
    const response = await api.get(`/shops/rankings/${region}`, {
      params: { limit }
    });
    return response.data;
  },
};

// Health check
export const healthApi = {
  checkHealth: async (): Promise<any> => {
    const response = await api.get('/health');
    return response.data;
  },
};

export default api; 