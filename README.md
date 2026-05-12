# Tasks App

A modern, asynchronous RESTful API built with FastAPI for managing tasks. This application provides a complete task management system with CRUD operations, pagination, and is designed for scalability with an async-first architecture.

## Features

- **FastAPI Framework**: Built with FastAPI for high-performance async APIs
- **PostgreSQL Database**: Uses async SQLAlchemy with PostgreSQL for data persistence
- **CRUD Operations**: Complete Create, Read, Update, Delete functionality for tasks
- **Pagination**: Built-in pagination support with customizable limits
- **Database Migrations**: Alembic for managing database schema changes
- **Modular Architecture**: Organized into separate modules (tasks, auth, aws)
- **Error Handling**: Comprehensive error handling with appropriate HTTP status codes
- **Logging**: Configured logging for development and production
- **Environment Configuration**: Uses python-dotenv for environment variable management

## Tech Stack

- **Backend**: FastAPI, Python 3.12+
- **Database**: PostgreSQL with asyncpg driver
- **ORM**: SQLAlchemy 2.0+
- **Migrations**: Alembic
- **Validation**: Pydantic
- **Server**: Uvicorn ASGI server

## Installation

### Prerequisites

- Python 3.12 or higher
- PostgreSQL database

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/tasks_app.git
   cd tasks_app
   ```

2. **Install Poetry (if not already installed):**
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. **Install dependencies:**
   ```bash
   poetry install
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory:
   ```
   PG_DATABASE_URL_ASYNC=postgresql+asyncpg://username:password@localhost:5432/tasks_db
   ```

5. **Run database migrations:**
   ```bash
   poetry run alembic upgrade head
   ```

6. **Start the application:**
   ```bash
   poetry run uvicorn src.main:app --reload
   ```

The API will be available at `http://localhost:8000`

## Usage

### API Endpoints

All endpoints are prefixed with `/api/v1/tasks`

#### Create a Task
```http
POST /api/v1/tasks
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Get milk, eggs, and bread",
  "is_completed": false
}
```

#### Get All Tasks (Paginated)
```http
GET /api/v1/tasks?page=1&limit=10
```

#### Get a Specific Task
```http
GET /api/v1/tasks/{task_id}
```

#### Update a Task
```http
PUT /api/v1/tasks/{task_id}
Content-Type: application/json

{
  "title": "Updated task title",
  "description": "Updated description",
  "is_completed": true
}
```

#### Delete a Task
```http
DELETE /api/v1/tasks/{task_id}
```

### Response Format

#### Task Object
```json
{
  "id": 1,
  "title": "Task title",
  "description": "Task description",
  "is_completed": false,
  "created_at": "2023-01-01T00:00:00Z"
}
```

#### Paginated Response
```json
{
  "items": [...],
  "total": 25,
  "page": 1,
  "limit": 10,
  "pages": 3,
  "has_next": true,
  "has_prev": false
}
```

## Project Structure

```
tasks_app/
├── src/
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py               # Configuration
│   ├── database.py             # Database setup
│   ├── models.py               # Global models
│   ├── pagination.py           # Pagination utilities
│   ├── exceptions.py           # Custom exceptions
│   ├── tasks/                  # Task management module
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── router.py
│   │   ├── services.py
│   │   ├── dependencies.py
│   │   ├── utils.py
│   │   ├── exceptions.py
│   │   └── constants.py
│   ├── auth/                   # Authentication module (in development)
│   ├── aws/                    # AWS integration module (in development)
│   └── paginador/              # Pagination schemas
├── alembic/                    # Database migrations
│   └── versions/               # Migration files
├── templates/                  # Frontend templates
├── tests/                      # Test suite
├── requirements/               # Dependency files
│   ├── base.txt                # Base dependencies
│   ├── dev.txt                 # Development dependencies
│   └── prod.txt                # Production dependencies
├── pyproject.toml              # Project metadata and dependencies
├── alembic.ini                 # Alembic configuration
├── logging.ini                 # Logging configuration
└── .env                        # Environment variables
```

## Configuration

### Environment Variables

- `PG_DATABASE_URL_ASYNC`: PostgreSQL connection string for async operations

### Database Configuration

The application uses async SQLAlchemy with PostgreSQL. Database sessions are managed through dependency injection.

### Pagination Settings

- Default limit: 10 items per page
- Maximum limit: 100 items per page

## Development

### Running Tests

```bash
# Run tests
poetry run pytest
```

### Database Migrations

```bash
# Create a new migration
poetry run alembic revision --autogenerate -m "Migration message"

# Apply migrations
poetry run alembic upgrade head

# Rollback
poetry run alembic downgrade -1
```

### API Documentation

When running the application, visit `http://localhost:8000/docs` for interactive API documentation powered by Swagger UI.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Database ORM with [SQLAlchemy](https://www.sqlalchemy.org/)
- Data validation with [Pydantic](https://pydantic-docs.helpmanual.io/)</content>