# FastAPI API Project


# Rent & Sell Yacht API

This project is an API for renting and selling yachts. The API allows users to register accounts, book yachts, leave reviews, view available yachts, sell yachts, and manage their user data. Administrative access is also enabled to manage users, yachts, and bookings.

## API Functionality

### 1. **Authentication and Registration**
- **POST /auth/register**: Allows users to register.
- **POST /auth/login**: Allows users to log in and receive a JWT token for further interactions with the API.

### 2. **User Account**
- **GET /user/show**: Displays user information.
- **POST /user/upload-picture**: Allows users to upload their profile picture.

### 3. **Yacht**
- **GET /yacht**: Displays a list of yachts with filters.
- **GET /yacht/{id}**: Displays yacht details.

### 4. **Yacht Rentals**
- **POST /rents**: Allows users to book a yacht for rent.
- **DELETE /rents/{rent_id}**: Allows users to cancel a booking.
- **GET /yacht/{id}/active-rents**: Displays active rentals for a yacht.

### 5. **Reviews**
- **POST /reviews**: Allows users to leave reviews for yachts.
- **DELETE /reviews/{review_id}**: Allows users to delete their reviews.

### 6. **Yacht Sales**
- **POST /sale**: Allows users to sell their yachts.
- **GET /sale/my-sales**: Displays all sales by the user.

### 7. **Status**
- **GET /status**: Displays all statuses.

## Admin Routes

These routes are restricted to admin users and provide functionality to manage users, yachts, and other aspects of the platform.

### 1. **User Management**
- **GET /user/all-users**: View all registered users. *(Admin only)*
- **GET /user/{id}**: View user information by ID. *(Admin only)*
- **DELETE /user/{id}**: Ban a user by ID. *(Admin only)*
- **POST /user/{id}/admin**: Grant admin privileges to a user by ID. *(Admin only)*

### 2. **Yacht Management**
- **POST /yacht**: Add a new yacht. *(Admin only)*
- **PUT /yacht/{id}**: Update yacht details. *(Admin only)*
- **DELETE /yacht/{id}**: Delete a yacht by ID. *(Admin only)*
- **POST /yacht/{id}/upload-image**: Upload an image for a yacht. *(Admin only)*

### 3. **Status Management**
- **POST /status**: Allows admin to create new status.

## Technologies

This project uses the following technologies:
- **FastAPI**: Web framework for building APIs quickly.
- **SQLAlchemy**: ORM for database interactions.
- **Pydantic**: Data validation.
- **MySQL**: Database for storing data.
- **JWT**: For user authentication and authorization.
- **Alembic**: Database migrations.


## Requirements

Before you start, ensure you have the following installed on your machine:

- Python 3.12 or higher
- pip 22.0.4 or higher (Python package manager)
- A database system compatible with your project

## Setting Up the Project Locally

Follow these steps to set up and run the project:

### 1. Clone the Repository

```bash
git clone https://github.com/PopovicJovan/devlab-final-fapi.git
cd devlab-final-fapi
```

### 2. Create a virtual environment
```bash
python3 -m venv .venv
```
- to activate virtual environment run:
    ```bash
    source .venv/bin/activate
    ```
### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the database
- Update the database configuration files (e.g., settings.py or .env).

### 5. Create and configure environment file
```bash
cp app/.env.example app/.env
```

### 6. Run database migrations
```bash
alembic upgrade head
```

### 7. Run server
```bash
fastapi dev app/main.py
```
![er_fastapi](https://github.com/user-attachments/assets/5c168237-2056-480a-bb7e-c932415acca5)
