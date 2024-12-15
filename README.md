# FastAPI API Project

#### This is a FastAPI project.This document provides steps to set up and run the project locally.

## Prerequisites

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
