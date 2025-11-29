def calculate_fibonacci(n):
    """Calculate the nth Fibonacci number using recursion."""
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

def main():
    """Main function to demonstrate Fibonacci calculation."""
    for i in range(10):
        print(f"Fibonacci({i}) = {calculate_fibonacci(i)}")

if __name__ == "__main__":
    main()
