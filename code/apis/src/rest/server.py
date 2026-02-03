"""
REST API Server using Flask
Demonstrates traditional RESTful API design with multiple endpoints
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.database import db

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Helper function to convert dataclass to dict
def to_dict(obj):
    """Convert dataclass instance to dictionary"""
    if hasattr(obj, '__dataclass_fields__'):
        return {k: v for k, v in obj.__dict__.items()}
    return obj


# ============================================
# PRODUCT ENDPOINTS
# ============================================

@app.route('/api/products', methods=['GET'])
def get_products():
    """
    GET /api/products
    Query params: category_id, limit
    
    REST CHARACTERISTIC: Returns full product objects (potential over-fetching)
    """
    category_id = request.args.get('category_id', type=int)
    limit = request.args.get('limit', type=int)
    
    products = db.get_all_products(category_id=category_id, limit=limit)
    
    return jsonify({
        'data': [to_dict(p) for p in products],
        'count': len(products),
        'note': 'REST: Returns all product fields even if you only need some'
    })


@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """
    GET /api/products/:id
    
    REST CHARACTERISTIC: Returns complete product object
    Client cannot specify which fields to return
    """
    product = db.get_product(product_id)
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    return jsonify({
        'data': to_dict(product),
        'note': 'REST: All fields returned, no field selection'
    })


@app.route('/api/products', methods=['POST'])
def create_product():
    """
    POST /api/products
    Body: {name, description, price, category_id, image_url}
    """
    data = request.json
    
    try:
        product = db.create_product(
            name=data['name'],
            description=data['description'],
            price=data['price'],
            category_id=data['category_id'],
            image_url=data.get('image_url', '')
        )
        return jsonify({
            'data': to_dict(product),
            'message': 'Product created successfully'
        }), 201
    except KeyError as e:
        return jsonify({'error': f'Missing required field: {e}'}), 400


@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """
    PUT /api/products/:id
    Body: {name?, description?, price?, category_id?, image_url?}
    """
    data = request.json
    product = db.update_product(product_id, **data)
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    return jsonify({
        'data': to_dict(product),
        'message': 'Product updated successfully'
    })


@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """
    DELETE /api/products/:id
    """
    success = db.delete_product(product_id)
    
    if not success:
        return jsonify({'error': 'Product not found'}), 404
    
    return jsonify({
        'message': 'Product deleted successfully',
        'deleted_id': product_id
    })


# ============================================
# PRODUCT REVIEWS ENDPOINTS
# ============================================

@app.route('/api/products/<int:product_id>/reviews', methods=['GET'])
def get_product_reviews(product_id):
    """
    GET /api/products/:id/reviews
    
    REST CHARACTERISTIC: Separate endpoint for nested resource
    Requires additional HTTP request to get reviews
    """
    product = db.get_product(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    reviews = db.get_product_reviews(product_id)
    
    return jsonify({
        'data': [to_dict(r) for r in reviews],
        'count': len(reviews),
        'note': 'REST: Separate request needed for reviews (N+1 problem)'
    })


@app.route('/api/products/<int:product_id>/reviews', methods=['POST'])
def create_review(product_id):
    """
    POST /api/products/:id/reviews
    Body: {rating, comment, author}
    """
    product = db.get_product(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    data = request.json
    
    try:
        review = db.create_review(
            product_id=product_id,
            rating=data['rating'],
            comment=data['comment'],
            author=data['author']
        )
        return jsonify({
            'data': to_dict(review),
            'message': 'Review created successfully'
        }), 201
    except KeyError as e:
        return jsonify({'error': f'Missing required field: {e}'}), 400


# ============================================
# PRODUCT INVENTORY ENDPOINTS
# ============================================

@app.route('/api/products/<int:product_id>/inventory', methods=['GET'])
def get_product_inventory(product_id):
    """
    GET /api/products/:id/inventory
    
    REST CHARACTERISTIC: Another separate endpoint for inventory
    Yet another HTTP request needed
    """
    product = db.get_product(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    inventory = db.get_product_inventory(product_id)
    
    if not inventory:
        return jsonify({'error': 'Inventory not found'}), 404
    
    return jsonify({
        'data': to_dict(inventory),
        'note': 'REST: Third request needed for inventory (under-fetching)'
    })


# ============================================
# CATEGORY ENDPOINTS
# ============================================

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """GET /api/categories"""
    categories = db.get_all_categories()
    return jsonify({
        'data': [to_dict(c) for c in categories],
        'count': len(categories)
    })


@app.route('/api/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """GET /api/categories/:id"""
    category = db.get_category(category_id)
    
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    
    return jsonify({'data': to_dict(category)})


@app.route('/api/categories/<int:category_id>/products', methods=['GET'])
def get_category_products(category_id):
    """
    GET /api/categories/:id/products
    
    REST CHARACTERISTIC: Nested resource requires separate endpoint
    """
    category = db.get_category(category_id)
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    
    products = db.get_all_products(category_id=category_id)
    
    return jsonify({
        'data': [to_dict(p) for p in products],
        'count': len(products),
        'category': to_dict(category)
    })


# ============================================
# API DOCUMENTATION ENDPOINT
# ============================================

@app.route('/api', methods=['GET'])
def api_info():
    """API documentation and available endpoints"""
    return jsonify({
        'api': 'REST API Demo',
        'version': '1.0',
        'characteristics': [
            'Multiple endpoints for different resources',
            'Fixed response structure (over-fetching)',
            'Multiple requests for nested data (under-fetching)',
            'HTTP verbs for operations (GET, POST, PUT, DELETE)',
            'Resource-based URLs'
        ],
        'endpoints': {
            'products': {
                'GET /api/products': 'List all products (query: category_id, limit)',
                'GET /api/products/:id': 'Get single product',
                'POST /api/products': 'Create product',
                'PUT /api/products/:id': 'Update product',
                'DELETE /api/products/:id': 'Delete product',
                'GET /api/products/:id/reviews': 'Get product reviews',
                'POST /api/products/:id/reviews': 'Create review',
                'GET /api/products/:id/inventory': 'Get product inventory'
            },
            'categories': {
                'GET /api/categories': 'List all categories',
                'GET /api/categories/:id': 'Get single category',
                'GET /api/categories/:id/products': 'Get products in category'
            }
        },
        'examples': {
            'over_fetching': 'GET /api/products/1 returns ALL fields even if you only need name',
            'under_fetching': 'Need 3 requests: product + reviews + inventory',
            'n_plus_1': 'Get 10 products + their reviews = 11 requests'
        }
    })


# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


# ============================================
# MAIN
# ============================================

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 REST API Server Starting")
    print("=" * 60)
    print(f"📍 Server: http://localhost:3000")
    print(f"📖 API Docs: http://localhost:3000/api")
    print(f"🔍 Example: http://localhost:3000/api/products")
    print("=" * 60)
    print("\n⚠️  REST API Characteristics:")
    print("   • Multiple endpoints for different resources")
    print("   • Over-fetching: Returns all fields")
    print("   • Under-fetching: Multiple requests for nested data")
    print("   • N+1 problem: Separate requests for relations")
    print("=" * 60)
    print()
    
    app.run(host='0.0.0.0', port=3000, debug=True)
