import sys
from src.app import Assignment3 as App

WINDOW_WIDTH = int(sys.argv[1])
WINDOW_HEIGHT = int(sys.argv[2])

def main():
    app = App(WINDOW_WIDTH, WINDOW_HEIGHT, "CS3388B - Assignment 3")
    app()
    
if __name__ == "__main__":
    main()
