
# Fast Student API

Fast Student API is a robust and scalable backend API built using **FastAPI**. It provides a comprehensive set of APIs to manage students, leveraging **Pydantic** for request/response validation and **MongoDB** and **DynamoDB** for data persistence. The project follows a modular structure inspired by the **big application project structure** in FastAPI to maintain scalability and ease of maintenance.

## Features

- **Student management**: CRUD operations for student data (e.g., name, age, location, etc.).
- **MongoDB**: Uses MongoDB as the primary database for storing student and related data.
- **DynamoDB**: Supports additional data storage or integration with Amazon's DynamoDB, using **boto3**.
- **Pydantic Validation**: Pydantic models for request validation and data serialization.
- **Project structure**: Follows FastAPI’s big project structure for better maintainability and scalability.

## Tech Stack

- **FastAPI**: High-performance Python web framework.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **MongoDB**: NoSQL database for scalable and flexible data storage.
- **DynamoDB**: Amazon's NoSQL database used via boto3 client.
- **Uvicorn**: ASGI server for serving the FastAPI application.

## Requirements

- Python 3.9+
- MongoDB
- DynamoDB
- FastAPI
- Pydantic
- Uvicorn
- Motor (MongoDB async driver)
- Boto3 (AWS SDK for Python)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/fast-student-api.git
   cd fast-student-api
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/MacOS
   # or
   venv\Scripts\activate     # For Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the environment variables:
   Create a `.env` file in the root directory with the necessary configurations, including MongoDB and DynamoDB connection settings:
   ```bash
   MONGO_URI=mongodb://localhost:27017/your_db
   AWS_ACCESS_KEY_ID=your_aws_access_key_id
   AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
   AWS_REGION_NAME=your_aws_region
   ```

5. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

6. Access the API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Project Structure

```
app/
├── api/                         # API routes (organized by modules)
│   ├── __init__.py
│   ├── person.py                # Routes related to Person entity
│   └── student.py               # Routes related to Student entity
│
├── core/                        # Core application logic (config, security, etc.)
│   ├── __init__.py
│   └── config.py                # Configuration settings (environment variables, etc.)
│
├── enums/                       # Shared enums
│   ├── __init__.py
│   └── gender_enum.py           # Enum for Gender (male, female, other)
│
├── models/                      # Database models and shared models
│   ├── __init__.py
│   ├── shared.py                # Shared models (Address, GeoLocation, CustomDateTime)
│   ├── person.py                # Parent model (Person)
│   └── student.py               # Child model (Student)
│
├── schemas/                     # Pydantic schemas (request/response validation models)
│   ├── __init__.py
│   ├── common/                  # Common schemas used by multiple entities
│   │   ├── __init__.py
│   │   ├── location.py          # Schema for Location
│   │   ├── address.py           # Schema for Address
│   │   └── geofence.py          # Schema for GeoFence
│   ├── person.py                # Pydantic schemas for Person
│   └── student.py               # Pydantic schemas for Student
│
├── services/                    # Business logic and services for models
│   ├── __init__.py
│   ├── person_service.py        # Business logic for Person entity
│   └── student_service.py       # Business logic for Student entity
│
├── utils/                       # Utility functions (helpers, validations, etc.)
│   ├── __init__.py
│   └── validation.py            # Shared validation utilities (e.g., age validation)
│
└── main.py                      # FastAPI application entry point
```

### Key Components:

- **api/**: API routes that define the endpoints for the Person and Student entities.
- **core/**: Core logic for configurations and other centralized application concerns.
- **enums/**: Shared enums, like `GenderEnum`, used across services and schemas.
- **models/**: MongoDB data models and shared models like `Address`, `GeoLocation`, etc.
- **schemas/**: Pydantic request/response schemas, with a separation between common schemas and entity-specific schemas.
- **services/**: Business logic for handling the different operations on entities.
- **utils/**: Shared utility functions, including validation logic for common fields.

## Example API Endpoints

- **GET /students**: Fetch all students.
- **POST /students**: Create a new student.
- **GET /students/{student_id}**: Fetch a student by ID.
- **PUT /students/{student_id}**: Update a student by ID.
- **DELETE /students/{student_id}**: Delete a student by ID.

## Environment Variables

- `MONGO_URI`: MongoDB connection string.
- `AWS_ACCESS_KEY_ID`: AWS Access Key for DynamoDB.
- `AWS_SECRET_ACCESS_KEY`: AWS Secret Key for DynamoDB.
- `AWS_REGION_NAME`: AWS region for DynamoDB.
- `google_api_key`, `here_maps_api_key` for third-party services (configured in `core/config.py`).

## Testing

To run tests (assuming you have test cases set up):
```bash
pytest
```

## License

This project is licensed under the MIT License.
