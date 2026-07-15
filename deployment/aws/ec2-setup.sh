#!/bin/bash
# ==============================================================================
# LeafSense AI - EC2 User Data Bootstrap Script
# ==============================================================================
# INSTRUCTIONS:
# Paste this entire script into the "User data" section under "Advanced details"
# when launching your EC2 instance in the AWS Management Console.
#
# IMPORTANT: Before pasting, update the placeholders in the variables section below!
# ==============================================================================

# Update these variables with your specific AWS resource details:
export DB_USER="leafsense_admin"
export DB_PASSWORD="REPLACE_WITH_YOUR_SECURE_PASSWORD"
export DB_HOST="REPLACE_WITH_YOUR_RDS_ENDPOINT_ADDRESS"
export AWS_S3_BUCKET="REPLACE_WITH_YOUR_S3_BUCKET_NAME"
export AWS_REGION="ap-south-1"

# ------------------------------------------------------------------------------
# System Update & Dependency Installation
# ------------------------------------------------------------------------------
apt-get update -y
apt-get install -y git python3-pip python3-venv nginx postgresql-client

# ------------------------------------------------------------------------------
# Create Backend Environment File
# ------------------------------------------------------------------------------
cat <<EOF > /etc/leafsense.env
ENVIRONMENT=production
DB_USER=${DB_USER}
DB_PASSWORD=${DB_PASSWORD}
DB_HOST=${DB_HOST}
DB_PORT=5432
DB_NAME=leafsense_db
AWS_S3_BUCKET=${AWS_S3_BUCKET}
AWS_REGION=${AWS_REGION}
USE_S3_STORAGE=true
EOF

# ------------------------------------------------------------------------------
# Clone Repository & Setup Virtual Environment
# ------------------------------------------------------------------------------
git clone https://github.com/kmrinal/leafsense-ai /home/ubuntu/leafsense-ai
chown -R ubuntu:ubuntu /home/ubuntu/leafsense-ai
cd /home/ubuntu/leafsense-ai

sudo -u ubuntu python3 -m venv /home/ubuntu/leafsense-ai/ml_venv
sudo -u ubuntu /home/ubuntu/leafsense-ai/ml_venv/bin/pip install --upgrade pip
sudo -u ubuntu /home/ubuntu/leafsense-ai/ml_venv/bin/pip install -r /home/ubuntu/leafsense-ai/backend/requirements.txt

# Run dry-run to compile assets and generate folder indices (prevents first-run delays)
sudo -u ubuntu /home/ubuntu/leafsense-ai/ml_venv/bin/python /home/ubuntu/leafsense-ai/ml/train.py --quick-train

# ------------------------------------------------------------------------------
# Configure and Start Systemd Daemon for FastAPI
# ------------------------------------------------------------------------------
cat <<EOF > /etc/systemd/system/leafsense-backend.service
[Unit]
Description=LeafSense AI FastAPI Application Service
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/leafsense-ai/backend
EnvironmentFile=/etc/leafsense.env
ExecStart=/home/ubuntu/leafsense-ai/ml_venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl start leafsense-backend
systemctl enable leafsense-backend

# ------------------------------------------------------------------------------
# Configure Nginx Reverse Proxy
# ------------------------------------------------------------------------------
cat <<EOF > /etc/nginx/sites-available/leafsense
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

ln -s /etc/nginx/sites-available/leafsense /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
systemctl restart nginx
