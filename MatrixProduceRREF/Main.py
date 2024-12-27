import numpy as np
from LinearSystemSolver import LinearSystemSolver  # Import the solver class
from InnerMatrixProduction import InnerMatrixProduction     # Import the RREFMatrix class
import os

class Main:
    # Private attribute
    _log_path = None

    # Setter for the log path
    @classmethod
    def set_log_path(cls, path):
        if not path:  # Validate the path
            raise ValueError("Log path cannot be empty.")
        cls._log_path = path

    # Getter for the log path
    @classmethod
    def get_log_path(cls):
        return cls._log_path

    # Main function to handle different phases of the project
    @staticmethod
    def main():
        while True:

            # Ask client paths
            _log_path = input('Please choose where to save Log file?').strip() # Remove extra spaces
            if not os.path.exists(_log_path):
                os.makedirs(_log_path)
                print(f"Directory {_log_path} created.")
            Main.set_log_path(_log_path)  # Set the log path

            print("\n--- Matrix Operations Menu ---")
            print("1. Solve a system of linear equations")
            print("2. Exit")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                print("\n--- Solve a Linear System ---")

                # Solve the system and save matrices
                solver = LinearSystemSolver(_log_path)          # Create an instance of the solver (handles input)
                solver.parse_equations()                        # Parse the system provided by the user
                excel_file = solver.save_to_excel(_log_path)    # No need to pass the path explicitly; it's stored in log_path

                # Retrieve matrices from the solver
                coefficient_matrix, constant_vector = solver.get_matrices()

                print("\nCoefficient Matrix (coefficient_matrix):")
                print(coefficient_matrix)
                print("\nConstant Vector (constant_vector):")
                print(constant_vector)

                # Use InnerMatrixProduction to process RREF
                print("\n--- Reducing the System to RREF ---")
                rref_output_file = os.path.join(_log_path, "RREF_Result.xlsx")      # RREF result file
                rref_processor = InnerMatrixProduction(read_path=excel_file, write_path=rref_output_file)
                rref_processor.produce_matrix()                 # Process the RREF and save the result

                print(f"The RREF matrix has been saved to: {rref_output_file}")

                """
                # Delegate the solving process to the solver
                try:
                    solution = np.linalg.solve(coefficient_matrix, constant_vector)
                    print("\nSolution Vector (x):")
                    print(solution)
                except np.linalg.LinAlgError as e:
                    print(f"Error: Cannot solve the system ({e}).")
                """
            elif choice == "2":
                print("Exiting the program. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    Main.main()