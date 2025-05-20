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

2. Create and activate a virtual environment:
```bash
# On Windows
python -m venv env
.\env\Scripts\activate

# On Unix/Linux/MacOS
python -m venv env
source env/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

5. Update the `.env` file with your configuration:
- Set your database URL
- Set your JWT secret key
- Set your Firebase credentials path (if using Firebase)
- Configure other environment variables as needed

## Development

1. Start the development server:
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
├── gunicorn_conf.py   # Production server configuration
├── .env               # Environment variables (not in git)
├── .env.example       # Environment variables template
├── models/            # SQLAlchemy models
├── routers/           # API routes
└── schemas/           # Pydantic models
```

## Production Deployment

### 1. Environment Setup

1. Set up a production environment:
```bash
python -m venv env
source env/bin/activate  # or .\env\Scripts\activate on Windows
pip install -r requirements.txt
```

2. Configure environment variables:
- Copy `.env.example` to `.env`
- Update all variables with production values
- Set `DEBUG=False`
- Configure proper `ALLOWED_ORIGINS`

### 2. Database Setup

1. Set up PostgreSQL:
```bash
# Create database
createdb rtc_league

# Run migrations (if using Alembic)
alembic upgrade head
```

### 3. Running in Production

1. Using Gunicorn (recommended):
```bash
gunicorn -c gunicorn_conf.py main:app
```

2. Using Uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 4. SSL/TLS Configuration

1. Obtain SSL certificates (e.g., from Let's Encrypt)
2. Update `gunicorn_conf.py` with SSL settings:
```python
keyfile = "/path/to/privkey.pem"
certfile = "/path/to/fullchain.pem"
```

### 5. Process Management

1. Using systemd (Linux):
```ini
[Unit]
Description=RTC League API
After=network.target

[Service]
User=your_user
Group=your_group
WorkingDirectory=/path/to/app
Environment="PATH=/path/to/app/env/bin"
ExecStart=/path/to/app/env/bin/gunicorn -c gunicorn_conf.py main:app
Restart=always

[Install]
WantedBy=multi-user.target
```

2. Using Supervisor:
```ini
[program:rtc_league]
command=/path/to/app/env/bin/gunicorn -c gunicorn_conf.py main:app
directory=/path/to/app
user=your_user
autostart=true
autorestart=true
stderr_logfile=/var/log/rtc_league.err.log
stdout_logfile=/var/log/rtc_league.out.log
```

### 6. Monitoring and Logging

1. Set up proper logging:
- Application logs
- Access logs
- Error logs

2. Monitor the application:
- System resources (CPU, Memory, Disk)
- Application metrics
- Error rates

### 7. Backup Strategy

1. Database backups:
```bash
pg_dump rtc_league > backup.sql
```

2. Regular backup schedule:
- Daily incremental backups
- Weekly full backups
- Monthly archives

## Security Considerations

1. Keep all dependencies updated
2. Use strong passwords and secrets
3. Enable HTTPS
4. Configure proper CORS settings
5. Implement rate limiting
6. Regular security audits

## License

[Your License Here] 