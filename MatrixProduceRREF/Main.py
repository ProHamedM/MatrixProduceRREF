import numpy as np
from LinearSystemSolver import LinearSystemSolver  # Import the parser class

# Main function to handle different phases of the project
def main():
    while True:
        print("\n--- Matrix Operations Menu ---")
        print("1. Solve a system of linear equations")
        print("2. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            print("\n--- Solve a Linear System ---")
            parser = LinearSystemSolver()  # Create an instance of the parser (handles input)
            parser.parse_equations()  # Parse the system provided by the user

            # Retrieve matrices from the parser
            coefficient_matrix, constant_vector = parser.get_matrices()

            print("\nCoefficient Matrix (coefficient_matrix):")
            print(coefficient_matrix)
            print("\nConstant Vector (constant_vector):")
            print(constant_vector)

            # Delegate the solving process to the parser
            try:
                solution = np.linalg.solve(coefficient_matrix, constant_vector)
                print("\nSolution Vector (x):")
                print(solution)
            except np.linalg.LinAlgError as e:
                print(f"Error: Cannot solve the system ({e}).")
        elif choice == "2":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()