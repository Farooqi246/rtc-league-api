import os
import shutil
import subprocess
import sys

def create_virtual_environment():
    """Create a virtual environment if it doesn't exist."""
    if not os.path.exists('env'):
        print("Creating virtual environment...")
        subprocess.run([sys.executable, '-m', 'venv', 'env'])
    else:
        print("Virtual environment already exists.")

def install_requirements():
    """Install required packages."""
    print("Installing requirements...")
    if os.name == 'nt':  # Windows
        subprocess.run(['env\\Scripts\\pip', 'install', '-r', 'requirements.txt'])
    else:  # Unix/Linux/MacOS
        subprocess.run(['env/bin/pip', 'install', '-r', 'requirements.txt'])

def create_env_file():
    """Create .env file if it doesn't exist."""
    if not os.path.exists('.env'):
        print("Creating .env file...")
        with open('.env', 'w') as f:
            f.write("""# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/dbname

# JWT Configuration
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Firebase Configuration (if needed)
FIREBASE_CREDENTIALS_PATH=path/to/your/firebase-credentials.json
""")
        print("Please update the .env file with your actual configuration values.")

def create_directories():
    """Create necessary directories if they don't exist."""
    directories = ['logs', 'data']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

def main():
    """Main build function."""
    print("Starting build process...")
    
    # Create virtual environment
    create_virtual_environment()
    
    # Install requirements
    install_requirements()
    
    # Create .env file
    create_env_file()
    
    # Create necessary directories
    create_directories()
    
    print("\nBuild completed successfully!")
    print("\nTo run the application:")
    print("1. Update the .env file with your configuration")
    print("2. Activate the virtual environment:")
    if os.name == 'nt':  # Windows
        print("   .\\env\\Scripts\\activate")
    else:  # Unix/Linux/MacOS
        print("   source env/bin/activate")
    print("3. Run the application:")
    print("   uvicorn main:app --reload")

if __name__ == "__main__":
    main() 