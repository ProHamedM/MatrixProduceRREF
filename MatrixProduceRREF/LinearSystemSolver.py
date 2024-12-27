import re
import logging
import numpy as np
import pandas as pd
import os

# Class for parsing a system of linear equations
class LinearSystemSolver:

    # Initialize the parser by prompting the user for equations.
    def __init__(self, log_path):

        # Initialize the solver with a LogManager instance
        self.log_path = log_path

        # Configure logging dynamically based on log_path
        log_file = os.path.join(self.log_path, "linearSystemLog.txt")       # Create the path for the log file
        logging.basicConfig(
            filename=log_file,                                              # Log file name
            level=logging.INFO,                                             # Logging level
            format='%(asctime)s - %(levelname)s - %(message)s'              # Log entry format
        )
        self.logger = logging.getLogger()

        # Logging initialization
        self.logger.info("LinearSystemSolver initialized.")

        print("Enter your linear equations one by one.")
        print("Type 'done' when you finish entering all equations.")
        equations = []  # Initialize empty list for equations

        while True:
            equation = input("Equation: ").strip()  # Get input and remove extra spaces
            if equation.lower() == 'done':  # Break loop if user types 'done'
                break
            equations.append(equation)  # Add equation to the list

        self.equations = equations  # Store equations provided by the user
        self.variables = []         # List to store unique variables
        self.coefficients = []      # List to store coefficients from equations
        self.constants = []         # List to store constants from equations

        self.logger.info("Equations received from user.")

    # Parse the input equations to extract variables, coefficients, and constants.
    def parse_equations(self):

        # Log parsing process
        self.logger.info("Parsing equations...")

        # Set to store variables without duplicates
        variable_set = set()

        # Regular expressions:
        # term_pattern: Match terms like '2x', '-y', '3.5z'
        term_pattern = re.compile(r"([+-]?\d*\.?\d*)\s*([a-zA-Z]+)")
        # constant_pattern: Match the constant part after '='
        constant_pattern = re.compile(r"=\s*([+-]?\d+\.?\d*)")

        # Process each equation in the input list
        for equation in self.equations:
            coefficient_dictionary = {}  # Temporary dictionary to store coefficients of this equation

            # Extract coefficients and variables
            for term in term_pattern.findall(equation):
                coefficient, var = term  # Split coefficient and variable (e.g., '2x' -> '2', 'x')

                # Handle cases where the coefficient is missing or is just '+' or '-'
                if coefficient in ["+", "-"]:
                    coefficient += "1"  # Convert '+' to '+1' and '-' to '-1'
                coefficient = float(coefficient) if coefficient else 1.0 # Default to 1.0 if coefficient is empty

                coefficient_dictionary[var] = coefficient  # Store in dictionary with variable as key
                variable_set.add(var)   # Add variable to the set

            # Extract constant value
            constant_match = constant_pattern.search(equation)  # Look for '= constant'
            if not constant_match:  # If '=' or constant is missing, raise an error
                raise ValueError("Invalid equation format. Missing constant value.")
            constant = float(constant_match.group(1))  # Extract constant as a float

            # Append extracted constant and coefficient dictionary to respective lists
            self.constants.append(constant)
            self.coefficients.append(coefficient_dictionary)

        # Sort variables alphabetically (for consistent ordering)
        self.variables = sorted(variable_set)

        # Build coefficient matrix and constant vector
        self._build_matrices()

        self.logger.info("Equations parsed successfully.")

    # Construct the coefficient matrix (A) and constant vector (b) from parsed data.
    def _build_matrices(self):

        # Determine the dimensions of the matrices
        num_equations = len(self.equations)  # Number of equations
        num_variables = len(self.variables) # Number of unique variables

        # Initialize the coefficient matrix with zeros
        coefficient_matrix = np.zeros((num_equations, num_variables))
        # Convert constants list to a NumPy array
        constant_vector = np.array(self.constants)

        # Populate the coefficient matrix row by row
        for count_one, coefficient_dictionary in enumerate(self.coefficients):
            for count_two, var in enumerate(self.variables):
                # Fill matrix with coefficients (default to 0 if variable is missing)
                coefficient_matrix[count_one, count_two] = coefficient_dictionary.get(var, 0)

        # Store matrices as instance attributes
        self.coefficient_matrix = coefficient_matrix
        self.constant_vector = constant_vector

        self.logger.info("Matrices constructed successfully.")

    def get_matrices(self):
        """
        Return the coefficient matrix and constant vector.
        :return: Tuple (coefficient_matrix, constant_vector)
        """
        return self.coefficient_matrix, self.constant_vector

    # Save the coefficient matrix and constant vector to an Excel file in the log_path directory.
    def save_to_excel(self, output_directory):
        try:
            # Prepare DataFrame for the full augmented matrix (coefficients | constants)
            augmented_matrix = np.hstack([self.coefficient_matrix, self.constant_vector.reshape(-1, 1)])
            dataframe = pd.DataFrame(augmented_matrix)

            # Construct the output file path using the log_path
            output_path = os.path.join(self.log_path, 'LinearSystem.xlsx')

            # Save DataFrame to Excel
            dataframe.to_excel(output_path, index=False, header=False)

            print(f"Matrix saved to {output_path}")
            return output_path
        except Exception as exception:
            print(f"An error occurred while saving the matrix: {exception}")
            raise