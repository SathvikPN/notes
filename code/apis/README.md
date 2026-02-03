# REST vs GraphQL API - Comprehensive Comparison Demo

A practical, side-by-side comparison of REST and GraphQL APIs using the same data entity (product catalog) to demonstrate real-world advantages and drawbacks of each approach.

## 🎯 What You'll Learn

- **Fundamental differences** between REST and GraphQL
- **When to use** each API style
- **Performance implications** of over-fetching and under-fetching
- **Design trade-offs** and decision criteria
- **Practical examples** of common scenarios

---

## 📊 Quick Comparison

| Feature | REST | GraphQL |
|---------|------|---------|
| **Endpoints** | Multiple (`/products`, `/reviews`, etc.) | Single (`/graphql`) |
| **Data Fetching** | Fixed structure (over-fetching) | Flexible fields (precise) |
| **Nested Data** | Multiple requests (under-fetching) | Single request |
| **N+1 Problem** | Yes (separate requests for relations) | No (nested queries) |
| **Versioning** | URL versioning (`/v1`, `/v2`) | Schema evolution (deprecation) |
| **Caching** | HTTP caching (easy) | Custom caching (complex) |
| **Learning Curve** | Low | Medium-High |
| **Tooling** | Mature (Swagger, Postman) | Growing (GraphiQL, Apollo) |

---

## 🏗️ Project Structure

```
apis/
├── README.md                      # This file
├── DESIGN_CHOICES.md             # Decision criteria guide
├── requirements.txt              # Python dependencies
├── src/
│   ├── data/
│   │   └── database.py           # Shared in-memory database
│   ├── rest/
│   │   └── server.py             # Flask REST API (port 3000)
│   ├── graphql/
│   │   ├── server.py             # GraphQL server (port 4000)
│   │   └── schema.py             # GraphQL schema & resolvers
│   └── client/
│       ├── rest_examples.py      # REST client examples
│       ├── graphql_examples.py   # GraphQL client examples
│       └── test_both.py          # Run both for comparison
└── examples/
    ├── rest-requests.http        # REST API examples
    └── graphql-queries.graphql   # GraphQL query examples
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Navigate to project directory
cd /Users/sathvikpn/workspace/prep/code/apis

# Install dependencies
pip install -r requirements.txt
```

### Running the Servers

**Terminal 1: Start REST API**
```bash
python src/rest/server.py
# Server runs on http://localhost:3000
# API docs: http://localhost:3000/api
```

**Terminal 2: Start GraphQL API**
```bash
python src/graphql/server.py
# Server runs on http://localhost:4000
# GraphiQL IDE: http://localhost:4000
```

### Testing the APIs

**Terminal 3: Run Examples**
```bash
# Run REST examples
python src/client/rest_examples.py

# Run GraphQL examples
python src/client/graphql_examples.py

# Run both for comparison
python src/client/test_both.py
```

---

## 📖 Understanding the Differences

### 1. Over-Fetching vs Precise Fetching

**REST Problem: Over-Fetching**
```bash
# Goal: Get only product name
curl http://localhost:3000/api/products/1

# Returns: id, name, description, price, category_id, image_url, created_at
# We only needed 'name' but got everything!
```

**GraphQL Solution: Precise Fetching**
```graphql
# Request only what you need
query {
  product(id: 1) {
    name
  }
}

# Returns: Only { "name": "Laptop Pro 15" }
```

---

### 2. Under-Fetching vs Nested Queries

**REST Problem: Under-Fetching (N+1)**
```bash
# Goal: Get product with reviews and inventory
# Requires 3 separate HTTP requests:

curl http://localhost:3000/api/products/1          # Request 1
curl http://localhost:3000/api/products/1/reviews  # Request 2
curl http://localhost:3000/api/products/1/inventory # Request 3
```

**GraphQL Solution: Nested Query**
```graphql
# Single request for all data
query {
  product(id: 1) {
    name
    price
    reviews {
      rating
      comment
    }
    inventory {
      quantity
    }
  }
}
```

---

### 3. N+1 Problem

**REST: Severe N+1 Problem**
```bash
# Get 10 products with their reviews
# = 1 request for products + 10 requests for reviews = 11 total requests!

curl http://localhost:3000/api/products?limit=10
# Then for each product:
curl http://localhost:3000/api/products/1/reviews
curl http://localhost:3000/api/products/2/reviews
# ... 10 more requests
```

