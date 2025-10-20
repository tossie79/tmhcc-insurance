# 📑 TMHCC Underwriting Policy Management System

A **FastAPI**-based insurance policy management system built with a **Domain-Driven Design (DDD)** architecture. This project provides both robust **REST API** endpoints and a dynamic **web frontend** for comprehensive policy management operations.

---

##  Features

* **REST API** for managing insurance policies.
* **Frontend Dashboard** for real-time policy visualization and management.
* **HTMX-Powered Updates** for dynamic, efficient content updates without full page reloads.
* **Database Flexibility:** Supports **SQLite** (default) and **PostgreSQL**.

---

##  Architecture

This project strictly adheres to **Domain-Driven Design (DDD)** principles, utilizing a **clean architecture** to separate concerns.

The core structure is as follows:
```
app/policy_management/
├── domain/              # Business logic and entities 
├── infrastructure/      # Database, repositories, external concerns
├── application/         # Use cases and service layer
├── api/                # Web interface and REST API
└── tests/              # Test suites (unit, integration, API)

```
##  Quick Start

### Prerequisites

* **Python 3.11+**
* **SQLite** (default) or **PostgreSQL**
* **pip** (Python package manager)

### Installation

1.  **Clone the repository and set up the environment:**

    ```bash
    git clone <repository-url>
    cd tmhcc-underwriting

    # Create and activate a virtual environment
    python -m venv venv
    source venv/bin/activate    # On Windows: venv\Scripts\activate

    # Install dependencies
    pip install -r requirements.txt
    ```

2.  **Initialize the database:**

    The database is designed to **auto-initialize** on the first run of the application.

3.  **Run the application:**

    ```bash
    python main.py
    ```

### Access

Once running, access the system using these endpoints:

* **Web Frontend:** `http://localhost:8000`
* **API Documentation (Swagger/OpenAPI):** `http://localhost:8000/docs`
* **API v1 Base:** `http://localhost:8000/api/v1/policies`

---

##  API Usage

### REST API Endpoints

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/v1/policies/` | `GET` | List all policies |
| `/api/v1/policies/{policy_number}` | `GET` | Retrieve a single policy by its policy number |
| `/` | `GET` | Serve the frontend dashboard |

### Example Queries

**Get Policy by Policy Number**
```bash
curl -X GET "http://localhost:8000/api/v1/policies/TMPROP2024001"
```

**List All Policies**
```bash
curl -X GET "http://localhost:8000/api/v1/policies"
```

---
  ## **Testing**
   **Comprehensive Test Suite**
The project includes a complete test suite located in the tests/ directory:

**Test Structure**
 - Unit Tests (test_unit_basic.py): Test domain entities, value objects, and services in isolation
 - Integration Tests (test_integration_basic.py): Test database operations and repository patterns
 - API Tests (test_api_basic.py): Test REST API endpoints and HTTP responses

 **Run all tests**
 ```bash
cd app/policy_management
python -m pytest tests/ -v


# Run specific test types
python -m pytest tests/test_unit_basic.py -v           # Unit tests (domain logic)
python -m pytest tests/test_integration_basic.py -v    # Integration tests (database)
python -m pytest tests/test_api_basic.py -v            # API tests (endpoints)

# Run with coverage
python -m pytest tests/ --cov=app.policy_management --cov-report=html

# Run specific test markers
python -m pytest tests/ -m "unit" -v
python -m pytest tests/ -m "integration" -v
python -m pytest tests/ -m "api" -v
```


 ## **Development**
  **Code Quality**
Ensure code quality using the following commands for linting and formatting:
 ```bash
flake8 app/ tests/
black app/ tests/ --check
```
## **Database Schema**
The system uses a normalized database design:
 - policies - Main policy records
 - policy_statuses - Status lookup (active, pending, cancelled, inactive)
 - policy_types - Type lookup (Property, Casualty, Marine, Construction) 

 Key features:
 - Automatic timestamp tracking
 - Foreign key constraints
 - Optimized indexes for common queries
 - Data validation at database level

## **Potential Improvements**
  **Short-term**
 - Add pagination to policy listings.
 - Implement policy search and filtering functionality.
 - Add policy create, update, cancel, and activate endpoints.
 - Enhance error handling and input validation.
 - Introduce commands and queries in the application layer to move towards a CQRS (Command Query Responsibility Segregation) pattern.
 - Implement rate limiting.

 **Medium-term**
 - Implement policy documents storage
 - Add email notifications for policy events
 - Create a dedicated admin dashboard.
 - Add detailed audit logging.
 - mplement a structured policy renewal workflow.

**Long-term**
 - Event Driven architecture architecture 
 - Implement a structured policy renewal workflow.
 - Develop advanced analytics and reporting features.
 - Integrate Machine Learning models for risk assessment.