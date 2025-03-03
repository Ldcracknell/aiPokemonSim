import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the main function from the GUI version
from src.gui_battle import main

if __name__ == "__main__":
    main() 