# COSC310-Team9-ByteBites

## 📌 Project Overview
ByteBites is a full-stack, dockerized multi-user backend system designed for a food delivery application using **FastAPI**. The project focuses on robust backend functionality, data integrity, and RESTful API development while adhering to modern software engineering practices like **SOLID principles**, automated testing via **Pytest**, and **CI/CD** via GitHub Actions.

---

## 🏗 Architecture & Design
The system is organized into three distinct layers:

1. **API Layer (FastAPI Routers)**  
   Handles REST endpoints, validation, and RBAC.

2. **Service Layer (Business Logic)**  
   Implements business rules such as pricing, order flow, and refunds.

3. **Data Access Layer (Persistence)**  
   Manages data storage and retrieval.

---

## 🛠 Core Features
The following features are implemented:

- **User Authentication & Authorization** (RBAC)
- **Menu Management** (CRUD for managers)
- **Browse & Search** (filter + pagination)
- **Order Management** (full lifecycle)
- **Pricing & Calculation**
- **Payment Simulation**
- **Refund System**
- **Notifications System**

---

## 🧪 Testing & Quality Assurance
- **Pytest** for unit & integration tests  
- **CI/CD** using GitHub Actions  
- **Testing techniques**:
  - Mocking  
  - Equivalence partitioning  
  - Fault injection  
- Test results stored in `backend/tests/`

---

## 🐳 Docker Setup

The system is fully containerized to ensure consistent deployment and environment reproducibility.

---

### 🔧 Build Docker Images

```bash
docker build -t bytebites-backend ./backend
docker build -t bytebites-frontend ./frontend


docker run -p 8000:8000 bytebites-backend
docker run -p 5173:80 bytebites-frontend

docker compose up --build
