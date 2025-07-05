#!/usr/bin/env python3
"""
TopShopE MVP 测试脚本
用于验证核心功能是否正常工作
"""

import requests
import time
import json
from typing import Dict, List

class TopShopETester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api/v1"
        
    def test_health(self) -> bool:
        """测试API健康状态"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            if response.status_code == 200:
                print("✅ API健康检查通过")
                return True
            else:
                print(f"❌ API健康检查失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ API健康检查异常: {e}")
            return False
    
    def test_create_shop(self) -> Dict:
        """测试创建商店"""
        shop_data = {
            "domain": "fashionnova.com",
            "name": "Fashion Nova",
            "region": "north_america",
            "description": "Trendy women's fashion store"
        }
        
        try:
            response = requests.post(f"{self.api_url}/shops", json=shop_data, timeout=10)
            if response.status_code == 200:
                shop = response.json()
                print(f"✅ 成功创建商店: {shop['domain']}")
                return shop
            else:
                print(f"❌ 创建商店失败: {response.status_code}")
                return {}
        except Exception as e:
            print(f"❌ 创建商店异常: {e}")
            return {}
    
    def test_verify_shopify(self, shop_id: int) -> bool:
        """测试Shopify验证"""
        try:
            response = requests.post(f"{self.api_url}/shops/{shop_id}/verify-shopify", timeout=30)
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Shopify验证完成: {result['verification_result']['is_shopify']}")
                return True
            else:
                print(f"❌ Shopify验证失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Shopify验证异常: {e}")
            return False
    
    def test_classify_fashion(self, shop_id: int) -> bool:
        """测试女装分类"""
        try:
            response = requests.post(f"{self.api_url}/shops/{shop_id}/classify-fashion", timeout=30)
            if response.status_code == 200:
                result = response.json()
                print(f"✅ 女装分类完成: {result['classification_result']['is_womens_fashion']}")
                return True
            else:
                print(f"❌ 女装分类失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 女装分类异常: {e}")
            return False
    
    def test_get_shops(self) -> bool:
        """测试获取商店列表"""
        try:
            response = requests.get(f"{self.api_url}/shops", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 获取商店列表成功: {len(data['shops'])} 个商店")
                return True
            else:
                print(f"❌ 获取商店列表失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 获取商店列表异常: {e}")
            return False
    
    def test_get_rankings(self) -> bool:
        """测试获取排名"""
        regions = ["north_america", "europe", "middle_east"]
        
        for region in regions:
            try:
                response = requests.get(f"{self.api_url}/shops/rankings/{region}", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ 获取 {region} 排名成功: {len(data['rankings'])} 个排名")
                else:
                    print(f"❌ 获取 {region} 排名失败: {response.status_code}")
            except Exception as e:
                print(f"❌ 获取 {region} 排名异常: {e}")
        
        return True
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始 TopShopE MVP 测试...")
        print("=" * 50)
        
        # 测试API健康状态
        if not self.test_health():
            print("❌ API不可用，停止测试")
            return False
        
        # 测试创建商店
        shop = self.test_create_shop()
        if not shop:
            print("❌ 创建商店失败，停止测试")
            return False
        
        shop_id = shop['id']
        
        # 测试Shopify验证
        self.test_verify_shopify(shop_id)
        
        # 测试女装分类
        self.test_classify_fashion(shop_id)
        
        # 测试获取商店列表
        self.test_get_shops()
        
        # 测试获取排名
        self.test_get_rankings()
        
        print("=" * 50)
        print("🎉 MVP测试完成！")
        return True

def main():
    """主函数"""
    print("TopShopE MVP 测试工具")
    print("请确保后端服务已启动在 http://localhost:8000")
    print()
    
    tester = TopShopETester()
    tester.run_all_tests()

if __name__ == "__main__":
    main() 