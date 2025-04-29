import pyautogui
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python clicker.py <x> <y>")
        sys.exit(1)

    try:
        x = int(sys.argv[1])
        y = int(sys.argv[2])
        pyautogui.moveTo(x, y)
        pyautogui.click()
        pyautogui.click()
    except ValueError:
        print("Invalid coordinates.")
        sys.exit(1)

if __name__ == "__main__":
    main()