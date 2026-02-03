#!/bin/bash

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "  🔄 Proxy Demo - Testing Both Types"
echo "=========================================="
echo ""

# ========================================
# Test Reverse Proxy
# ========================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}1. REVERSE PROXY (Server-Side)${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "📝 Description: Client doesn't know about backend server"
echo "   Client → Reverse Proxy (port 80) → Backend Server"
echo ""

echo -e "${YELLOW}Test 1: Allowed endpoint through reverse proxy${NC}"
echo "Command: curl http://localhost/api/allowed"
echo ""
curl -s http://localhost/api/allowed | jq '.' 2>/dev/null || curl -s http://localhost/api/allowed
echo ""
echo ""

echo -e "${YELLOW}Test 2: Blocked endpoint (should return 403)${NC}"
echo "Command: curl http://localhost/api/blocked"
echo ""
curl -s http://localhost/api/blocked | jq '.' 2>/dev/null || curl -s http://localhost/api/blocked
echo ""
echo ""

echo -e "${YELLOW}Test 3: External domain through reverse proxy${NC}"
echo "Command: curl http://localhost/external/jsonplaceholder/posts/1"
echo ""
curl -s http://localhost/external/jsonplaceholder/posts/1 | jq '.' 2>/dev/null || curl -s http://localhost/external/jsonplaceholder/posts/1
echo ""
echo ""

# ========================================
# Test Forward Proxy
# ========================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}2. FORWARD PROXY (Client-Side)${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "📝 Description: Client explicitly uses proxy to access internet"
echo "   Client → Forward Proxy (port 8888) → Internet"
echo ""

echo -e "${YELLOW}Test 4: Check forward proxy info${NC}"
echo "Command: curl http://localhost:8888/proxy-info"
echo ""
curl -s http://localhost:8888/proxy-info | jq '.' 2>/dev/null || curl -s http://localhost:8888/proxy-info
echo ""
echo ""

echo -e "${YELLOW}Test 5: Access allowed domain through forward proxy${NC}"
echo "Command: curl -x http://localhost:8888 http://example.com"
echo ""
curl -x http://localhost:8888 -s http://example.com | head -n 20
echo "... (truncated)"
echo ""
echo ""

echo -e "${YELLOW}Test 6: Try blocked domain (should fail)${NC}"
echo "Command: curl -x http://localhost:8888 http://google.com"
echo ""
curl -x http://localhost:8888 -s http://google.com | jq '.' 2>/dev/null || curl -x http://localhost:8888 -s http://google.com
echo ""
echo ""

# ========================================
# Summary
# ========================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}📊 SUMMARY${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${GREEN}✅ Reverse Proxy (port 80):${NC}"
echo "   - Protects backend servers"
echo "   - Client unaware of proxy"
echo "   - Filters based on URL paths"
echo ""
echo -e "${GREEN}✅ Forward Proxy (port 8888):${NC}"
echo "   - Protects client identity"
echo "   - Client must configure proxy"
echo "   - Filters based on domains"
echo ""
echo "=========================================="
