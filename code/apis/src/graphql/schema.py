"""
GraphQL Schema Definition using Strawberry
Demonstrates GraphQL's flexible query capabilities
"""

import strawberry
from typing import List, Optional
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.database import db


# ============================================
# GRAPHQL TYPES
# ============================================

@strawberry.type
class Category:
    """Category type"""
    id: int
    name: str
    description: str
    
    @strawberry.field
    def products(self) -> List['Product']:
        """
        GRAPHQL ADVANTAGE: Nested field resolution
        Client can request category.products in single query
        """
        return [Product.from_db(p) for p in db.get_all_products(category_id=self.id)]


@strawberry.type
class Review:
    """Review type"""
    id: int
    product_id: int
    rating: int
    comment: str
    author: str
    created_at: str


@strawberry.type
class Inventory:
    """Inventory type"""
    product_id: int
    quantity: int
    warehouse: str
    last_updated: str


@strawberry.type
class Product:
    """Product type with nested resolvers"""
    id: int
    name: str
    description: str
    price: float
    category_id: int
    image_url: str
    created_at: str
    
    @strawberry.field
    def category(self) -> Optional[Category]:
        """
        GRAPHQL ADVANTAGE: Lazy loading
        Only fetched if client requests it
        """
        cat = db.get_category(self.category_id)
        if cat:
            return Category(
                id=cat.id,
                name=cat.name,
                description=cat.description
            )
        return None
    
    @strawberry.field
    def reviews(self) -> List[Review]:
        """
        GRAPHQL ADVANTAGE: Nested data in single request
        No N+1 problem - client decides what to fetch
        """
        reviews = db.get_product_reviews(self.id)
        return [Review(
            id=r.id,
            product_id=r.product_id,
            rating=r.rating,
            comment=r.comment,
            author=r.author,
            created_at=r.created_at
        ) for r in reviews]
    
    @strawberry.field
    def inventory(self) -> Optional[Inventory]:
        """
        GRAPHQL ADVANTAGE: Optional nested field
        Only fetched if requested
        """
        inv = db.get_product_inventory(self.id)
        if inv:
            return Inventory(
                product_id=inv.product_id,
                quantity=inv.quantity,
                warehouse=inv.warehouse,
                last_updated=inv.last_updated
            )
        return None
    
    @strawberry.field
    def average_rating(self) -> Optional[float]:
        """
        GRAPHQL ADVANTAGE: Computed fields
        Can add derived data without new endpoints
        """
        reviews = db.get_product_reviews(self.id)
        if not reviews:
            return None
        return sum(r.rating for r in reviews) / len(reviews)
    
    @classmethod
    def from_db(cls, product):
        """Convert database product to GraphQL type"""
        return cls(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            category_id=product.category_id,
            image_url=product.image_url,
            created_at=product.created_at
        )


# ============================================
# INPUT TYPES FOR MUTATIONS
# ============================================

@strawberry.input
class ProductInput:
    """Input type for creating/updating products"""
    name: str
    description: str
    price: float
    category_id: int
    image_url: Optional[str] = ""


@strawberry.input
class ReviewInput:
    """Input type for creating reviews"""
    product_id: int
    rating: int
    comment: str
    author: str


# ============================================
# QUERIES
# ============================================

@strawberry.type
class Query:
    """
    GraphQL Query root
    GRAPHQL ADVANTAGE: Single endpoint, flexible queries
    """
    
    @strawberry.field
    def products(
        self,
        category_id: Optional[int] = None,
        limit: Optional[int] = None
    ) -> List[Product]:
        """
        Get products with optional filtering
        
        GRAPHQL ADVANTAGE: Client can request exactly the fields needed
        Example: query { products { id name price } }
        """
        products = db.get_all_products(category_id=category_id, limit=limit)
        return [Product.from_db(p) for p in products]
    
    @strawberry.field
    def product(self, id: int) -> Optional[Product]:
        """
        Get single product by ID
        
        GRAPHQL ADVANTAGE: Can nest related data in single query
        Example: query { product(id: 1) { name category { name } reviews { rating } } }
        """
        product = db.get_product(id)
        if product:
            return Product.from_db(product)
        return None
    
    @strawberry.field
    def categories(self) -> List[Category]:
        """Get all categories"""
        return [Category(
            id=c.id,
            name=c.name,
            description=c.description
        ) for c in db.get_all_categories()]
    
    @strawberry.field
    def category(self, id: int) -> Optional[Category]:
        """Get single category"""
        cat = db.get_category(id)
        if cat:
            return Category(
                id=cat.id,
                name=cat.name,
                description=cat.description
            )
        return None
    
    @strawberry.field
    def search_products(self, query: str) -> List[Product]:
        """
        Search products by name or description
        
        GRAPHQL ADVANTAGE: Easy to add new query types
        No need for new REST endpoint
        """
        all_products = db.get_all_products()
        query_lower = query.lower()
        matching = [
            p for p in all_products
            if query_lower in p.name.lower() or query_lower in p.description.lower()
        ]
        return [Product.from_db(p) for p in matching]


# ============================================
# MUTATIONS
# ============================================

@strawberry.type
class Mutation:
    """
    GraphQL Mutation root
    GRAPHQL ADVANTAGE: Clear separation of queries vs mutations
    """
    
    @strawberry.mutation
    def create_product(self, input: ProductInput) -> Product:
        """Create a new product"""
        product = db.create_product(
            name=input.name,
            description=input.description,
            price=input.price,
            category_id=input.category_id,
            image_url=input.image_url or ""
        )
        return Product.from_db(product)
    
    @strawberry.mutation
    def update_product(self, id: int, input: ProductInput) -> Optional[Product]:
        """Update an existing product"""
        product = db.update_product(
            id,
            name=input.name,
            description=input.description,
            price=input.price,
            category_id=input.category_id,
            image_url=input.image_url
        )
        if product:
            return Product.from_db(product)
        return None
    
    @strawberry.mutation
    def delete_product(self, id: int) -> bool:
        """Delete a product"""
        return db.delete_product(id)
    
    @strawberry.mutation
    def create_review(self, input: ReviewInput) -> Review:
        """Create a new review"""
        review = db.create_review(
            product_id=input.product_id,
            rating=input.rating,
            comment=input.comment,
            author=input.author
        )
        return Review(
            id=review.id,
            product_id=review.product_id,
            rating=review.rating,
            comment=review.comment,
            author=review.author,
            created_at=review.created_at
        )


# ============================================
# SCHEMA
# ============================================

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation
)
