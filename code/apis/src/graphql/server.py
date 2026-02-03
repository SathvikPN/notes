"""
GraphQL API Server using Strawberry + Flask
Demonstrates GraphQL's single endpoint with flexible queries
"""

from flask import Flask
from flask_cors import CORS
from strawberry.flask.views import GraphQLView
from schema import schema

app = Flask(__name__)
CORS(app)  # Enable CORS

# Add GraphQL endpoint
app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql_view", schema=schema),
)

# Add GraphQL IDE (GraphiQL)
app.add_url_rule(
    "/",
    view_func=GraphQLView.as_view("graphiql", schema=schema, graphiql=True),
)


if __name__ == '__main__':
    print("=" * 60)
    print("🚀 GraphQL API Server Starting")
    print("=" * 60)
    print(f"📍 GraphQL Endpoint: http://localhost:4000/graphql")
    print(f"🎨 GraphiQL IDE: http://localhost:4000")
    print("=" * 60)
    print("\n✨ GraphQL Advantages:")
    print("   • Single endpoint for all queries")
    print("   • Request exactly the fields you need")
    print("   • Nested data in single request")
    print("   • No over-fetching or under-fetching")
    print("   • Strong typing and introspection")
    print("   • Self-documenting API")
    print("=" * 60)
    print("\n📝 Example Query:")
    print("""
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
        inventory {
          quantity
        }
      }
    }
    """)
    print("=" * 60)
    print()
    
    app.run(host='0.0.0.0', port=4000, debug=True)
