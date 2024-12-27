import pandas as pd
import numpy as np
import logging
import os


class InnerMatrixProduction:
    # Initialize the RREF processor with paths for input and output files
    def __init__(self, read_path, write_path):
        self.read_path = read_path
        self.write_path = write_path

        # Configure logging
        log_directory = os.path.dirname(write_path)
        log_file = os.path.join(log_directory, 'inner_matrix_operations.txt')  # Logging specific to this class
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger()

    # Process the matrix to reduce it to RREF and save the result
    def produce_matrix(self):
        try:
            # Read the matrix from the Excel file
            matrix = pd.read_excel(self.read_path, header=None).astype(float)

            # Check if the matrix is empty
            if matrix.empty:
                self.logger.info("Input file is empty.")
                print("The file is empty.")
                return

            num_rows = matrix.shape[0]  # Number of rows

            # Loop through each pivot row
            for pivot_row in range(num_rows):
                # Ensure the pivot is non-zero. If zero, swap with a lower row.
                if matrix.iloc[pivot_row, pivot_row] == 0:
                    for lower_row in range(pivot_row + 1, num_rows):
                        if matrix.iloc[lower_row, pivot_row] != 0:
                            # Swap rows
                            matrix.iloc[[pivot_row, lower_row]] = matrix.iloc[[lower_row, pivot_row]].values
                            self.logger.info(f"Swapped row {pivot_row} with row {lower_row} to make pivot non-zero.")
                            break
                    else:
                        # If no non-zero pivot found, skip this column
                        self.logger.warning(f"Column {pivot_row} has no valid pivot. Skipping...")
                        print(f"Column {pivot_row} has no valid pivot. Skipping...")
                        continue

                # Normalize the pivot row
                pivot_value = matrix.iloc[pivot_row, pivot_row]
                matrix.iloc[pivot_row, :] /= pivot_value
                self.logger.info(f"Normalized row {pivot_row} with pivot value {pivot_value}.")

                # Eliminate all other entries in the pivot column
                for target_row in range(num_rows):
                    if target_row != pivot_row:  # Skip the pivot row itself
                        multiplier = matrix.iloc[target_row, pivot_row]
                        matrix.iloc[target_row, :] -= multiplier * matrix.iloc[pivot_row, :]
                        self.logger.info(
                            f"Eliminated column {pivot_row} in row {target_row} using multiplier {multiplier}.")

            # Log the resulting matrix
            self.logger.info("Final RREF matrix computed:")
            self.logger.info("\n" + str(matrix))
            print("Final RREF Matrix:")
            print(matrix)

            # Save the resulting matrix to an Excel file
            matrix.to_excel(self.write_path, index=False, header=False)
            print(f"RREF matrix saved to {self.write_path}")
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
            print(f"An error occurred: {e}")