**GraphQL: No N+1 Problem**
```graphql
# Single request for all products and their reviews
query {
  products(limit: 10) {
    name
    reviews {
      rating
      comment
    }
  }
}
```

---

## ✅ REST API Advantages

### 1. **Simplicity**
- Easy to understand and implement
- Well-established patterns
- Familiar to most developers

### 2. **HTTP Caching**
```bash
# Automatic HTTP caching with headers
GET /api/products/1
Cache-Control: max-age=3600
ETag: "abc123"
```

### 3. **Stateless**
- Each request is independent
- Easy to scale horizontally
- Simple load balancing

### 4. **Mature Tooling**
- Swagger/OpenAPI for documentation
- Postman for testing
- Wide ecosystem support

### 5. **Good for Simple CRUD**
```bash
GET    /api/products      # List
POST   /api/products      # Create
GET    /api/products/:id  # Read
PUT    /api/products/:id  # Update
DELETE /api/products/:id  # Delete
```

---

## ❌ REST API Disadvantages

### 1. **Over-Fetching**
- Returns all fields even if you need only one
- Wastes bandwidth
- Slower on mobile networks

### 2. **Under-Fetching**
- Multiple requests for related data
- Increased latency
- More complex client code

### 3. **N+1 Problem**
- Exponential requests for nested data
- Performance bottleneck
- Difficult to optimize

### 4. **Versioning Challenges**
```bash
/api/v1/products  # Old version
/api/v2/products  # New version
# Maintaining multiple versions is complex
```

### 5. **Fixed Response Structure**
- Can't customize fields per request
- Mobile and web get same data
- No flexibility

---

## ✅ GraphQL Advantages

### 1. **Precise Data Fetching**
```graphql
# Request exactly what you need
query {
  product(id: 1) {
    name
    price
  }
}
```

### 2. **Single Request for Nested Data**
```graphql
# Product + category + reviews + inventory in ONE request
query {
  product(id: 1) {
    name
    category { name }
    reviews { rating }
    inventory { quantity }
  }
}
```

### 3. **No N+1 Problem**
```graphql
# 100 products with reviews = still 1 request
query {
  products(limit: 100) {
    name
    reviews { rating }
  }
}
```

### 4. **Schema Evolution**
```graphql
# Deprecate fields without breaking changes
type Product {
  oldField: String @deprecated(reason: "Use newField instead")
  newField: String
}
```

### 5. **Strong Typing**
```graphql
type Product {
  id: ID!           # Non-null ID
  price: Float!     # Non-null Float
  reviews: [Review] # Array of Review
}
```

### 6. **Self-Documenting**
- GraphiQL provides interactive documentation
- Introspection reveals entire schema
- Auto-complete in IDE

### 7. **Flexible for Different Clients**
```graphql
# Mobile app (minimal data)
query {
  products { id name price }
}

# Web app (detailed data)
query {
  products {
    id name description price
    category { name }
    reviews { rating comment }
  }
}
```

---

## ❌ GraphQL Disadvantages

### 1. **Complexity**
- Steeper learning curve
- More complex server implementation
- Requires understanding of schema design

### 2. **Caching Challenges**
```
POST /graphql
# Can't use HTTP caching easily
# Need custom caching solutions (Apollo, DataLoader)
```

### 3. **Over-Querying**
```graphql
# Malicious or accidental expensive queries
query {
  products {
    reviews {
      author {
        products {
          reviews {
            # Deeply nested, expensive query
          }
        }
      }
    }
  }
}
```

### 4. **File Uploads**
- Not built-in to GraphQL spec
- Requires additional libraries
- More complex than REST multipart

### 5. **Monitoring & Error Handling**
- All requests return 200 OK
- Errors in response body
- Harder to monitor with traditional tools

### 6. **Learning Curve for Team**
- New concepts (schema, resolvers, fragments)
- Different debugging approach
- Requires training

---

## 🎯 When to Use REST

### ✅ Use REST When:

1. **Simple CRUD Operations**
   - Basic create, read, update, delete
   - No complex relationships
   - Example: User management, simple blog

2. **Public APIs**
   - Need HTTP caching
   - Want wide compatibility
   - Example: Weather API, public data

