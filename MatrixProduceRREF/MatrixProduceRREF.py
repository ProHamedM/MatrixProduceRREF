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
    global temp_matrix
    global temp_num

    try:
        # Read matrix from Excel file
        doc_matrix = pd.read_excel(read_path, header=None).astype(float) # Disable header assumption & Set values Float

        # Check if DataFrame is empty
        if doc_matrix.empty:
            print('The file is empty. :)')
        else:

            # Extract the first row
            temp_matrix = doc_matrix.iloc[0, :]  # Using .iloc for positional indexing
            # Get the first value of the first row
            temp_num = temp_matrix.iloc [0]
            # Divide the first row by its first value
            temp_matrix = temp_matrix / temp_num
            # Update the DataFrame
            doc_matrix.iloc[0, :] = temp_matrix


            num_rows = doc_matrix.shape[0] # Number of rows

            for count in range(num_rows):  # Use `for` loop for cleaner iteration
                # Initial 1st row just as it is
                if count == 0: # Access the row by position
                    row = doc_matrix.iloc[count]  # Access the row at index `count`
                else:
                    # Extract the row
                    temp_matrix = doc_matrix.iloc[0, :]  # Using .iloc for positional indexing
                    # Get the first value of the row
                    temp_num = doc_matrix.iloc[count,0] # Access the value in the (num_row) row and first column
                    # Multiply the row by its first value
                    temp_matrix = temp_matrix * temp_num

                    print("log temp _ MAt : " + str (temp_matrix))
                    # Subtract the row from the specific Row of the DataFrame
                    doc_matrix.iloc[count, :] = doc_matrix.iloc[count,:] - temp_matrix

        print('log MAT total : ' + str(doc_matrix))  # Print row without the index
    except Exception as e:
        print(f"An error occurred: {e}")

    # Save the DataFrame to Excel (include Raw & Column index)
    doc_matrix.to_excel(write_path, index=True)

produce_matrix()