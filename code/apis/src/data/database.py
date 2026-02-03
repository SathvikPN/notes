"""
Shared in-memory database for both REST and GraphQL APIs.
This demonstrates that both APIs can work with the same data source.
"""

from typing import List, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Category:
    """Product category"""
    id: int
    name: str
    description: str


@dataclass
class Review:
    """Product review"""
    id: int
    product_id: int
    rating: int  # 1-5
    comment: str
    author: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class Inventory:
    """Product inventory information"""
    product_id: int
    quantity: int
    warehouse: str
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class Product:
    """Main product entity"""
    id: int
    name: str
    description: str
    price: float
    category_id: int
    image_url: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


# In-memory data store
class Database:
    """Simulated database with sample data"""
    
    def __init__(self):
        self.categories = [
            Category(1, "Electronics", "Electronic devices and gadgets"),
            Category(2, "Books", "Physical and digital books"),
            Category(3, "Clothing", "Apparel and accessories"),
            Category(4, "Home & Garden", "Home improvement and garden supplies"),
        ]
        
        self.products = [
            Product(1, "Laptop Pro 15", "High-performance laptop with 16GB RAM", 1299.99, 1, "https://example.com/laptop.jpg"),
            Product(2, "Wireless Mouse", "Ergonomic wireless mouse with USB receiver", 29.99, 1, "https://example.com/mouse.jpg"),
            Product(3, "Python Programming", "Comprehensive guide to Python programming", 49.99, 2, "https://example.com/python-book.jpg"),
            Product(4, "Mechanical Keyboard", "RGB mechanical keyboard with blue switches", 89.99, 1, "https://example.com/keyboard.jpg"),
            Product(5, "Cotton T-Shirt", "100% organic cotton t-shirt", 19.99, 3, "https://example.com/tshirt.jpg"),
            Product(6, "Garden Tools Set", "Complete set of essential garden tools", 79.99, 4, "https://example.com/tools.jpg"),
            Product(7, "USB-C Hub", "7-in-1 USB-C hub with HDMI and card reader", 39.99, 1, "https://example.com/hub.jpg"),
            Product(8, "Design Patterns Book", "Classic software design patterns", 54.99, 2, "https://example.com/design-book.jpg"),
        ]
        
        self.reviews = [
            Review(1, 1, 5, "Excellent laptop! Fast and reliable.", "Alice"),
            Review(2, 1, 4, "Great performance but a bit pricey.", "Bob"),
            Review(3, 2, 5, "Perfect mouse, very comfortable.", "Charlie"),
            Review(4, 3, 5, "Best Python book I've read!", "Diana"),
            Review(5, 3, 4, "Very comprehensive, good for beginners.", "Eve"),
            Review(6, 4, 5, "Love the tactile feedback!", "Frank"),
            Review(7, 5, 3, "Good quality but runs small.", "Grace"),
            Review(8, 6, 4, "Solid tools, good value.", "Henry"),
        ]
        
        self.inventory = [
            Inventory(1, 15, "Warehouse A"),
            Inventory(2, 50, "Warehouse B"),
            Inventory(3, 30, "Warehouse A"),
            Inventory(4, 25, "Warehouse B"),
            Inventory(5, 100, "Warehouse C"),
            Inventory(6, 20, "Warehouse A"),
            Inventory(7, 40, "Warehouse B"),
            Inventory(8, 35, "Warehouse A"),
        ]
        
        # Auto-increment IDs
        self.next_product_id = 9
        self.next_review_id = 9
    
    # Product methods
    def get_all_products(self, category_id: Optional[int] = None, limit: Optional[int] = None) -> List[Product]:
        """Get all products, optionally filtered by category"""
        products = self.products
        if category_id:
            products = [p for p in products if p.category_id == category_id]
        if limit:
            products = products[:limit]
        return products
    
    def get_product(self, product_id: int) -> Optional[Product]:
        """Get a single product by ID"""
        return next((p for p in self.products if p.id == product_id), None)
    
    def create_product(self, name: str, description: str, price: float, category_id: int, image_url: str = "") -> Product:
        """Create a new product"""
        product = Product(
            id=self.next_product_id,
            name=name,
            description=description,
            price=price,
            category_id=category_id,
            image_url=image_url
        )
        self.products.append(product)
        self.next_product_id += 1
        return product
    
    def update_product(self, product_id: int, **kwargs) -> Optional[Product]:
        """Update a product"""
        product = self.get_product(product_id)
        if product:
            for key, value in kwargs.items():
                if hasattr(product, key) and value is not None:
                    setattr(product, key, value)
        return product
    
    def delete_product(self, product_id: int) -> bool:
        """Delete a product"""
        product = self.get_product(product_id)
        if product:
            self.products.remove(product)
            # Also remove related reviews and inventory
            self.reviews = [r for r in self.reviews if r.product_id != product_id]
            self.inventory = [i for i in self.inventory if i.product_id != product_id]
            return True
        return False
    
    # Category methods
    def get_all_categories(self) -> List[Category]:
        """Get all categories"""
        return self.categories
    
    def get_category(self, category_id: int) -> Optional[Category]:
        """Get a single category by ID"""
        return next((c for c in self.categories if c.id == category_id), None)
    
    # Review methods
    def get_product_reviews(self, product_id: int) -> List[Review]:
        """Get all reviews for a product"""
        return [r for r in self.reviews if r.product_id == product_id]
    
    def create_review(self, product_id: int, rating: int, comment: str, author: str) -> Review:
        """Create a new review"""
        review = Review(
            id=self.next_review_id,
            product_id=product_id,
            rating=rating,
            comment=comment,
            author=author
        )
        self.reviews.append(review)
        self.next_review_id += 1
        return review
    
    # Inventory methods
    def get_product_inventory(self, product_id: int) -> Optional[Inventory]:
        """Get inventory for a product"""
        return next((i for i in self.inventory if i.product_id == product_id), None)
    
    def update_inventory(self, product_id: int, quantity: int, warehouse: str = None) -> Optional[Inventory]:
        """Update product inventory"""
        inventory = self.get_product_inventory(product_id)
        if inventory:
            inventory.quantity = quantity
            if warehouse:
                inventory.warehouse = warehouse
            inventory.last_updated = datetime.now().isoformat()
        else:
            inventory = Inventory(product_id, quantity, warehouse or "Warehouse A")
            self.inventory.append(inventory)
        return inventory


# Singleton instance
db = Database()
