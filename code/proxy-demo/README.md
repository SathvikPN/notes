# Nginx Proxy Demo - Learn Proxies Practically

This demo demonstrates **both Forward Proxy and Reverse Proxy** configurations, showing how they intercept and filter HTTP requests differently.

## 🎯 What You'll Learn

1. **Forward vs Reverse Proxy**: Understand the key differences with practical examples
2. **Request Interception**: How Nginx sits between client and internet/backend
3. **Request Filtering**: How to allow/block specific domains or paths
4. **Proxy Configuration**: Practical Nginx proxy setup for both types
5. **Request Flow**: Visualize the complete request journey

## 📁 Project Structure

```
proxy-demo/
├── client/                 # Simple web client
│   └── index.html         # Client interface to make requests
├── backend/               # Mock backend server
│   └── server.js          # Simple Node.js server
├── nginx/                 # Nginx proxy configuration
│   └── nginx.conf         # Proxy rules and filtering
├── docker-compose.yml     # Orchestrate all services
└── README.md             # This file
```

## 🏗️ Architecture

### Reverse Proxy (Port 80)
```
[Client] → [Reverse Proxy] → [Backend Server]
              ↓
        Filters by PATH
        (/api/allowed ✅, /api/blocked ❌)
```

### Forward Proxy (Port 8888)
```
[Client] → [Forward Proxy] → [Internet]
    ↑            ↓
 Explicitly  Filters by DOMAIN
configured  (example.com ✅, google.com ❌)
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Basic understanding of HTTP requests

### Step 1: Start All Services

```bash
cd /Users/sathvikpn/workspace/prep/code/proxy-demo
docker-compose up
```

### Step 2: Access the Demo

Open your browser and navigate to:
- **Client Interface**: http://localhost:8080
- **Direct Backend** (will fail through proxy): http://localhost:3000

### Step 3: Test Both Proxy Types

#### Option A: Automated Test Script
```bash
./test-proxies.sh
```

#### Option B: Manual Testing

**Test Reverse Proxy (port 80):**
```bash
# Allowed endpoint
curl http://localhost/api/allowed

# Blocked endpoint (returns 403)
curl http://localhost/api/blocked
```

**Test Forward Proxy (port 8888):**
```bash
# Allowed domain
curl -x http://localhost:8888 http://example.com

# Blocked domain (returns 403)
curl -x http://localhost:8888 http://google.com
```

#### Option C: Web Interface
Open http://localhost:8080 for an interactive demo of the **reverse proxy**

## 🔍 How It Works

### 1. Client Makes Request
Your browser sends a request to the Nginx proxy (port 80)

### 2. Nginx Intercepts
Nginx receives the request and checks its configuration rules

### 3. Filtering Logic
- **Allowed paths**: `/api/allowed`, `/api/data`
- **Blocked paths**: `/api/blocked`, `/api/secret`
- **Allowed domains**: `jsonplaceholder.typicode.com`, `api.github.com`
- **Blocked**: Everything else

### 4. Proxy or Reject
- ✅ Allowed → Nginx forwards to backend/internet
- ❌ Blocked → Nginx returns 403 Forbidden

## 📝 Key Nginx Proxy Concepts

### Proxy Pass
```nginx
proxy_pass http://backend:3000;
```
Forwards the request to the specified backend server.

### Location Blocks
```nginx
location /api/allowed {
    proxy_pass http://backend:3000;
}
```
Defines rules for specific URL paths.

### Access Control
```nginx
location /api/blocked {
    return 403;
}
```
Blocks specific requests with HTTP 403.

### Headers
```nginx
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
```
Adds metadata about the original request.

## 🧪 Experiments to Try

1. **Modify Allowed Paths**: Edit `nginx/nginx.conf` to allow different paths
2. **Add Domain Whitelist**: Configure proxy to allow specific external domains
3. **View Logs**: Check Nginx logs to see intercepted requests
4. **Add Authentication**: Require tokens for certain endpoints
5. **Rate Limiting**: Limit requests per IP address

## 📊 Monitoring Requests

### View Nginx Logs
```bash
docker-compose logs -f nginx
```

### View Backend Logs
```bash
docker-compose logs -f backend
```

## 🛠️ Configuration Files Explained

### nginx.conf
The heart of the proxy - defines all routing and filtering rules.

### docker-compose.yml
Orchestrates three services:
- `nginx`: The proxy server (port 80)
- `backend`: Mock API server (port 3000)
- `client`: Web interface (port 8080)

## 🎓 Learning Path

1. **Start Simple**: Run the demo and test allowed/blocked requests
2. **Read Logs**: Observe what happens in Nginx logs
3. **Modify Config**: Change nginx.conf and restart to see effects
4. **Add Rules**: Create your own filtering rules
5. **Advanced**: Add caching, load balancing, SSL termination

## 🔧 Troubleshooting

**Ports already in use?**
```bash
# Change ports in docker-compose.yml
ports:
  - "8081:80"  # Change 8080 to 8081
```

**Changes not reflecting?**
```bash
# Restart services
docker-compose restart nginx
```

**View running containers**
```bash
docker-compose ps
```

## 🧹 Cleanup

```bash
# Stop all services
docker-compose down

# Remove volumes
docker-compose down -v
```

## 📚 Next Steps

- Learn about reverse proxy vs forward proxy
- Explore Nginx caching mechanisms
- Implement SSL/TLS termination
- Add load balancing across multiple backends
- Set up authentication middleware

## 🤝 Real-World Use Cases

1. **Corporate Networks**: Filter employee internet access
2. **API Gateway**: Route requests to microservices
3. **Security**: Block malicious requests before reaching backend
4. **Caching**: Store responses to reduce backend load
5. **Load Balancing**: Distribute traffic across servers

---

**Happy Learning! 🚀**
