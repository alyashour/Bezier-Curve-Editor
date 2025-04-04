import sys
from src.app import BezierApp

WINDOW_WIDTH = int(sys.argv[1])
WINDOW_HEIGHT = int(sys.argv[2])

def main():
    app = BezierApp(WINDOW_WIDTH, WINDOW_HEIGHT, "Bezier Curve Editor")
    app()
    
if __name__ == "__main__":
    main()
