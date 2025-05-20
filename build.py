import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command):
    """Run a shell command and print its output."""
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(f"Error: {e.stderr}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist."""
    env_path = Path('.env')
    if not env_path.exists():
        env_content = """# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/rtc_league

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Firebase Configuration
FIREBASE_CREDENTIALS_PATH=path/to/your/firebase-credentials.json

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# CORS Configuration
ALLOWED_ORIGINS=*

# Security Configuration
CORS_ORIGINS=*
CORS_METHODS=*
CORS_HEADERS=*

# Logging Configuration
LOG_LEVEL=INFO
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60

# Cache Configuration
CACHE_TTL=3600
CACHE_TYPE=simple

# Email Configuration (if needed)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-specific-password

# Redis Configuration (if using Redis)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Backup Configuration
BACKUP_DIR=backups
BACKUP_RETENTION_DAYS=30

# Monitoring Configuration
ENABLE_METRICS=True
METRICS_PORT=9090

# API Configuration
API_PREFIX=/api/v1
API_TITLE=RTC League API
API_VERSION=1.0.0
"""
        with open(env_path, 'w') as f:
            f.write(env_content)
        print("Created .env file with default configuration")
    else:
        print(".env file already exists")

def setup_virtual_environment():
    """Create and activate virtual environment."""
    venv_name = "env"
    if not Path(venv_name).exists():
        print(f"Creating virtual environment: {venv_name}")
        run_command(f"{sys.executable} -m venv {venv_name}")
    else:
        print(f"Virtual environment {venv_name} already exists")

def install_dependencies():
    """Install required packages."""
    print("Installing dependencies...")
    if platform.system() == "Windows":
        pip_cmd = f".\\env\\Scripts\\pip"
    else:
        pip_cmd = f"source env/bin/activate && pip"
    
    run_command(f"{pip_cmd} install --upgrade pip")
    run_command(f"{pip_cmd} install -r requirements.txt")

def create_directories():
    """Create necessary directories."""
    directories = [
        "logs",
        "backups",
        "uploads",
        "temp"
    ]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"Created directory: {directory}")

def main():
    """Main build function."""
    print("Starting build process...")
    
    # Create virtual environment
    setup_virtual_environment()
    
    # Install dependencies
    install_dependencies()
    
    # Create .env file
    create_env_file()
    
    # Create necessary directories
    create_directories()
    
    print("\nBuild completed successfully!")
    print("\nNext steps:")
    print("1. Update the .env file with your specific configuration")
    print("2. Activate the virtual environment:")
    if platform.system() == "Windows":
        print("   .\\env\\Scripts\\activate")
    else:
        print("   source env/bin/activate")
    print("3. Start the application:")
    print("   uvicorn main:app --reload")

if __name__ == "__main__":
    main() 