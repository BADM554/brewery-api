# Hetzner VPS Deployment Guide

Complete guide to deploy the Open Brewery DB API on a Hetzner VPS.

## Prerequisites

- Hetzner Cloud account ([hetzner.com](https://www.hetzner.com/cloud))
- Domain name (optional, for HTTPS)
- SSH client on your local machine

## Step 1: Create Hetzner VPS

1. Log in to [Hetzner Cloud Console](https://console.hetzner.cloud/)
2. Create new project (e.g., "badm554-api")
3. Add server:
   - **Location**: Choose closest to students
   - **Image**: Ubuntu 22.04
   - **Type**: CX11 (2GB RAM, 1 vCPU) - ~€4.15/month
   - **Networking**: IPv4 + IPv6
   - **SSH Key**: Add your public SSH key
   - **Firewall**: Create with these rules:
     - Inbound TCP 22 (SSH)
     - Inbound TCP 80 (HTTP)
     - Inbound TCP 443 (HTTPS)
     - Inbound TCP 8000 (API - optional)

4. Note your server IP address

## Step 2: Initial VPS Setup

### Connect to VPS
```bash
ssh root@YOUR_SERVER_IP
```

### Update system
```bash
apt update && apt upgrade -y
```

### Install Docker
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt install docker-compose -y

# Verify installation
docker --version
docker-compose --version
```

### Setup firewall (UFW)
```bash
ufw allow 22/tcp      # SSH
ufw allow 80/tcp      # HTTP
ufw allow 443/tcp     # HTTPS
ufw allow 8000/tcp    # API (if direct access needed)
ufw enable
ufw status
```

## Step 3: Deploy Application

### Option A: Simple Deployment (Direct Port Access)

```bash
# Create app directory
mkdir -p /opt/badm554-api
cd /opt/badm554-api

# Transfer files (run from your local machine)
scp -r /Users/vishal/Desktop/badm554-api/* root@YOUR_SERVER_IP:/opt/badm554-api/

# Or use git
git clone YOUR_REPO_URL /opt/badm554-api
cd /opt/badm554-api

# Start with Docker Compose
docker-compose up -d

# Check logs
docker-compose logs -f

# Test
curl http://YOUR_SERVER_IP:8000/
```

Your API will be available at: `http://YOUR_SERVER_IP:8000`

### Option B: Production Deployment with Caddy (HTTPS + Domain)

#### 1. Update docker-compose.yml
```bash
cd /opt/badm554-api
nano docker-compose-caddy.yml
```

Add this content:
```yaml
version: '3.8'

services:
  api:
    build: .
    expose:
      - "8000"
    restart: unless-stopped
    environment:
      - PYTHONUNBUFFERED=1

  caddy:
    image: caddy:2.7-alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - caddy_data:/data
      - caddy_config:/config
    restart: unless-stopped
    depends_on:
      - api

volumes:
  caddy_data:
  caddy_config:
```

#### 2. Create Caddyfile
```bash
nano Caddyfile
```

**For domain with HTTPS:**
```
api.yourdomain.com {
    reverse_proxy api:8000
    encode gzip
}
```

**For IP-only access (no HTTPS):**
```
http://YOUR_SERVER_IP {
    reverse_proxy api:8000
    encode gzip
}
```

#### 3. Setup DNS (if using domain)
Point your domain A record to your Hetzner server IP:
```
A    api    YOUR_SERVER_IP
```

#### 4. Deploy
```bash
docker-compose -f docker-compose-caddy.yml up -d --build

# Check logs
docker-compose -f docker-compose-caddy.yml logs -f

# Test
curl https://api.yourdomain.com/
```

Your API will be available at: `https://api.yourdomain.com`

## Step 4: Manage Deployment

### View logs
```bash
docker-compose logs -f api
```

### Restart services
```bash
docker-compose restart
```

### Update application
```bash
cd /opt/badm554-api
git pull  # or transfer new files
docker-compose down
docker-compose up -d --build
```

### Stop services
```bash
docker-compose down
```

### Monitor resources
```bash
docker stats
htop  # install with: apt install htop
```

## Step 5: Student Access

Share with students:
- **Simple deployment**: `http://YOUR_SERVER_IP:8000`
- **With domain**: `https://api.yourdomain.com`

Example for students:
```python
import requests

# Use your actual URL
API_URL = "http://YOUR_SERVER_IP:8000"

response = requests.get(f"{API_URL}/breweries?per_page=10")
breweries = response.json()["data"]
print(f"Found {len(breweries)} breweries")
```

## Troubleshooting

### Container won't start
```bash
docker-compose logs api
docker-compose ps
```

### Port already in use
```bash
# Check what's using port 8000
lsof -i :8000
# Kill process if needed
kill -9 PID
```

### Firewall blocking access
```bash
ufw status
ufw allow 8000/tcp
```

### Can't connect to server
```bash
# Test from VPS
curl localhost:8000

# Check if Docker is running
systemctl status docker
```

### SSL certificate issues (Caddy)
```bash
docker-compose -f docker-compose-caddy.yml logs caddy

# Ensure DNS is pointing to server
dig api.yourdomain.com
```

## Cost Estimation

**Hetzner CX11 Server:**
- 2GB RAM, 1 vCPU, 20GB SSD
- ~€4.15/month (~$4.50/month)
- Sufficient for 50+ concurrent students

**Recommended for production:**
- CPX11: 2GB RAM, 2 vCPU - €5.83/month
- Better CPU performance

## Security Best Practices

### 1. Create non-root user
```bash
adduser deploy
usermod -aG sudo deploy
usermod -aG docker deploy

# Switch to deploy user
su - deploy
```

### 2. Disable root SSH login
```bash
nano /etc/ssh/sshd_config
# Set: PermitRootLogin no
systemctl restart sshd
```

### 3. Setup automatic updates
```bash
apt install unattended-upgrades -y
dpkg-reconfigure -plow unattended-upgrades
```

### 4. Rate limiting (optional)
Install fail2ban:
```bash
apt install fail2ban -y
systemctl enable fail2ban
systemctl start fail2ban
```

## Backup Strategy

### Backup data
```bash
# Backup entire app directory
tar -czf badm554-api-backup.tar.gz /opt/badm554-api

# Download to local machine
scp root@YOUR_SERVER_IP:/root/badm554-api-backup.tar.gz .
```

### Hetzner Snapshots
- Use Hetzner Cloud Console
- Create snapshot: ~€0.01/GB/month
- Restore in minutes if needed

## Monitoring

### Basic monitoring
```bash
# Install monitoring tools
apt install htop iotop nethogs -y

# Check system resources
htop

# Check API health
watch -n 5 'curl -s http://localhost:8000/health | jq'
```

### Advanced monitoring (optional)
- **Uptime monitoring**: Use UptimeRobot (free)
- **Logs**: Setup logrotate for Docker logs
- **Metrics**: Prometheus + Grafana

## Quick Reference

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild and restart
docker-compose up -d --build

# Check status
docker-compose ps

# Shell into container
docker-compose exec api /bin/bash

# System resources
docker stats
```

## Support

- Hetzner Docs: https://docs.hetzner.com/
- Hetzner Community: https://community.hetzner.com/
- FastAPI Docs: https://fastapi.tiangolo.com/

---

**Total setup time:** ~15-30 minutes
**Cost:** ~€4-6/month
**Capacity:** 50+ concurrent users
