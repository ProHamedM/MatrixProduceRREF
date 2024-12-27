import pandas as pd
import logging
import os


# Ask client paths
read_path = input ('Please enter excel File\'s Path?').strip() # Remove extra spaces
write_path = input ('Please enter saving directory?').strip() # Remove extra spaces
# Convert paths to string
read_path = str(read_path)
write_path = str(write_path ) + '\Answer.xlsx'
print(write_path)


# Extract directory from the read_path
log_directory = os.path.dirname(read_path)  # Get the directory of the input file

# Configure the logger
log_file = os.path.join(log_directory, 'operations.txt')  # Create the path for the log file
logging.basicConfig(
    filename = log_file ,                                  # Log file name
    level = logging.INFO,                                  # Logging level
    format = '%(asctime)s - %(levelname)s - %(message)s'   # Log entry format
)



def produce_matrix ():
    global doc_matrix
    global temp_matrix
    global temp_num

    try:
        # Read matrix from Excel file
        doc_matrix = pd.read_excel(read_path, header=None).astype(float) # Disable header assumption & Set values Float

        # Check if DataFrame is empty
        if doc_matrix.empty:
            logging.info("Input file is empty.")
            print('The file is empty. :)')
        else:

            num_rows = doc_matrix.shape[0] # Number of rows

            # Loop through each pivot row
            for pivot_row in range(num_rows):

                # Ensure the pivot is non-zero. If zero, swap with a lower row.
                if doc_matrix.iloc[pivot_row, pivot_row] == 0:
                    for lower_row in range(pivot_row + 1, num_rows):
                        if doc_matrix.iloc[lower_row, pivot_row] != 0:
                            # Swap rows
                            doc_matrix.iloc[[pivot_row, lower_row]] = doc_matrix.iloc[[lower_row, pivot_row]].values
                            logging.info(f"Swapped row {pivot_row} with row {lower_row} to make pivot non-zero.")
                            break
                    else:
                        # If no non-zero pivot found, skip this column
                        logging.warning(f"Column {pivot_row} has no valid pivot. Skipping...")
                        print(f"Column {pivot_row} has no valid pivot. Skipping...")
                        continue

                # Normalize the pivot row
                pivot_value = doc_matrix.iloc[pivot_row, pivot_row]
                doc_matrix.iloc[pivot_row, :] /= pivot_value
                logging.info(f"Normalized row {pivot_row} with pivot value {pivot_value}.")

                # Eliminate all other entries in the pivot column
                for target_row in range(num_rows):
                    if target_row != pivot_row:  # Skip the pivot row itself
                        multiplier = doc_matrix.iloc[target_row, pivot_row]
                        doc_matrix.iloc[target_row, :] -= multiplier * doc_matrix.iloc[pivot_row, :]
                        logging.info(
                            f"Eliminated column {pivot_row} in row {target_row} using multiplier {multiplier}.")

            # Log the resulting matrix
            logging.info("Final RREF matrix computed:")
            logging.info("\n" + str(doc_matrix))
            print("Final RREF Matrix:")
            print(doc_matrix)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")

    # Save the DataFrame to Excel (include Raw & Column index)
    doc_matrix.to_excel(write_path, index=True)

produce_matrix()