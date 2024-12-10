import pandas as pd

# Ask client paths
read_path = input ('Please enter excel File\'s Path?').strip() # Remove extra spaces
write_path = input ('Please enter saving directory?').strip() # Remove extra spaces
# Convert paths to string
read_path = str(read_path)
write_path = str(write_path ) + '\Answer.xlsx'
print(write_path)



def produce_matrix ():
    global doc_matrix

    try:
        # Read matrix from Excel file
        doc_matrix = pd.read_excel(read_path, header=None) # Disable header assumption

        # Get the number of columns
        row_count = doc_matrix.shape[1]

        # Check if DataFrame is empty
        if doc_matrix.empty:
            print('The file is empty. :)')
        else:
            num_rows = doc_matrix.shape[0] # Number of rows
            count = 0

            for count in range(num_rows):  # Use `for` loop for cleaner iteration
                # Access each row by position
                row = doc_matrix.iloc[count]  # Access the row at index `count`
                print(row.to_string(index=False))  # Print row without the index

    except Exception as e:
        print(f"An error occurred: {e}")

    # Save the DataFrame to Excel (include Raw & Column index)
    doc_matrix.to_excel(write_path, index=True)

produce_matrix()