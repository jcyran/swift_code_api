# SWIFT Codes REST API

This project is a RESTful API built with **Django REST Framework** to parse, store, and serve SWIFT code data for banks across various countries. The API supports querying SWIFT codes by individual code or by country (using ISO-2 country codes), as well as adding and deleting SWIFT code entries. The application is containerized using Docker, with data stored in a PostgreSQL database for fast, low-latency querying.

## Table of Contents
- [Main Technologies](#main-technologies)
- [Setup Instructions](#setup-instructions)
- [Populating the Database](#populating-the-database)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Notes](#notes)

## Main Technologies
- Python
- Django
- Django REST Framework
- PostgreSQL
- Docker

## Setup Instructions

### Prerequisites
Ensure the following tools are installed:
- [Docker](https://www.docker.com/get-started) (for containerization)
- [Docker Compose](https://docs.docker.com/compose/install/) (for multi-container applications)
- [Git](https://git-scm.com/downloads) (for cloning the repository)

### Installation and Preparation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/jcyran/swift_code_api.git
   cd swift_code_api
   ```

2. **Environment Variables**:
   - Create a `.env` file in the project root based on the provided `.env.example`:
     ```env
     DB_NAME=mydb
     DB_USER=user
     DB_PASSWORD=pass
     DB_HOST=db
     DB_PORT=5432
     DJANGO_SECRET_KEY=your-secret-key
     ```
   - Replace `your-secret-key` with a secure key for production. Ensure `DB_HOST` matches the database service name in `docker-compose.yml`.

3. **Build and Run with Docker**:
   - Run the following command to build and start the containers:
     ```bash
     docker-compose up --build
     ```
   - This will:
     - Set up a PostgreSQL database.
     - Run migrations to create the database schema.
     - Start the REST API at `http://localhost:8080`.

## Populating the Database
To populate the database with SWIFT code data:
- Use the provided [sample datasheet](./datasheets/sample_data.csv) by running:
  ```bash
  docker-compose exec web python manage.py import_from_csv datasheets/sample_data.csv
  ```
  - You can replace `sample_data.csv` with another CSV file following the same format.
- Alternatively, use the POST endpoint (see [API Endpoints](#api-endpoints)) to add entries programmatically.

## Testing
The project includes unit and integration tests located in `./api/tests/`.

1. **Run Tests**:
   ```bash
   docker-compose exec web python manage.py test
   ```

2. **Check Test Coverage**:
   ```bash
   docker-compose exec web pip install coverage
   docker-compose exec web coverage run manage.py test
   docker-compose exec web coverage report
   ```

## Project Structure
```
swift_code_api/
├── api/                        # Django app for SWIFT code API logic
│   ├── management/             # Custom Django management commands
│   ├── migrations/             # Database migrations
│   ├── tests/                  # Unit and integration tests
│   ├── utils/                  # Utility functions and helpers
│   ├── __init__.py            # Python package initialization
│   ├── admin.py               # Django admin configuration
│   ├── apps.py                # Django app configuration
│   ├── models.py              # Database models for SWIFT codes
│   ├── serializers.py         # API serializers for data formatting
│   ├── urls.py                # URL routing for the API
│   └── views.py               # API views and logic
├── datasheets/                 # Directory for input data files
│   └── sample_data.csv        # Sample SWIFT codes data file
├── swift_code_api/             # Django project settings
│   ├── __init__.py            # Python package initialization
│   ├── asgi.py                # ASGI configuration for async deployment
│   ├── settings.py            # Django project settings
│   ├── urls.py                # Project-level URL routing
│   └── wsgi.py                # WSGI configuration for deployment
├── docker-compose.yml          # Docker Compose configuration for app and database
├── Dockerfile                  # Docker configuration for the application
├── manage.py                   # Django management script
├── README.md                   # Project documentation
└── requirements.txt            # Python dependencies
```

## API Endpoints
The following endpoints are available for interacting with the SWIFT codes API:

| Method | Endpoint                                  | Description                                                  | Parameters                              |
|--------|-------------------------------------------|--------------------------------------------------------------|-----------------------------------------|
| GET    | `/v1/swift-codes/{swiftCode}`            | Retrieve details of a single SWIFT code (headquarters or branch) | `swiftCode` (e.g., `ABCDEF12XXX`)    |
| GET    | `/v1/swift-codes/country/{countryISO2}`  | Retrieve all SWIFT codes for a specific country               | `countryISO2` (e.g., `PL`)              |
| POST   | `/v1/swift-codes`                        | Add a new SWIFT code entry for a specific country             | JSON body (see request structure below) |
| DELETE | `/v1/swift-codes/{swiftCode}`            | Delete a SWIFT code entry if it exists in the database        | `swiftCode` (e.g., `ABCDEF12XXX`)       |

### Request and Response Structures

#### GET /v1/swift-codes/{swiftCode}/
- **Request**:
  ```bash
  curl http://localhost:8080/v1/swift-codes/ABCDEF12XXX
  ```
- **Response (Headquarters)**:
  ```json
  {
      "swiftCode": "string",
      "bankName": "string",
      "countryISO2": "string",
      "countryName": "string",
      "address": "string",
      "isHeadquarter": true,
      "branches": [
          {
              "swiftCode": "string",
              "bankName": "string",
              "countryISO2": "string",
              "address": "string",
              "isHeadquarter": false
          },
          ...
      ]
  }
  ```
- **Response (Branch)**:
  ```json
  {
      "swiftCode": "string",
      "bankName": "string",
      "countryISO2": "string",
      "countryName": "string",
      "address": "string",
      "isHeadquarter": false
  }
  ```

#### GET /v1/swift-codes/country/{countryISO2}/
- **Request**:
  ```bash
  curl http://localhost:8080/v1/swift-codes/country/PL
  ```
- **Response**:
  ```json
  {
      "countryISO2": "string",
      "countryName": "string",
      "swiftCodes": [
          {
              "swiftCode": "string",
              "bankName": "string",
              "countryISO2": "string",
              "address": "string",
              "isHeadquarter": boolean
          },
          ...
      ]
  }
  ```

#### POST /v1/swift-codes/
- **Request**:
  ```bash
  curl -X POST http://localhost:8080/v1/swift-codes \
       -H "Content-Type: application/json" \
       -d '{
           "swiftCode": "ABCDEF12XXX",
           "bankName": "Example Bank",
           "countryISO2": "PL",
           "countryName": "POLAND",
           "address": "123 Main St, Warsaw",
           "isHeadquarter": true
       }'
  ```
- **Request Structure**:
  ```json
  {
      "swiftCode": "string",
      "bankName": "string",
      "countryISO2": "string",
      "countryName": "string",
      "address": "string",
      "isHeadquarter": boolean
  }
  ```
- **Response**:
  ```json
  {
      "message": "SWIFT code created successfully"
  }
  ```

#### DELETE /v1/swift-codes/{swiftCode}/
- **Request**:
  ```bash
  curl -X DELETE http://localhost:8080/v1/swift-codes/ABCDEF12XXX
  ```
- **Response**:
  ```json
  {
      "message": "SWIFT code deleted successfully"
  }
  ```

## Notes
- The SWIFT codes datasheet must be in `.csv` format with the following columns:
  - `SWIFT CODE`: The SWIFT code (e.g., `ABCDEF12XXX`).
  - `NAME`: The name of the bank.
  - `ADDRESS`: The address of the branch or headquarters.
  - `COUNTRY ISO2 CODE`: The ISO-2 country code (e.g., `PL`).
  - `COUNTRY NAME`: The full country name (e.g., `POLAND`).
- Country codes and names are stored and returned as uppercase strings.
- SWIFT codes ending with `XXX` are treated as headquarters; others are branches linked to headquarters by their first 8 characters.
- Redundant columns in the CSV are ignored during parsing.
- The API is accessible at `http://localhost:8080` as specified.