3. **File Uploads/Downloads**
   - Streaming large files
   - Simple multipart uploads
   - Example: Image upload service

4. **Team Familiarity**
   - Team knows REST well
   - Limited time for learning
   - Example: Small startup, tight deadlines

5. **Microservices**
   - Service-to-service communication
   - Simple request/response
   - Example: Internal APIs

### Real-World Examples:
- **Twitter API** (simple tweets, users)
- **Stripe API** (payments, customers)
- **GitHub REST API** (repositories, issues)

---

## 🎯 When to Use GraphQL

### ✅ Use GraphQL When:

1. **Complex Data Relationships**
   - Deeply nested data
   - Many-to-many relationships
   - Example: Social network, e-commerce

2. **Multiple Client Types**
   - Mobile, web, desktop
   - Different data needs
   - Example: Facebook, Instagram

3. **Frequent Schema Changes**
   - Rapid iteration
   - Need backward compatibility
   - Example: Startup in growth phase

4. **Over/Under-Fetching Problems**
   - Mobile bandwidth concerns
   - Performance critical
   - Example: Mobile-first app

5. **Developer Experience**
   - Want strong typing
   - Need self-documentation
   - Example: Large development team

### Real-World Examples:
- **GitHub GraphQL API** (complex repository data)
- **Shopify API** (products, orders, customers)
- **Facebook Graph API** (social graph)

---

## 🔄 Hybrid Approach

Many companies use **both**:

```
REST for:
- File uploads
- Webhooks
- Simple CRUD
- Public APIs

GraphQL for:
- Complex queries
- Mobile apps
- Web dashboards
- Internal tools
```

**Examples:**
- **GitHub**: REST API + GraphQL API
- **Shopify**: REST API + GraphQL API
- **Stripe**: Primarily REST, exploring GraphQL

---

## 📊 Performance Comparison

### Bandwidth Usage

**Scenario: Get product name for 10 products**

**REST:**
```
10 requests × ~500 bytes = ~5KB
(Returns all fields for each product)
```

**GraphQL:**
```
1 request × ~200 bytes = ~200 bytes
(Returns only name field)
```

### Request Count

**Scenario: Get 10 products with reviews**

**REST:**
```
1 request (products) + 10 requests (reviews) = 11 requests
```

**GraphQL:**
```
1 request (nested query) = 1 request
```

---

## 🛠️ Example Queries

### REST Examples

```bash
# List products
curl http://localhost:3000/api/products

# Get single product
curl http://localhost:3000/api/products/1

# Get product reviews
curl http://localhost:3000/api/products/1/reviews

# Create product
curl -X POST http://localhost:3000/api/products \
  -H "Content-Type: application/json" \
  -d '{"name":"New Product","price":99.99,"category_id":1}'
```

### GraphQL Examples

```graphql
# List products with specific fields
query {
  products {
    id
    name
    price
  }
}

# Get product with nested data
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
    }
  }
}

# Create product
mutation {
  createProduct(input: {
    name: "New Product"
    price: 99.99
    categoryId: 1
  }) {
    id
    name
  }
}
```

---

## 🎓 Learning Resources

### REST
- [REST API Tutorial](https://restfulapi.net/)
- [HTTP Status Codes](https://httpstatuses.com/)
- [OpenAPI Specification](https://swagger.io/specification/)

### GraphQL
- [GraphQL Official Docs](https://graphql.org/learn/)
- [How to GraphQL](https://www.howtographql.com/)
- [GraphQL Best Practices](https://graphql.org/learn/best-practices/)

---

## 🧹 Cleanup

```bash
# Stop servers with Ctrl+C in each terminal

# Optional: Remove virtual environment
deactivate
rm -rf venv
```

---

## 📚 Next Steps

1. **Experiment**: Modify queries and see responses
2. **Add Features**: Implement pagination, filtering, sorting
3. **Performance**: Add DataLoader to prevent N+1 in GraphQL
4. **Security**: Add authentication and authorization
5. **Production**: Add rate limiting, monitoring, logging

---

## 🤝 Contributing

This is a learning demo. Feel free to:
- Add more examples
- Improve documentation
- Add new features
- Share feedback

---

## 📄 License

MIT License - Feel free to use for learning and teaching.

---

**🎉 Happy Learning!**

For design decision criteria, see [DESIGN_CHOICES.md](./DESIGN_CHOICES.md)
