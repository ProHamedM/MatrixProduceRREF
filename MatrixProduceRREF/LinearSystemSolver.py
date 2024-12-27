import re
import numpy as np

# Class for parsing a system of linear equations
class LinearSystemSolver:

    # Initialize the parser by prompting the user for equations.
    def __init__(self):

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

    # Parse the input equations to extract variables, coefficients, and constants.
    def parse_equations(self):

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

    def get_matrices(self):
        """
        Return the coefficient matrix and constant vector.
        :return: Tuple (coefficient_matrix, constant_vector)
        """
        return self.coefficient_matrix, self.constant_vector