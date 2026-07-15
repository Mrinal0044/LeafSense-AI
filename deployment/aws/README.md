# AWS Manual Deployment Guide (Amplify + EC2 + S3 + RDS)

This guide provides comprehensive, step-by-step instructions for deploying the **LeafSense AI** infrastructure manually using the AWS Management Console. 

No Terraform or coding is required for the infrastructure setup—just point and click!

---

## Architecture Overview

```
                   User
                    │
              AWS Amplify
           (React Frontend)
                    │
              HTTPS REST API
                    │
           Amazon EC2 (FastAPI)
         ┌──────────┼──────────┐
         │          │          │
         ▼          ▼          ▼
    TensorFlow   Amazon S3   Amazon RDS
     Model        Images    PostgreSQL
```

---

## Phase 1: Security and Storage Setup

### Step 1: Create the S3 Bucket (For Image Uploads)
1. Log in to the AWS Console and search for **S3**.
2. Click **Create bucket**.
3. **Bucket name**: Enter a globally unique name (e.g., `leafsense-uploads-yourname-2026`).
4. **AWS Region**: Select your preferred region (e.g., `ap-south-1` Mumbai).
5. **Object Ownership**: Leave as ACLs disabled (recommended).
6. **Block Public Access**: Ensure **Block all public access** is **CHECKED**. Our backend uses secure pre-signed URLs, so the bucket itself must remain strictly private.
7. Click **Create bucket**. *Save this bucket name for later.*

### Step 2: Create Security Groups
1. Search for **EC2** in the AWS Console.
2. In the left menu, under **Network & Security**, click **Security Groups**.
3. **Create the EC2 Security Group**:
   - **Name**: `leafsense-ec2-sg`
   - **Description**: Allow HTTP and SSH
   - **Inbound Rules**: 
     - Type: **HTTP**, Port: **80**, Source: **Anywhere-IPv4 (0.0.0.0/0)**
     - Type: **SSH**, Port: **22**, Source: **Anywhere-IPv4 (0.0.0.0/0)** (or restrict to your specific IP).
   - Click **Create security group**.
4. **Create the RDS Security Group**:
   - **Name**: `leafsense-rds-sg`
   - **Description**: Allow Postgres from EC2
   - **Inbound Rules**:
     - Type: **PostgreSQL**, Port: **5432**, Source: Select the `leafsense-ec2-sg` you just created.
   - Click **Create security group**.

---

## Phase 2: Database Setup

### Step 3: Launch the RDS PostgreSQL Database
1. Search for **RDS** in the AWS Console.
2. Click **Create database**.
3. **Creation method**: Standard create.
4. **Engine options**: Select **PostgreSQL** (Version 15.x or higher).
5. **Templates**: Select **Free tier** (if available) or **Dev/Test**.
6. **Settings**:
   - DB instance identifier: `leafsense-db`
   - Master username: `leafsense_admin`
   - Master password: Create a strong password and save it!
7. **Instance configuration**: `db.t3.micro` or `db.t4g.micro`.
8. **Connectivity**:
   - **Public access**: **No** (crucial for security).
   - **VPC security group**: Choose **Select existing** and select the `leafsense-rds-sg` created in Step 2. Remove the default security group.
9. Click **Create database**.
   > *Note: It will take a few minutes to provision. Once its status is "Available", click on it and copy the **Endpoint** address.*

---

## Phase 3: Backend API Setup (Amazon EC2)

### Step 4: Create an IAM Role for EC2
Your EC2 instance needs permission to upload files to your S3 bucket.
1. Search for **IAM** in the AWS Console.
2. Go to **Roles** -> **Create role**.
3. **Trusted entity type**: AWS service -> **EC2**. Click Next.
4. **Add permissions**: Search for and select **AmazonS3FullAccess** and **AmazonSSMManagedInstanceCore**.
5. **Role name**: `leafsense-ec2-role`. Click **Create role**.

### Step 5: Launch the EC2 Instance
1. Search for **EC2** in the console and click **Launch instance**.
2. **Name**: `leafsense-backend`.
3. **Application and OS Images**: Select **Ubuntu** (Ubuntu Server 22.04 LTS).
4. **Instance type**: Select **t3.medium** (needed for TensorFlow memory requirements).
5. **Key pair**: Create a new key pair (e.g., `leafsense-key`) or use an existing one so you can SSH into the server later.
6. **Network settings**:
   - **Security groups**: Select **existing security group** and choose `leafsense-ec2-sg`.
7. **Advanced details**:
   - **IAM instance profile**: Select the `leafsense-ec2-role` you created in Step 4.
   - **User data**: 
     - Open the `deployment/aws/ec2-setup.sh` file located in this repository.
     - **IMPORTANT**: At the top of that file, replace the placeholder variables with your specific database password, database endpoint (from Step 3), and S3 bucket name (from Step 1).
     - Copy the entire contents of the updated file and paste it into this User data text box.
8. Click **Launch instance**.
   > *The User Data script will automatically install Python, clone your GitHub repo, setup the environment, and start the FastAPI server via Nginx. It takes about 5 minutes to complete the initial setup.*

9. Once the instance is running, copy its **Public IPv4 address**.

---

## Phase 4: Frontend Web App Setup (AWS Amplify)

### Step 6: Deploy React App via AWS Amplify
1. Ensure your latest code (including the `amplify.yml` file) is pushed to your GitHub repository.
2. Search for **AWS Amplify** in the AWS Console.
3. Click **Create new app**.
4. Select **GitHub** and authorize AWS to access your repositories.
5. Select the `leafsense-ai` repository and the `main` branch.
6. In the **Build settings** page, expand **Advanced settings**.
7. Add an **Environment variable**:
   - **Key**: `VITE_API_BASE_URL`
   - **Value**: `http://<YOUR_EC2_PUBLIC_IP>` (Replace with the IP copied in Step 5).
8. Click **Save and deploy**.
9. Amplify will now build and host your frontend. Once complete, click the generated **Domain** link to access your LeafSense AI web application!

---

## Troubleshooting

- **API Not Connecting**: If the frontend cannot connect to the backend, ensure you used `http://` (not `https://`) for the `VITE_API_BASE_URL` since we haven't configured SSL certificates yet. Also verify the EC2 Security Group allows Port 80.
- **Checking EC2 Logs**: If the backend is returning 500 errors or failing to start, SSH into your EC2 instance and check the service logs:
  ```bash
  ssh -i "leafsense-key.pem" ubuntu@<YOUR_EC2_PUBLIC_IP>
  sudo journalctl -u leafsense-backend -f
  ```
