# Understanding Proxy Types

## 🔄 Forward Proxy vs Reverse Proxy

### Forward Proxy (Client-Side Proxy)

```
[Client] → [Forward Proxy] → [Internet/External Servers]
   ↑              ↑
   |              |
   Knows about    Acts on behalf
   the proxy      of CLIENT
```

**Characteristics:**
- Client **explicitly configures** the proxy
- Proxy sits between client and the internet
- Hides/protects the **client's identity**
- Client sends requests TO the proxy, asking it to fetch resources

**Real-World Examples:**
- Corporate firewall proxy (blocks certain websites)
- VPN services (hide your IP address)
- Content filtering in schools/offices
- Caching proxy to save bandwidth

**Configuration:**
Client must be configured with proxy settings (e.g., browser proxy settings)

---

### Reverse Proxy (Server-Side Proxy)

```
[Client] → [Reverse Proxy] → [Backend Server(s)]
              ↑                      ↑
              |                      |
         Client doesn't         Acts on behalf
         know it exists         of SERVER
```

**Characteristics:**
- Client **doesn't know** about the proxy
- Proxy sits in front of backend servers
- Hides/protects the **server infrastructure**
- Client thinks it's talking directly to the server

**Real-World Examples:**
- Nginx/Apache as load balancer
- CDN (Content Delivery Network)
- SSL termination
- API Gateway

**Configuration:**
No client configuration needed - transparent to client

---

## 📊 Comparison Table

| Feature | Forward Proxy | Reverse Proxy |
|---------|--------------|---------------|
| **Protects** | Client | Server |
| **Client Awareness** | Client knows about proxy | Client unaware |
| **Configuration** | Client must configure | Server-side only |
| **Direction** | Client → Proxy → Internet | Internet → Proxy → Server |
| **Use Case** | Privacy, filtering | Load balancing, security |
| **Example** | Corporate firewall | Nginx, CloudFlare |

---

## 🎯 This Demo Project

### Current Setup: Reverse Proxy ✅

The `nginx/nginx.conf` implements a **reverse proxy**:

```nginx
location /api/allowed {
    proxy_pass http://backend_server;
    # Nginx forwards to backend on behalf of the server
}
```

**Why it's a reverse proxy:**
1. Client sends request to `http://localhost/api/allowed`
2. Client doesn't know about `backend:3000`
3. Nginx forwards to backend server
4. Protects/hides backend infrastructure

### Enhanced: Forward Proxy Demo 🆕

The `nginx/forward-proxy.conf` implements a **forward proxy**:

```nginx
# Client explicitly uses this as a proxy
# Client configures: http://localhost:8888 as proxy server
```

**Why it's a forward proxy:**
1. Client configures browser to use proxy
2. Client sends ANY request through the proxy
3. Proxy filters/allows specific domains
4. Acts on behalf of the client

---

## 🧪 Testing Both Types

### Test Reverse Proxy (Current)
```bash
# Client doesn't configure anything
curl http://localhost/api/allowed
# → Nginx forwards to backend:3000
```

### Test Forward Proxy (New)
```bash
# Client explicitly uses proxy
curl -x http://localhost:8888 http://jsonplaceholder.typicode.com/posts/1
# → Nginx acts as forward proxy, filters domain
```

---

## 💡 Key Takeaway

**The main difference is WHO the proxy is protecting:**

- **Forward Proxy** = Protects the **CLIENT** (hides client from server)
- **Reverse Proxy** = Protects the **SERVER** (hides server from client)

Both intercept and filter requests, but from different perspectives!
