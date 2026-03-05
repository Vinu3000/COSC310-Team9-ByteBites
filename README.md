# COSC310-Team9-ByteBites

## 📌 Project Overview
[cite_start]ByteBites is a full-stack, dockerized multi-user backend system designed for a food delivery application using **FastAPI**[cite: 197, 205]. [cite_start]The project focuses on robust backend functionality, data integrity, and RESTful API development while adhering to modern software engineering practices like **SOLID principles**, automated testing via **Pytest**, and **CI/CD** via GitHub Actions[cite: 207].

## 🏗 Architecture & Design
[cite_start]The system is organized into three distinct layers as defined in the **Milestone 2 (M2)** architecture document[cite: 36, 37]:

1.  [cite_start]**API Layer (FastAPI Routers)**: Manages RESTful endpoints, request validation, and enforces role-based access control (RBAC)[cite: 38].
2.  [cite_start]**Service Layer (Business Logic)**: Implements all business rules, including order workflows, pricing rules, and status transitions[cite: 39, 40].
3.  [cite_start]**Data Access Layer (Persistence)**: Handles database operations and data retrieval, ensuring the rest of the system does not directly access the database[cite: 41, 42].



## 🛠 Core Features
The following features from the **Software Requirements Specification (SRS)** are implemented:
* [cite_start]**User Authentication & Authorization**: Secure login and registration with Role-Based Access Control (Regular User, Restaurant Manager, Admin)[cite: 43, 47].
* [cite_start]**Menu Management**: Allows managers to perform CRUD operations on menu items linked to their specific restaurants[cite: 51, 52].
* [cite_start]**Browse & Search**: Keyword-based filtering for restaurants and menu items with paginated results[cite: 58, 60].
* [cite_start]**Order Management**: Lifecycle management from creation to completion, enforcing immutability once an order is marked as "Completed"[cite: 63, 100].
* [cite_start]**Pricing & Calculation**: Automated totals using the business rule: $Total = Subtotal + Delivery Fee + Taxes$[cite: 69, 70].
* [cite_start]**Payment & Notifications**: Simulated "Success/Rejected" payment workflows and event-driven notifications for status changes[cite: 74, 79, 120].

## 🧪 Testing & Quality Assurance
In alignment with **M3 requirements**, this repository maintains high code quality through:
* [cite_start]**Automated Testing**: Integration and unit tests using `Pytest` covering core API endpoints[cite: 249].
* [cite_start]**CI Pipeline**: A GitHub Actions workflow ensures all code passes tests before merging[cite: 207].
* **QA Methodologies**: Utilization of mocking, equivalence partitioning, and fault injection to ensure system reliability.
* **Test Evidence**: Reports and coverage screenshots are maintained in the `backend/tests/reports/` directory.

## 🚀 Getting Started
[cite_start]The system is fully containerized for environment consistency[cite: 250].

### Prerequisites
* Docker and Docker Compose

### Installation
1.  **Clone the repository**:
    ```bash
    git clone [https://github.com/Vinu3000/COSC310-Team9-ByteBites.git](https://github.com/Vinu3000/COSC310-Team9-ByteBites.git)
    ```
2.  **Run with Docker**:
    ```bash
    docker-compose up --build
    ```
3.  **Access API Documentation**:
    Navigate to `http://localhost:8000/docs` to view the interactive FastAPI Swagger UI.

## 📑 Project Information
* [cite_start]**Course**: COSC 310 - Software Engineering [cite: 199]
* [cite_start]**Team**: Team 9 [cite: 200]
* [cite_start]**Members**: Ruoyan Xu, Vinayak Singh, Amro Ahmed [cite: 277, 278, 279]
* [cite_start]**Traceability**: For the mapping of requirements to implementation, see the **Traceability Matrix** in the `docs/` folder[cite: 193, 274].
