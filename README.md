# docker-cloudflare-bypasser
A simple api that runs within a container that returns user-agent and cookies 
```
curl -X POST "http://127.0.0.1:8000/bypass-cloudflare" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://nopecha.com/demo/cloudflare"}'
```
