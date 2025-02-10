# 🎉 Hackathon Badge Scanning System

## 🗂 Project Overview

This project is a Flask-based RESTful API that allows for user management, activity tracking, and scan records to be used in a hackathon!

## ⚙️ Setup Instructions

### 🔧 Prerequisites

- Python 3.x
- Flask
- SQLAlchemy
- SQLite
- Additional required libraries specified in `requirements.txt`

### 🛠 Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```bash
   cd <project-directory>
   ```

3. Run and build Docker Container
   ```bash
    docker-compose up --build
   ```
   If this is your first time running the app, a database.db file should automatically create in the data folder and data will be loaded into it.
   Data will only load if you do not have tables set up or your tables are empty.

### 📊 OPTIONAL: To view the data in your tables
1. Access the shell

   ```bash
   docker exec -it api-new /bin/bash
   ```
2. Uses sqlite3
  ```bash
  sqlite3 data/database.db
  ```
3. Run your SQL commands (for example)

  View tables
    ```bash
    .tables
    ```
  View user data 
  ```bash
  SELECT * FROM user;
  ```

The API will start running at `http://localhost:3000`.

## 🚀 API Endpoints

### 1. Get Users
- **Endpoint**: `GET /users`
- **Example query**: GET `http://localhost:3000/users`
- **Description**: Retrieves a list of all users in the database.
- **Response**: 
    ```json
    [
        {
            "id": 1,
            "email": "user@example.com",
            "name": "User One",
            "badge_code": "B123",
            "phone": "1234567890",
            "updated_at": "2025-02-09T12:00:00",
            "scans": [
                {
                    "activity_name": "Opening Ceremony",
                    "scanned_at": "2025-01-01T08:00:00",
                    "activity_category": "Event"
                }
            ]
        }
    ]
    ```
- **Status Codes**:
  - `200 OK` - Successful retrieval of users.

### 2. Get User by ID
- **Endpoint**: `GET /users/<int:user_id>`
- - **Example query**: GET `http://localhost:3000/users/100`
- **Description**: Retrieves details for a specific user identified by their unique ID.
- **Response**:
    ```json
    {
        "id": 1,
        "email": "user@example.com",
        "name": "User One",
        "badge_code": "B123",
        "phone": "1234567890",
        "updated_at": "2025-02-09T12:00:00",
        "scans": [
            {
                "activity_name": "Opening Ceremony",
                "scanned_at": "2025-01-01T08:00:00",
                "activity_category": "Event"
            }
        ]
    }
    ```
- **Status Codes**:
  - `200 OK` - User found.
  - `404 Not Found` - User with the specified ID does not exist.

### 3. Update User Data
- **Endpoint**: `PUT /users/<int:user_id>`
- **Example query**: PUT `http://localhost:3000/users/1`
- **Description**: Updates a user's information (e.g., name, phone, email, badge code) by their ID.
- **Request Body**:
    ```json
    {
        "phone": "+1 (555) 123 4567",
        "name": "John Doe"
    }
    ```
- **Response**:
    ```json
    {
        "id": 1,
        "email": "user@example.com",
        "name": "John Doe",
        "badge_code": "B123",
        "phone": "+1 (555) 123 4567",
        "updated_at": "2025-02-09T12:01:00",
        "scans": []
    }
    ```
- **Status Codes**:
  - `200 OK` - User updated successfully.
  - `400 Bad Request` - If attempts to set unexpected fields or if unique constraints are violated.
  - `404 Not Found` - If the user does not exist.

### 4. Add Scan Data
- **Endpoint**: `PUT /scan/<string:badge_code>`
- **Description**: Adds a new scan for a user identified by badge code.
- **Request Body**:
    ```json
    {
        "activity_name": "Sample Activity",
        "activity_category": "Workshop"
    }
    ```
- **Response**:
    ```json
    {
        "user_id": 1,
        "user_email": "user@example.com",
        "activity_name": "Sample Activity",
        "scanned_at": "2025-02-10T01:01:00",
        "activity_category": "Workshop"
    }
    ```
