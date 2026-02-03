"""
GraphQL API Client Examples
Demonstrates GraphQL advantages: precise fetching, single requests, flexible queries
"""

import requests
import json
from typing import Dict, Any

GRAPHQL_URL = "http://localhost:4000/graphql"


def print_section(title: str):
    """Print formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def execute_query(query: str, variables: Dict[str, Any] = None, note: str = ""):
    """Execute GraphQL query and print response"""
    print(f"\n📝 Query:")
    print(query)
    
    if variables:
        print(f"\n📋 Variables:")
        print(json.dumps(variables, indent=2))
    
    if note:
        print(f"\n💡 {note}")
    
    response = requests.post(
        GRAPHQL_URL,
        json={"query": query, "variables": variables or {}}
    )
    
    print(f"\n📦 Response:")
    print(json.dumps(response.json(), indent=2))
    
    return response.json()


# ============================================
# EXAMPLE 1: Precise Field Selection
# ============================================

def example_precise_fetching():
    """
    GraphQL ADVANTAGE: Request exactly the fields you need
    No over-fetching!
    """
    print_section("EXAMPLE 1: Precise Field Selection (No Over-Fetching)")
    
    print("\n❓ Goal: Get only the NAME of product #1")
    print("✅ GraphQL Solution: Request only 'name' field")
    
    query = """
    query {
      product(id: 1) {
        name
      }
    }
    """
    
    execute_query(
        query,
        note="Notice: Response contains ONLY the 'name' field we requested!"
    )


# ============================================
# EXAMPLE 2: Nested Data in Single Request
# ============================================

def example_nested_data():
    """
    GraphQL ADVANTAGE: Get nested data in single request
    No under-fetching or N+1 problem!
    """
    print_section("EXAMPLE 2: Nested Data in Single Request")
    
    print("\n❓ Goal: Get product with reviews AND inventory")
    print("✅ GraphQL Solution: Single query with nested fields")
    
    query = """
    query {
      product(id: 1) {
        name
        price
        category {
          name
        }
        reviews {
          rating
          comment
          author
        }
        inventory {
          quantity
          warehouse
        }
      }
    }
    """
    
    execute_query(
        query,
        note="All data in ONE request! Product + category + reviews + inventory"
    )


# ============================================
# EXAMPLE 3: Multiple Products - No N+1
# ============================================

def example_no_n_plus_1():
    """
    GraphQL ADVANTAGE: No N+1 problem
    Get multiple products with reviews in single request
    """
    print_section("EXAMPLE 3: Multiple Products with Reviews (No N+1)")
    
    print("\n❓ Goal: Get 5 products with their reviews")
    print("✅ GraphQL Solution: Single query, no N+1 problem")
    
    query = """
    query {
      products(limit: 5) {
        id
        name
        price
        reviews {
          rating
          comment
        }
        averageRating
      }
    }
    """
    
    execute_query(
        query,
        note="All 5 products + their reviews in ONE request!"
    )


# ============================================
# EXAMPLE 4: Flexible Field Selection
# ============================================

def example_flexible_fields():
    """
    GraphQL ADVANTAGE: Different fields for different queries
    """
    print_section("EXAMPLE 4: Flexible Field Selection")
    
    print("\n❓ Goal: Get different fields for different use cases")
    print("✅ GraphQL Solution: Customize fields per query")
    
    # Query 1: Minimal fields for list view
    print("\n🔹 Use Case 1: Product list (minimal)")
    query1 = """
    query {
      products(limit: 3) {
        id
        name
        price
      }
    }
    """
    execute_query(query1, note="Minimal fields for list view")
    
    # Query 2: Detailed fields for product page
    print("\n🔹 Use Case 2: Product detail (comprehensive)")
    query2 = """
    query {
      product(id: 1) {
        id
        name
        description
        price
        category {
          name
          description
        }
        reviews {
          rating
          comment
          author
        }
        inventory {
          quantity
          warehouse
        }
        averageRating
      }
    }
    """
    execute_query(query2, note="All fields for detail view")


# ============================================
# EXAMPLE 5: Search with Custom Fields
# ============================================

def example_search():
    """
    GraphQL ADVANTAGE: Easy to add new query types
    """
    print_section("EXAMPLE 5: Search Products")
    
    print("\n❓ Goal: Search products and get specific fields")
    print("✅ GraphQL Solution: Custom query with field selection")
    
    query = """
    query {
      searchProducts(query: "book") {
        name
        price
        category {
          name
        }
      }
    }
    """
    
    execute_query(
        query,
        note="Search with custom field selection"
    )


# ============================================
# EXAMPLE 6: Mutations (Creating Data)
# ============================================

def example_mutation():
    """
    GraphQL: Creating resources with mutations
    """
    print_section("EXAMPLE 6: Creating Resources (GraphQL Mutation)")
    
    print("\n📤 Creating new product")
    
    mutation = """
    mutation CreateProduct($input: ProductInput!) {
      createProduct(input: $input) {
        id
        name
        price
        category {
          name
        }
      }
    }
    """
    
    variables = {
        "input": {
            "name": "GraphQL Test Product",
            "description": "Created via GraphQL mutation",
            "price": 149.99,
            "categoryId": 1,
            "imageUrl": "https://example.com/graphql-test.jpg"
        }
    }
    
    execute_query(
        mutation,
        variables,
        note="Mutation returns exactly the fields we specify"
    )


# ============================================
# EXAMPLE 7: Computed Fields
# ============================================

def example_computed_fields():
    """
    GraphQL ADVANTAGE: Computed fields without new endpoints
    """
    print_section("EXAMPLE 7: Computed Fields")
    
    print("\n❓ Goal: Get product with average rating")
    print("✅ GraphQL Solution: Computed field in schema")
    
    query = """
    query {
      product(id: 1) {
        name
        reviews {
          rating
        }
        averageRating
      }
    }
    """
    
    execute_query(
        query,
        note="'averageRating' is computed on the fly, no database field needed"
    )


# ============================================
# EXAMPLE 8: Aliases for Multiple Queries
# ============================================

def example_aliases():
    """
    GraphQL ADVANTAGE: Query same field multiple times with aliases
    """
    print_section("EXAMPLE 8: Aliases for Multiple Queries")
    
    print("\n❓ Goal: Get two different products in one request")
    print("✅ GraphQL Solution: Use aliases")
    
    query = """
    query {
      laptop: product(id: 1) {
        name
        price
      }
      book: product(id: 3) {
        name
        price
      }
    }
    """
    
    execute_query(
        query,
        note="Two products in one request using aliases"
    )


# ============================================
# MAIN
# ============================================

def main():
    """Run all GraphQL examples"""
    print("\n" + "🟢" * 35)
    print("  GRAPHQL API CLIENT EXAMPLES")
    print("  Demonstrating GraphQL Advantages")
    print("🟢" * 35)
    
    try:
        # Check if server is running
        requests.post(GRAPHQL_URL, json={"query": "{__typename}"}, timeout=2)
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: GraphQL API server not running!")
        print("   Start it with: python src/graphql/server.py")
        return
    
    example_precise_fetching()
    example_nested_data()
    example_no_n_plus_1()
    example_flexible_fields()
    example_search()
    example_computed_fields()
    example_aliases()
    example_mutation()
    
    print("\n" + "=" * 70)
    print("  ✅ GraphQL API Examples Complete")
    print("=" * 70)
    print("\n📊 GraphQL API Summary:")
    print("   ✅ Request exactly the fields you need (no over-fetching)")
    print("   ✅ Nested data in single request (no under-fetching)")
    print("   ✅ No N+1 problem")
    print("   ✅ Flexible field selection per query")
    print("   ✅ Strong typing and introspection")
    print("   ✅ Self-documenting (GraphiQL)")
    print("   ✅ Computed fields without new endpoints")
    print("=" * 70)


if __name__ == "__main__":
    main()
