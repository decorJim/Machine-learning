import os
import subprocess

# Define the project name and environment folder
PROJECT_NAME = "breast_cancer_wiscosin"
VENV_DIR = f"{PROJECT_NAME}_env"

# Detect OS for platform-specific paths
IS_WINDOWS = os.name == "nt"
VENV_PYTHON = os.path.join(VENV_DIR, "Scripts", "python.exe") if IS_WINDOWS else os.path.join(VENV_DIR, "bin", "python")
ACTIVATE_CMD = f"{VENV_DIR}\\Scripts\\activate" if IS_WINDOWS else f"source {VENV_DIR}/bin/activate"

def run_command(command):
    """Runs a shell command and prints output."""
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")

def create_venv():
    """Creates a virtual environment if it doesn't exist."""
    if not os.path.exists(VENV_DIR):
        print(f"🔹 Creating virtual environment: {VENV_DIR}")
        run_command(f"python -m venv {VENV_DIR}")
    else:
        print(f"✅ Virtual environment already exists: {VENV_DIR}")

def install_packages():
    """Installs required Python packages."""
    print(f"🔹 Installing Jupyter and dependencies...")
    run_command(f"{VENV_PYTHON} -m pip install --upgrade pip")
    run_command(f"{VENV_PYTHON} -m pip install jupyter ipykernel")

def register_kernel():
    """Registers the Jupyter kernel if not already registered."""
    print(f"🔹 Registering Jupyter kernel for {PROJECT_NAME}...")
    kernel_name = PROJECT_NAME.replace("-", "_")  # Replace invalid characters
    display_name = f"Python ({PROJECT_NAME.replace('-', ' ').title()})"

    # Use double quotes for Windows and escape properly
    if os.name == "nt":
        run_command(f'{VENV_PYTHON} -m ipykernel install --user --name={kernel_name} --display-name "{display_name}"')
    else:
        run_command(f"{VENV_PYTHON} -m ipykernel install --user --name={kernel_name} --display-name '{display_name}'")


def check_kernel_exists():
    """Checks if the kernel is already registered."""
    try:
        result = subprocess.run(["jupyter", "kernelspec", "list"], capture_output=True, text=True)
        return PROJECT_NAME in result.stdout
    except FileNotFoundError:
        return False

if __name__ == "__main__":
    create_venv()  # Step 1: Check if the virtual environment exists
    install_packages()  # Step 2: Install dependencies (skips redundant steps)
    if not check_kernel_exists():
        register_kernel()  # Step 3: Register the Jupyter kernel only if needed
    else:
        print(f"✅ Jupyter kernel already registered: Python ({PROJECT_NAME})")

    print("\n🎉 Setup complete! To activate the environment, run:")
    print(f"{ACTIVATE_CMD}  # Then launch Jupyter with: jupyter lab")