- **Status Codes**:
  - `201 Created` - Scan added successfully.
  - `400 Bad Request` - If required fields are missing in the request body.
  - `404 Not Found` - If no user corresponds to the provided badge code.
  
### 5. Get Scan Data
- **Endpoint**: `GET /scans`
- **Example query**: PUT `http://localhost:3000/scans?activity_category=meal&min_frequency=20&max_frequency=30`
- **Description**: Retrieves aggregated scan data based on optional filters.
- **Query Parameters**:
    - `min_frequency` (optional, int): Minimum number of scans to be included in the result.
    - `max_frequency` (optional, int): Maximum number of scans allowed.
    - `activity_category` (optional, str): The category of activities to filter by.

- **Response**:
    ```json
    [
        {
            "activity_name": "Sample Activity",
            "activity_category": "Workshop",
            "frequency": 10
        }
    ]
    ```
- **Status Codes**:
  - `200 OK` - Successful retrieval of scan data.

### ⚠️ Error Handling

- **HTTP Status Codes**: 
    - `200 OK`: Successful request.
    - `201 Created`: Resource successfully created.
    - `400 Bad Request`: Invalid input or unexpected fields.
    - `404 Not Found`: Requested resource does not exist.
    - `500 Internal Server Error`: An unexpected error occurred.

### Additional Notes

- **Validation**: Ensure all request data is validated before processing. Handle unexpected keys within the JSON request bodies to improve robustness.
- **Performance Considerations**: Utilize indexing on frequently queried fields to enhance query performance.
- **Eager Loading**: Consider using eager loading techniques (`joinedload` in SQLAlchemy) for related data if needed to optimize the performance of retrieving scans with users.

# 🧐 Assumptions and Challenges

## 🧠 Assumptions

- **Data Loading**:
  - The application only loads data from the JSON file if **all tables (users, activities, scans) are empty**. This avoids inefficiencies and unnecessary checks for duplicates every time the application starts.
  - It is assumed that the JSON file does not change frequently. The initial data load populates the database, and subsequent interactions will add or modify data through the provided endpoints.

- **User Update**:
  - The update functionality does not require returning scan information since scans remain unchanged and are not directly modified through the user update endpoint.

- **Data Integrity**:
  - There is no expectation for data cleaning in the incoming dataset, so the integrity of the source data is taken at face value.
  
- **Phone Number Format**:
  - The phone number formats in the input data can vary significantly, and there is no validation implemented for them at this time.

- **Badge Codes and Emails**:
  - It is assumed that at some point, there may be a need to change users' badge codes or emails. While changing emails makes sense, reassessing badge codes may not be practically necessary.
  - To ensure data integrity while allowing changes to these fields, an `id` field has been added as an immutable primary key, ensuring references remain stable even if the email or badge code changes.

- **Scan Requirement**:
  - The badge code is used as an identifier for scans. It is assumed that a user **must have a badge code** to create a scan. Therefore, activities can only be performed if the user possesses a valid badge.

## 😥 Challenges

- **Handling Empty Badge Codes**:
  - Badge codes can be represented as an empty string (`""`). There are considerations regarding how to handle this case based on the requirement.
  - After reviewing different scenarios, the design choice is made to treat `""` as `NULL` in the database to simplify handling.

- **Maintaining Uniqueness**:
  - The requirement to keep the badge code unique while allowing `None` (or `NULL` in the database) means that the field is retained as `unique`. 
  - The decision was made to ensure that the badge code must not be blank unless it is explicitly set to `NULL`.

- **Endpoint Responses**:
  - The response from the "Get All Users" endpoint includes an `id` and an `updated_at` timestamp. This means that the output will have slightly more data than what is presented in `example_data.json`.
  - Consequently, if you compare the total rows in the database output and the example JSON, there will be two additional fields (one for `id` and one for `updated_at`) per user, leading to an increase in data size.

- **Phone Number Cleaning**:
  - Future considerations include implementing phone number validation and cleaning to standardize formats before storing them in the database.


