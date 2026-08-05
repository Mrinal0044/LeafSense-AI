# LeafSense AI – AWS Based AI-Powered Plant Health Management Platform

LeafSense AI is a production-ready, AI-powered plant disease detection platform that identifies plant health conditions from uploaded leaf images using **EfficientNetB0 Transfer Learning**. The application provides disease diagnosis, scientific names, treatment recommendations, preventive measures, prediction history, and dashboard analytics through a secure cloud-hosted architecture.

**Project Demo:**
https://drive.google.com/file/d/1ardyiYpifhE5sTVY96kd3ORLRYe3Mh8d/view?usp=sharing

---

## Project Preview

| Landing Page | Prediction Dashboard |
|--------------|----------------------|
| *(Add Screenshot)* | *(Add Screenshot)* |

| Swagger API | Disease Prediction |
|--------------|--------------------|
| *(Add Screenshot)* | *(Add Screenshot)* |

---

## Features

- AI-powered plant disease detection
- EfficientNetB0 transfer learning model
- Supports 38 crop disease classes
- Secure JWT (OAuth2) authentication
- User registration and login
- Dashboard analytics
- Prediction history
- Scientific name identification
- Disease treatment suggestions
- Prevention recommendations
- Interactive Swagger API documentation
- Dockerized full-stack application
- AWS cloud deployment

---

## Architecture

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

## AWS Deployment Architecture

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

## Machine Learning

### Model

- EfficientNetB0 (Transfer Learning)

### Dataset

PlantVillage Dataset

### Dataset Statistics

| Metric | Value |
|--------|------:|
| Training Images | 37,997 |
| Validation Images | 10,859 |
| Total Images | 48,856+ |
| Disease Classes | 38 |

### Performance

| Metric | Value |
|---------|------:|
| Validation Accuracy | **98.74%** |

The model predicts:

- Disease name
- Scientific name
- Confidence score
- Plant health status
- Disease description
- Symptoms
- Treatment
- Prevention

---

## Tech Stack

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

## Project Structure

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

## REST APIs

### Authentication

| Method | Endpoint |
|---------|----------|
| POST | `/api/auth/register` |
| POST | `/api/auth/login` |

### Predictions

| Method | Endpoint |
|---------|----------|
| POST | `/api/predictions/predict` |
| GET | `/api/predictions/history` |
| DELETE | `/api/predictions/history/{id}` |

### Dashboard

| Method | Endpoint |
|---------|----------|
| GET | `/api/dashboard/stats` |

### Profile

| Method | Endpoint |
|---------|----------|
| GET | `/api/profile` |
| PUT | `/api/profile` |

---

## Authentication

LeafSense AI secures protected APIs using:

- JWT authentication
- OAuth2 password flow
- Bearer tokens
- Password hashing using Passlib

Protected endpoints include:

- Predictions
- Dashboard
- Prediction history
- User profile

---

## Local Deployment

### Clone Repository

```bash
git clone https://github.com/<your-username>/LeafSense-AI.git
cd LeafSense-AI
```

### Start Containers

```bash
docker compose up --build -d
```

### View Running Containers

```bash
docker compose ps
```

### Backend

```
http://localhost:8000
```

Swagger documentation:

```
http://localhost:8000/docs
```

### Frontend

```
http://localhost
```

---

## Production Deployment

The application is deployed on AWS using:

- **AWS EC2 (Ubuntu)** for hosting Dockerized React and FastAPI services
- **Amazon RDS PostgreSQL** as the managed cloud database
- **Docker Compose** for container orchestration
- **Nginx** for serving the React frontend
- **Swagger/OpenAPI** for API documentation

---

## Dashboard Analytics

The analytics dashboard provides:

- Total predictions
- Healthy vs. diseased plants
- Confidence distribution
- Most common diseases
- Recent prediction history

---

## Prediction Workflow

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

## Project Highlights

- Built an EfficientNetB0 transfer learning model
- 98.74% validation accuracy
- 38 crop disease categories
- 48,856+ images used for training and validation
- JWT authentication
- RESTful FastAPI backend
- React frontend
- PostgreSQL database
- Amazon RDS integration
- AWS EC2 deployment
- Dockerized full-stack architecture
- Prediction history tracking
- Dashboard analytics
- Swagger/OpenAPI documentation

---

## Author

**Mrinal**

GitHub: https://github.com/Mrinal0044

LinkedIn: *(Add your LinkedIn URL here)*
