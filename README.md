# COSC310-Team9-ByteBites

## 📌 Project Overview
ByteBites is a full-stack, dockerized multi-user backend system designed for a food delivery application using **FastAPI**. The project focuses on robust backend functionality, data integrity, and RESTful API development while adhering to modern software engineering practices like **SOLID principles**, automated testing via **Pytest**, and **CI/CD** via GitHub Actions.

## 🏗 Architecture & Design
The system is organized into three distinct layers as defined in the Milestone 2 (M2) architecture document:

1.  **API Layer (FastAPI Routers)**: Manages RESTful endpoints, request validation, and enforces role-based access control (RBAC).
2.  **Service Layer (Business Logic)**: Implements all business rules, including order workflows, pricing rules, and status transitions.
3.  **Data Access Layer (Persistence)**: Handles database operations and data retrieval, ensuring the rest of the system does not directly access the database.



## 🛠 Core Features
The following features from the Software Requirements Specification (SRS) are implemented:
* **User Authentication & Authorization**: Secure login and registration with Role-Based Access Control (Regular User, Restaurant Manager, Admin).
* **Menu Management**: Allows managers to perform CRUD operations on menu items linked to their specific restaurants.
* **Browse & Search**: Keyword-based filtering for restaurants and menu items with paginated results.
* **Order Management**: Lifecycle management from creation to completion, enforcing immutability once an order is marked as "Completed".
* **Pricing & Calculation**: Automated totals using the business rule: $Total = Subtotal + Delivery Fee + Taxes$.
* **Payment & Notifications**: Simulated "Success/Rejected" payment workflows and event-driven notifications for status changes.

## 🧪 Testing & Quality Assurance
In alignment with Milestone 3 (M3) requirements, this repository maintains high code quality through:
* **Automated Testing**: Integration and unit tests using Pytest covering core API endpoints.
* **CI Pipeline**: A GitHub Actions workflow ensures all code passes tests before merging.
* **QA Methodologies**: Utilization of mocking, equivalence partitioning, and fault injection to ensure system reliability.
* **Test Evidence**: Reports and coverage screenshots are maintained in the `backend/tests/reports/` directory.

## 🚀 Getting Started
The system is fully containerized for environment consistency.

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
* **Course**: COSC 310 - Software Engineering
* **Team**: Team 9
* **Members**: Ruoyan Xu, Vinayak Singh, Amro Ahmed
