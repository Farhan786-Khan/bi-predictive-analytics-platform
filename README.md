python setup_and_run.py
import os
import sys
import subprocess

REPO_URL = "https://github.com/Farhan786-Khan/bi-predictive-analytics-platform.git"
REPO_NAME = "bi-predictive-analytics-platform"

def run_command(cmd, shell=True):
    print(f"\nRunning: {cmd}")
    result = subprocess.run(cmd, shell=shell)
    if result.returncode != 0:
        print(f"Error running command: {cmd}")
        sys.exit(1)

def main():
    # Step 1: Clone repo
    if not os.path.isdir(REPO_NAME):
        run_command(f"git clone {REPO_URL}")
    os.chdir(REPO_NAME)

    # Step 2: Create & activate virtual env
    if not os.path.isdir(".venv"):
        run_command("python3 -m venv .venv")
    if sys.platform.startswith("win"):
        venv_activate = ".venv\\Scripts\\activate"
    else:
        venv_activate = "source .venv/bin/activate"
    print(f"\nActivate your virtual environment:\n{venv_activate}\n")

    # Step 3: Install requirements
    if os.path.isfile("requirements.txt"):
        run_command("pip install -r requirements.txt")
    else:
        print("requirements.txt not found!")

    # Step 4: Run main pipeline
    if os.path.isfile("src-main.py"):
        run_command("python src-main.py")
    else:
        print("src-main.py not found!")

    # Step 5: Train or run a model
    if os.path.isfile("prophet-model.py"):
        run_command("python prophet-model.py")
    else:
        print("prophet-model.py not found!")

if __name__ == "__main__":
    main()
