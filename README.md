# Room Inventory Microservice

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)
![Tableau](https://img.shields.io/badge/Tableau-E97627?style=for-the-badge&logo=tableau&logoColor=white)

## Overview

The Room Inventory Microservice is a vital component of the Hotel Kong Arthur management system, designed to handle all room-related operations efficiently. It provides comprehensive APIs for room management, including room types, availability tracking, and pricing management. The service implements a seasonal pricing strategy and maintains a relational database structure for optimal data organization.

**Key Features:**
- Room type management with base pricing
- Room availability tracking
- Seasonal price adjustment system
- RESTful API endpoints
- Docker containerization

## Project Structure

```bash
RoomInventoryService/
│
├── csv/
│   └── international_names_with_rooms_1000.csv  # Initial room data
│
├── db/
│   ├── pricing_constants.py          # Room pricing and seasonal multipliers
│   ├── connection.py                 # Database connection management
│   ├── initialize.py                 # Database initialization
│   ├── room_type_repository.py       # Room type operations
│   ├── room_repository.py            # Room operations
│   └── room_inventory.db            # SQLite database
│
├── .dockerignore                    # Docker ignore rules
├── .gitignore                       # Git ignore rules
├── app.py                          # Main Flask application
├── Dockerfile                      # Docker configuration
├── README.md                       # Project documentation
└── requirements.txt                # Python dependencies
```

The database module (`db/`) is organized into several Python modules for better separation of concerns:

- `pricing_constants.py`: Contains room pricing constants and seasonal multipliers
- `connection.py`: Handles database connection management
- `initialize.py`: Contains database initialization and setup functions
- `room_type_repository.py`: Handles all room type-related database operations
- `room_repository.py`: Handles all room-related database operations

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Python 3.x](https://www.python.org/downloads/) (for local development)
- [Postman](https://www.postman.com/downloads/) (for testing)

## Installation

### Docker Setup (Recommended)
```bash
docker build -t room-inventory-service .
docker run -d -p 5002:5002 --name room-inventory-service room-inventory-service
```

### Local Development Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Database Schema

```mermaid
erDiagram
    RoomTypes ||--o{ Rooms : contains
    RoomTypes {
        INTEGER id PK
        VARCHAR type_name UK
        REAL base_price
    }
    Rooms {
        INTEGER id PK
        INTEGER room_type_id FK
        INTEGER availability
    }
    Seasons {
        INTEGER id PK
        VARCHAR season_type UK
        REAL multiplier
    }
```


## API Documentation

| Method | Endpoint                     | Description             | Request Body                          | Response (200)                                                                                   | Error Responses                      |
|--------|-------------------------------|-------------------------|---------------------------------------|--------------------------------------------------------------------------------------------------|--------------------------------------|
| GET    | /api/v1/room_types            | Get all room types     | N/A                                   | `[{"id": 1, "type_name": "Standard Single", "base_price": 900}]`                                 | 404: `{"error": "No room types found"}` |
| GET    | /api/v1/room_type/{roomId}    | Get room type by ID    | N/A                                   | `{"id": 1, "type_name": "Standard Single", "base_price": 900}`                                   | 404: `{"error": "Room type not found"}` |
| POST   | /api/v1/room_type             | Add new room type      | `{"type_name": "Deluxe", "base_price": 1500}` | `{"message": "Room type added successfully"}`                                                 | 400: `{"error": "Missing required fields"}` |
| PATCH  | /api/v1/room_type/{roomId}/price | Update room price      | `{"base_price": 1600}`                | `{"message": "Price updated successfully"}`                                                     | 404: `{"error": "Room type not found"}` |
| GET    | /api/v1/rooms                 | Get all rooms          | N/A                                   | `[{"id": 1, "room_type_id": 1, "availability": 1, "type_name": "Standard Single", "base_price": 900}]` | 404: `{"error": "No rooms found"}`       |
| GET    | /api/v1/room/{roomId}         | Get room by ID         | N/A                                   | `{"id": 1, "room_type_id": 1, "availability": 1, "type_name": "Standard Single", "base_price": 900}` | 404: `{"error": "Room not found"}`       |
| PATCH  | /api/v1/room/{roomId}/availability | Update room availability| `{"availability": 0}`              | `{"message": "Room availability updated successfully"}`                                          | 404: `{"error": "Room not found"}`       |

## Room Types and Pricing System

The hotel implements a dynamic pricing system based on room types and seasonal demand. Each room type has a base price, which is adjusted using seasonal multipliers to optimize revenue based on demand patterns.

### Room Distribution (based on CSV)

The following table summarizes the distribution of room types based on the total bookings recorded. The hotel has a total of **214 rooms**, with varying amounts allocated to each type reflecting their luxury status and corresponding pricing.

| Room Type           | Number of Rooms | Number of Bookings | Base Price (DKK) |
|---------------------|------------------|---------------------|-------------------|
| Standard Single     | 50               | 117                 | 900               |
| Grand Lit           | 50               | 118                 | 1100              |
| Standard Double     | 40               | 117                 | 1200              |
| Superior Double     | 25               | 134                 | 1400              |
| Junior Suite        | 20               | 136                 | 1800              |
| Spa Executive       | 15               | 138                 | 2000              |
| Suite               | 10               | 137                 | 2500              |
| LOFT Suite          | 4                | 103                 | 3000              |
| **Total**           | **214**          | **1,000**           |                   |

- **Standard Single**, **Grand Lit**, and **Standard Double** are the most numerous, representing accessible luxury options.
- **Superior Double** and **Junior Suite** have a moderate number of rooms.
- **Spa Executive**, **Suite**, and **LOFT Suite** are the least available due to their higher luxury status.

### Seasonal Price Multipliers

```python
SEASONS = {
    'LOW': 0.8,
    'MID': 1.0,
    'HIGH': 1.2
}
```

## Testing

### Postman Collection

You can use the following API endpoints in Postman or any HTTP client to test the application.

#### 1. Get All Room Types
- **Method:** `GET`
- **Request:** `http://localhost:5002/api/v1/room_types`
- **Response Example:**
    ```json
    [
        {"id": 1, "type_name": "Standard Single", "base_price": 900},
        {"id": 2, "type_name": "Deluxe Suite", "base_price": 1500}
    ]
    ```

#### 2. Get Room Type by ID
- **Method:** `GET`
- **Request:** `http://localhost:5002/api/v1/room_type/1`
- **Response Example:**
    ```json
    {"id": 1, "type_name": "Standard Single", "base_price": 900}
    ```

#### 3. Add Room Type
- **Method:** `POST`
- **Request:** `http://localhost:5002/api/v1/room_type`
- **Request Body:**
    ```json
    {
        "type_name": "Supreme Deluxe",
        "base_price": 3000
    }
    ```
- **Response Example:**
    ```json
    {"message": "Room type added successfully"}
    ```

#### 4. Update Room Price
- **Method:** `PATCH`
- **Request:** `http://localhost:5002/api/v1/room_type/3/price`
- **Request Body:**
    ```json
    {
        "base_price": 1600
    }
    ```
- **Response Example:**
    ```json
    {"message": "Price updated successfully"}
    ```

#### 5. Get All Rooms
- **Method:** `GET`
- **Request:** `http://localhost:5002/api/v1/rooms`
- **Response Example:**
    ```json
    [
        {"id": 1, "room_type_id": 1, "availability": 1},
        {"id": 2, "room_type_id": 2, "availability": 0},
        {"id": 3, "room_type_id": 1, "availability": 0}
    ]
    ```

#### 6. Get Room by ID
- **Method:** `GET`
- **Request:** `http://localhost:5002/api/v1/room/10`
- **Response Example:**
    ```json
    {
        "id": 1,
        "room_type_id": 1,
        "availability": 1,
        "base_price": 900,
        "type_name": "Standard Single"
    }
    ```

#### 7. Update Room Availability
- **Method:** `PATCH`
- **Request:** `http://localhost:5002/api/v1/room/4/availability`
- **Request Body:**
    ```json
    {
        "availability": 0
    }
    ```
- **Response Example:**
    ```json
    {"message": "Room availability updated successfully"}
    ```

---

#### Created by Hotel Kong Arthur Team
