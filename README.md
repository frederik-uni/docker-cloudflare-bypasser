# docker-cloudflare-bypasser
A simple api that runs within a container that returns user-agent and cookies 
```
docker run -p 8000:8000 frederikuni/docker-cloudflare-bypasser:latest



curl -X POST "http://127.0.0.1:8000/bypass-cloudflare" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://nopecha.com/demo/cloudflare"}'
```
