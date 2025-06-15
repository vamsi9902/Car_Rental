# home.py
import subprocess
import sys
import os

def main():
    subprocess.Popen([sys.executable, os.path.join(os.getcwd(), 'login.py')])

if __name__ == "__main__":
    main()