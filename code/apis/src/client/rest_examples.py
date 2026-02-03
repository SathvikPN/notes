"""
REST API Client Examples
Demonstrates REST API characteristics: multiple requests, over-fetching, under-fetching
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:3000/api"


def print_section(title: str):
    """Print formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_response(response: requests.Response, note: str = ""):
    """Print formatted API response"""
    print(f"\n📍 {response.request.method} {response.url}")
    print(f"📊 Status: {response.status_code}")
    if note:
        print(f"💡 {note}")
    print(f"\n📦 Response:")
    print(json.dumps(response.json(), indent=2))


# ============================================
# EXAMPLE 1: Over-Fetching
# ============================================

def example_overfetching():
    """
    REST PROBLEM: Over-fetching
    We only need product name, but REST returns ALL fields
    """
    print_section("EXAMPLE 1: Over-Fetching Problem")
    
    print("\n❓ Goal: Get only the NAME of product #1")
    print("⚠️  REST Problem: Returns ALL fields (over-fetching)")
    
    response = requests.get(f"{BASE_URL}/products/1")
    print_response(
        response,
        "Notice: We got id, description, price, category_id, image_url, created_at - but we only needed 'name'!"
    )


# ============================================
# EXAMPLE 2: Under-Fetching (N+1 Problem)
# ============================================

def example_underfetching():
    """
    REST PROBLEM: Under-fetching / N+1 Problem
    Need multiple requests to get product + reviews + inventory
    """
    print_section("EXAMPLE 2: Under-Fetching / N+1 Problem")
    
    print("\n❓ Goal: Get product with its reviews AND inventory")
    print("⚠️  REST Problem: Requires 3 separate HTTP requests")
    
    # Request 1: Get product
    print("\n🔹 Request 1/3: Get product")
    response1 = requests.get(f"{BASE_URL}/products/1")
    print_response(response1, "Got product, but no reviews or inventory")
    
    # Request 2: Get reviews
    print("\n🔹 Request 2/3: Get product reviews")
    response2 = requests.get(f"{BASE_URL}/products/1/reviews")
    print_response(response2, "Got reviews in separate request")
    
    # Request 3: Get inventory
    print("\n🔹 Request 3/3: Get product inventory")
    response3 = requests.get(f"{BASE_URL}/products/1/inventory")
    print_response(response3, "Got inventory in third request")
    
    print("\n💭 Summary: 3 HTTP requests needed for related data")


# ============================================
# EXAMPLE 3: Multiple Products with Relations
# ============================================

def example_n_plus_1():
    """
    REST PROBLEM: Severe N+1 problem
    Getting 5 products + their reviews = 6 requests!
    """
    print_section("EXAMPLE 3: Severe N+1 Problem")
    
    print("\n❓ Goal: Get 5 products with their reviews")
    print("⚠️  REST Problem: 1 request for products + N requests for reviews")
    
    # Request 1: Get products
    print("\n🔹 Request 1: Get products")
    response = requests.get(f"{BASE_URL}/products?limit=5")
    products = response.json()['data']
    print(f"📦 Got {len(products)} products")
    
    # Requests 2-6: Get reviews for each product
    print(f"\n🔹 Requests 2-6: Get reviews for each product")
    for i, product in enumerate(products[:5], 1):
        response = requests.get(f"{BASE_URL}/products/{product['id']}/reviews")
        reviews = response.json()['data']
        print(f"   Product {product['id']} ({product['name']}): {len(reviews)} reviews")
    
    print(f"\n💭 Summary: 6 total HTTP requests (1 + 5)")
    print("   With 100 products, this would be 101 requests!")


# ============================================
# EXAMPLE 4: Fixed Response Structure
# ============================================

def example_fixed_structure():
    """
    REST CHARACTERISTIC: Fixed response structure
    Can't customize which fields to return
    """
    print_section("EXAMPLE 4: Fixed Response Structure")
    
    print("\n❓ Goal: Get different fields for different products")
    print("   Product 1: Only name and price")
    print("   Product 2: Only name and category")
    print("⚠️  REST Problem: Both return same fields")
    
    response1 = requests.get(f"{BASE_URL}/products/1")
    response2 = requests.get(f"{BASE_URL}/products/2")
    
    print("\n📦 Product 1 response (wanted: name, price):")
    print(f"   Got: {list(response1.json()['data'].keys())}")
    
    print("\n📦 Product 2 response (wanted: name, category):")
    print(f"   Got: {list(response2.json()['data'].keys())}")
    
    print("\n💭 Both return identical field structure")


# ============================================
# EXAMPLE 5: Creating Resources
# ============================================

def example_create_product():
    """
    REST: Creating resources with POST
    """
    print_section("EXAMPLE 5: Creating Resources (REST POST)")
    
    new_product = {
        "name": "REST Test Product",
        "description": "Created via REST API",
        "price": 99.99,
        "category_id": 1,
        "image_url": "https://example.com/test.jpg"
    }
    
    print("\n📤 Creating new product:")
    print(json.dumps(new_product, indent=2))
    
    response = requests.post(f"{BASE_URL}/products", json=new_product)
    print_response(response, "Product created successfully")


# ============================================
# EXAMPLE 6: Listing with Filters
# ============================================

def example_filtering():
    """
    REST: Query parameters for filtering
    """
    print_section("EXAMPLE 6: Filtering with Query Parameters")
    
    print("\n🔹 Get products in category 1 (Electronics)")
    response = requests.get(f"{BASE_URL}/products?category_id=1&limit=3")
    products = response.json()['data']
    print(f"📦 Found {len(products)} products:")
    for p in products:
        print(f"   - {p['name']} (${p['price']})")


# ============================================
# MAIN
# ============================================

def main():
    """Run all REST API examples"""
    print("\n" + "🔴" * 35)
    print("  REST API CLIENT EXAMPLES")
    print("  Demonstrating REST Characteristics & Problems")
    print("🔴" * 35)
    
    try:
        # Check if server is running
        requests.get(f"{BASE_URL}", timeout=2)
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: REST API server not running!")
        print("   Start it with: python src/rest/server.py")
        return
    
    example_overfetching()
    example_underfetching()
    example_n_plus_1()
    example_fixed_structure()
    example_filtering()
    example_create_product()
    
    print("\n" + "=" * 70)
    print("  ✅ REST API Examples Complete")
    print("=" * 70)
    print("\n📊 REST API Summary:")
    print("   ✅ Simple and well-understood")
    print("   ✅ Good for simple CRUD operations")
    print("   ❌ Over-fetching (returns all fields)")
    print("   ❌ Under-fetching (multiple requests for nested data)")
    print("   ❌ N+1 problem (many requests for related data)")
    print("   ❌ Fixed response structure")
    print("=" * 70)


if __name__ == "__main__":
    main()
