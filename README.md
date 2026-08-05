# 🌿 LeafSense AI – AWS Based AI-Powered Plant Health Management Platform

LeafSense AI is a production-ready, AI-powered plant disease detection platform that identifies plant health conditions from uploaded leaf images using **EfficientNetB0 Transfer Learning**. The application provides disease diagnosis, scientific names, treatment recommendations, preventive measures, prediction history, and dashboard analytics through a secure cloud-hosted architecture.

🎥 **Project Demo:**  
https://drive.google.com/file/d/1ardyiYpifhE5sTVY96kd3ORLRYe3Mh8d/view?usp=sharing

---

# 📸 Project Preview

| Landing Page | Prediction Dashboard |
|--------------|----------------------|
| *(Add Screenshot)* | *(Add Screenshot)* |

| Swagger API | Disease Prediction |
|--------------|--------------------|
| *(Add Screenshot)* | *(Add Screenshot)* |

---

# 🚀 Features

- 🌱 AI-powered plant disease detection
- 🧠 EfficientNetB0 Transfer Learning model
- 📊 Supports **38 crop disease classes**
- 🔐 Secure JWT (OAuth2) Authentication
- 👤 User Registration & Login
- 📈 Dashboard Analytics
- 📝 Prediction History
- 🔬 Scientific Name Identification
- 💊 Disease Treatment Suggestions
- 🛡 Prevention Recommendations
- 📄 Interactive Swagger API Documentation
- 🐳 Dockerized Full Stack Application
- ☁️ AWS Cloud Deployment

---

# 🏗 Architecture

```text
                    React (Vite)
                           │
                           │ REST API
                           ▼
                  FastAPI Backend
          ┌──────────┴──────────┐
          │                     │
          ▼                     ▼
 EfficientNetB0 Model     Amazon RDS PostgreSQL
          │                     │
          └──────────┬──────────┘
                     ▼
               Prediction Results
```

---

# ☁️ AWS Deployment Architecture

```text
                Internet
                    │
                    ▼
           AWS EC2 (Ubuntu)
                    │
      ┌─────────────┴─────────────┐
      │                           │
 React Frontend             FastAPI Backend
      │                           │
      └─────────────┬─────────────┘
                    │
                    ▼
          Amazon RDS PostgreSQL
```

---

# 🤖 Machine Learning

### Model

- EfficientNetB0 (Transfer Learning)

### Dataset

PlantVillage Dataset

### Dataset Statistics

- Training Images: **37,997**
- Validation Images: **10,859**
- Total Images: **48,856+**
- Disease Classes: **38**

### Performance

| Metric | Value |
|---------|------:|
| Validation Accuracy | **98.74%** |

The model predicts:

- Disease Name
- Scientific Name
- Confidence Score
- Plant Health Status
- Disease Description
- Symptoms
- Treatment
- Prevention

---

# 🛠 Tech Stack

| Layer | Technologies |
|-------|--------------|
| Frontend | React, Vite, Tailwind CSS, React Router, Axios, Recharts |
| Backend | FastAPI, SQLAlchemy, Alembic, Pydantic, JWT OAuth2, Passlib |
| Machine Learning | TensorFlow, EfficientNetB0, OpenCV, NumPy, Scikit-learn |
| Database | PostgreSQL, Amazon RDS |
| Cloud | AWS EC2, Amazon RDS |
| DevOps | Docker, Docker Compose, Nginx |
| API Docs | Swagger / OpenAPI |

---

# 📁 Project Structure

```text
LeafSense-AI/
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── Dockerfile
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── auth/
│   │   ├── core/
│   │   ├── database/
│   │   ├── middleware/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── utils/
│   │   └── main.py
│   └── Dockerfile
│
├── ml/
│   ├── dataset/
│   ├── models/
│   ├── saved_model/
│   ├── train.py
│   └── predict.py
│
├── deployment/
│   └── docker-compose.yml
│
├── docs/
│
└── README.md
```

---

# 🔥 REST APIs

## Authentication

| Method | Endpoint |
|---------|----------|
| POST | `/api/auth/register` |
| POST | `/api/auth/login` |

---

## Predictions

| Method | Endpoint |
|---------|----------|
| POST | `/api/predictions/predict` |
| GET | `/api/predictions/history` |
| DELETE | `/api/predictions/history/{id}` |

---

## Dashboard

| Method | Endpoint |
|---------|----------|
| GET | `/api/dashboard/stats` |

---

## Profile

| Method | Endpoint |
|---------|----------|
| GET | `/api/profile` |
| PUT | `/api/profile` |

---

# 🔐 Authentication

LeafSense AI secures protected APIs using:

- JWT Authentication
- OAuth2 Password Flow
- Bearer Tokens
- Password Hashing using Passlib

Protected endpoints include:

- Predictions
- Dashboard
- Prediction History
- User Profile

---

# 🐳 Local Deployment

## Clone Repository

```bash
git clone https://github.com/<your-username>/LeafSense-AI.git
cd LeafSense-AI
```

---

## Start Containers

```bash
docker compose up --build -d
```

---

## View Running Containers

```bash
docker compose ps
```

---

## Backend

```
http://localhost:8000
```

Swagger Documentation

```
http://localhost:8000/docs
```

---

## Frontend

```
http://localhost
```

---

# ☁️ Production Deployment

The application is deployed on AWS using:

- **AWS EC2 (Ubuntu)** for hosting Dockerized React and FastAPI services
- **Amazon RDS PostgreSQL** as the managed cloud database
- **Docker Compose** for container orchestration
- **Nginx** for serving the React frontend
- **Swagger/OpenAPI** for API documentation

---

# 📊 Dashboard Analytics

The analytics dashboard provides:

- Total Predictions
- Healthy vs Diseased Plants
- Confidence Distribution
- Most Common Diseases
- Recent Prediction History

---

# 🌱 Prediction Workflow

```text
User Uploads Leaf Image
            │
            ▼
JWT Authentication
            │
            ▼
FastAPI Backend
            │
            ▼
EfficientNetB0 Model
            │
            ▼
Disease Prediction
            │
            ▼
Store Prediction in Amazon RDS
            │
            ▼
Dashboard Analytics Updated
            │
            ▼
Prediction Returned to Frontend
```

---

# 📈 Project Highlights

- ✅ Built an EfficientNetB0 Transfer Learning model
- ✅ 98.74% Validation Accuracy
- ✅ 38 Crop Disease Categories
- ✅ 48,856+ Images Used for Training & Validation
- ✅ JWT Authentication
- ✅ RESTful FastAPI Backend
- ✅ React Frontend
- ✅ PostgreSQL Database
- ✅ Amazon RDS Integration
- ✅ AWS EC2 Deployment
- ✅ Dockerized Full Stack Architecture
- ✅ Prediction History Tracking
- ✅ Dashboard Analytics
- ✅ Swagger/OpenAPI Documentation

---
