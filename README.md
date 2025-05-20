# RTC League API

This is the API for the RTC League application, built with FastAPI.

## Prerequisites

- Python 3.8 or higher
- PostgreSQL database
- Firebase account (if using Firebase features)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Run the build script:
```bash
python build.py
```

3. Update the `.env` file with your configuration:
- Set your database URL
- Set your JWT secret key
- Set your Firebase credentials path (if using Firebase)

## Running the Application

1. Activate the virtual environment:
```bash
# On Windows
.\env\Scripts\activate

# On Unix/Linux/MacOS
source env/bin/activate
```

2. Start the application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:
- Swagger UI documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## Authentication

The API uses JWT token authentication. To get a token:

1. Send a POST request to `/token` with:
```json
{
    "email": "your.email@example.com",
    "password": "your_password"
}
```

2. Use the returned token in the Authorization header:
```
Authorization: Bearer your.jwt.token
```

## Project Structure

```
.
├── main.py              # Main application file
├── auth.py             # Authentication logic
├── database.py         # Database configuration
├── requirements.txt    # Python dependencies
├── build.py           # Build script
├── .env               # Environment variables
├── models/            # SQLAlchemy models
├── routers/           # API routes
└── schemas/           # Pydantic models
```

## Development

To add new features:
1. Create new models in `models/`
2. Create new schemas in `schemas/`
3. Create new routes in `routers/`
4. Update the main application in `main.py`

## Deployment

For production deployment:
1. Set appropriate environment variables
2. Use a production-grade ASGI server (e.g., Gunicorn)
3. Set up proper database backups
4. Configure SSL/TLS
5. Set up proper logging

## License

[Your License Here] 