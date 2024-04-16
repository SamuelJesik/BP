# test_script.py

def calculate_squares(n):
    return [i**2 for i in range(n)]

def main():
    squares = calculate_squares(10)
    print("Squares of numbers from 0 to 9:")
    for num, square in enumerate(squares):
        print(f"{num}^2 = {square}")

if __name__ == "__main__":
    main()