#!/bin/bash

# Start both REST and GraphQL servers concurrently

echo "=========================================="
echo "  Starting REST and GraphQL Servers"
echo "=========================================="
echo ""
echo "REST API: http://localhost:3000"
echo "GraphQL API: http://localhost:4000"
echo "GraphiQL IDE: http://localhost:4000"
echo ""
echo "Press Ctrl+C to stop both servers"
echo "=========================================="
echo ""

# Start both servers in background
python src/rest/server.py &
REST_PID=$!

python src/graphql/server.py &
GRAPHQL_PID=$!

# Wait for both processes
wait $REST_PID $GRAPHQL_PID
