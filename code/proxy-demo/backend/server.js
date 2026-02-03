const http = require('http');
const url = require('url');

const PORT = 3000;

// Simple in-memory data store
const data = {
    users: [
        { id: 1, name: 'Alice', role: 'Developer' },
        { id: 2, name: 'Bob', role: 'Designer' },
        { id: 3, name: 'Charlie', role: 'Manager' }
    ],
    stats: {
        requests: 0,
        lastAccessed: null
    }
};

// Helper function to send JSON response
function sendJSON(res, statusCode, data) {
    res.writeHead(statusCode, { 
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    });
    res.end(JSON.stringify(data, null, 2));
}

// Create HTTP server
const server = http.createServer((req, res) => {
    const parsedUrl = url.parse(req.url, true);
    const path = parsedUrl.pathname;
    const method = req.method;

    // Increment request counter
    data.stats.requests++;
    data.stats.lastAccessed = new Date().toISOString();

    // Log incoming request
    console.log(`[${new Date().toISOString()}] ${method} ${path}`);
    
    // Log proxy headers if present
    if (req.headers['x-proxied-by']) {
        console.log(`  ✓ Proxied by: ${req.headers['x-proxied-by']}`);
    }
    if (req.headers['x-real-ip']) {
        console.log(`  ✓ Real IP: ${req.headers['x-real-ip']}`);
    }
    if (req.headers['x-forwarded-for']) {
        console.log(`  ✓ Forwarded for: ${req.headers['x-forwarded-for']}`);
    }

    // Handle CORS preflight
    if (method === 'OPTIONS') {
        sendJSON(res, 200, { message: 'OK' });
        return;
    }

    // Route handlers
    switch (path) {
        case '/health':
            sendJSON(res, 200, { 
                status: 'healthy', 
                service: 'backend-server',
                uptime: process.uptime()
            });
            break;

        case '/api/allowed':
            sendJSON(res, 200, { 
                message: '✅ Success! This request was allowed by the proxy',
                endpoint: '/api/allowed',
                data: 'This is sensitive data that only allowed requests can access',
                timestamp: new Date().toISOString(),
                proxied: req.headers['x-proxied-by'] ? true : false
            });
            break;

        case '/api/data':
            sendJSON(res, 200, { 
                message: '✅ Data endpoint accessed successfully',
                users: data.users,
                stats: data.stats
            });
            break;

        case '/api/public':
            sendJSON(res, 200, { 
                message: '✅ Public endpoint - accessible to all',
                info: 'This is public information',
                timestamp: new Date().toISOString()
            });
            break;

        case '/api/blocked':
            // This should never be reached if proxy is working
            sendJSON(res, 200, { 
                message: '⚠️ WARNING: You reached the blocked endpoint directly!',
                note: 'This means you bypassed the proxy. In production, this endpoint would not be publicly accessible.',
                endpoint: '/api/blocked'
            });
            break;

        case '/api/admin':
            // This should never be reached if proxy is working
            sendJSON(res, 200, { 
                message: '⚠️ WARNING: You reached the admin endpoint directly!',
                note: 'This should be blocked by the proxy',
                secretData: 'This is admin-only data'
            });
            break;

        case '/api/secret':
            // This should never be reached if proxy is working
            sendJSON(res, 200, { 
                message: '⚠️ WARNING: You reached the secret endpoint directly!',
                note: 'This should be blocked by the proxy',
                secret: 'super-secret-key-12345'
            });
            break;

        case '/':
            sendJSON(res, 200, { 
                message: 'Backend Server is running',
                endpoints: {
                    allowed: ['/health', '/api/allowed', '/api/data', '/api/public'],
                    blocked: ['/api/blocked', '/api/admin', '/api/secret']
                },
                note: 'Try accessing these endpoints through the proxy at http://localhost:80'
            });
            break;

        default:
            sendJSON(res, 404, { 
                error: 'Not Found',
                message: `Endpoint ${path} does not exist`,
                availableEndpoints: ['/health', '/api/allowed', '/api/data', '/api/public', '/api/blocked', '/api/admin', '/api/secret']
            });
    }
});

// Start server
server.listen(PORT, () => {
    console.log('='.repeat(60));
    console.log('🚀 Backend Server Started');
    console.log('='.repeat(60));
    console.log(`📍 Server running on: http://localhost:${PORT}`);
    console.log(`🔒 Direct access available on port ${PORT}`);
    console.log(`🌐 Proxy access available on port 80`);
    console.log('='.repeat(60));
    console.log('\n📋 Available Endpoints:');
    console.log('  ✅ Allowed through proxy:');
    console.log('     - GET /health');
    console.log('     - GET /api/allowed');
    console.log('     - GET /api/data');
    console.log('     - GET /api/public');
    console.log('\n  ❌ Blocked by proxy:');
    console.log('     - GET /api/blocked');
    console.log('     - GET /api/admin');
    console.log('     - GET /api/secret');
    console.log('\n' + '='.repeat(60));
    console.log('Waiting for requests...\n');
});

// Handle graceful shutdown
process.on('SIGTERM', () => {
    console.log('\n🛑 Received SIGTERM, shutting down gracefully...');
    server.close(() => {
        console.log('✅ Server closed');
        process.exit(0);
    });
});
