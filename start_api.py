import os
import sys
import subprocess
import importlib.util

# Get the absolute paths
root_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(root_dir, "tina-api")
venv_python = os.path.join(root_dir, "venv", "Scripts", "python.exe")

def check_and_install_package(package_name):
    """Check if a package is installed, install only if missing"""
    try:
        # Create a subprocess to check if the package is installed
        result = subprocess.run(
            [venv_python, "-c", f"import {package_name}; print('{package_name} is installed')"], 
            capture_output=True, 
            text=True
        )
        if f"{package_name} is installed" in result.stdout:
            print(f"{package_name} is already installed.")
            return True
        else:
            print(f"Installing {package_name}...")
            subprocess.check_call([venv_python, "-m", "pip", "install", package_name])
            print(f"{package_name} installed successfully.")
            return True
    except Exception as e:
        print(f"Error checking/installing {package_name}: {str(e)}")
        return False

def setup_env_file():
    """Create or update .env file with Azure OpenAI credentials"""
    env_path = os.path.join(root_dir, '.env')
    
    # Check if .env exists
    if not os.path.exists(env_path):
        # Create new .env file with placeholders for Azure OpenAI credentials
        with open(env_path, 'w') as f:
            f.write("AZURE_OPENAI_ENDPOINT=https://your-openai-endpoint.openai.azure.com/\n")
            f.write("AZURE_OPENAI_KEY=your-api-key-here\n")
            f.write("AZURE_OPENAI_DEPLOYMENT=new-azure-openai-gpt-4o\n")
            f.write("AZURE_OPENAI_API_VERSION=2024-12-01-preview\n")
        print("Created .env file with Azure OpenAI credential placeholders")
    else:
        # Check if Azure OpenAI credentials exist, add if not
        with open(env_path, 'r') as f:
            content = f.read()
        
        updates_needed = []
        if "AZURE_OPENAI_ENDPOINT=" not in content:
            updates_needed.append("AZURE_OPENAI_ENDPOINT=https://your-openai-endpoint.openai.azure.com/")
        if "AZURE_OPENAI_KEY=" not in content:
            updates_needed.append("AZURE_OPENAI_KEY=your-api-key-here")
        if "AZURE_OPENAI_DEPLOYMENT=" not in content:
            updates_needed.append("AZURE_OPENAI_DEPLOYMENT=new-azure-openai-gpt-4o")
        if "AZURE_OPENAI_API_VERSION=" not in content:
            updates_needed.append("AZURE_OPENAI_API_VERSION=2024-12-01-preview")
        
        if updates_needed:
            with open(env_path, 'a') as f:
                f.write('\n' + '\n'.join(updates_needed) + '\n')
            print("Updated .env file with Azure OpenAI credential placeholders")
        else:
            print("Azure OpenAI credentials already exist in .env file")

def start_api():
    """Start the FastAPI backend"""
    print("Starting the API server...")
    os.chdir(backend_dir)
    subprocess.call([venv_python, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])

if __name__ == "__main__":
    try:
        # Check and install required packages
        if check_and_install_package("uvicorn") and check_and_install_package("openai"):
            # Setup environment variables for Azure OpenAI
            setup_env_file()
            # Start the API
            start_api()
        else:
            print("Failed to ensure required packages are installed. Cannot start API.")
    except Exception as e:
        print(f"Error: {str(e)}")
        input("Press Enter to exit...")
