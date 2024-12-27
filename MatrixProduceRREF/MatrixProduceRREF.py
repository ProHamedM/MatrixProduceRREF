import pandas as pd
import numpy as np
import logging


# Configure the logger
logging.basicConfig(
    filename='matrix_operations.log',  # Log file name
    level=logging.INFO,                # Logging level
    format='%(asctime)s - %(message)s' # Log entry format
)

# Ask client paths
read_path = input ('Please enter excel File\'s Path?').strip() # Remove extra spaces
write_path = input ('Please enter saving directory?').strip() # Remove extra spaces
# Convert paths to string
read_path = str(read_path)
write_path = str(write_path ) + '\Answer.xlsx'
print(write_path)



def produce_matrix ():
    global doc_matrix
    global temp_matrix
    global temp_num

    try:
        # Read matrix from Excel file
        doc_matrix = pd.read_excel(read_path, header=None).astype(float) # Disable header assumption & Set values Float

        # Check if DataFrame is empty
        if doc_matrix.empty:
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
                            break
                    else:
                        # If no non-zero pivot found, skip this column
                        print(f"Column {pivot_row} has no valid pivot. Skipping...")
                        continue

                # Normalize the pivot row
                pivot_value = doc_matrix.iloc[pivot_row, pivot_row]
                doc_matrix.iloc[pivot_row, :] /= pivot_value

                # Step 3: Eliminate all other entries in the pivot column
                for target_row in range(num_rows):
                    if target_row != pivot_row:  # Skip the pivot row itself
                        multiplier = doc_matrix.iloc[target_row, pivot_row]
                        doc_matrix.iloc[target_row, :] -= multiplier * doc_matrix.iloc[pivot_row, :]

            # Log the resulting matrix
            print("Final RREF Matrix:")
            print(doc_matrix)

    except Exception as e:
        print(f"An error occurred: {e}")

    # Save the DataFrame to Excel (include Raw & Column index)
    doc_matrix.to_excel(write_path, index=True)

produce_matrix()