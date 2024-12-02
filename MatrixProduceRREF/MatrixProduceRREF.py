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
        doc_matrix = pd.read_excel(read_path)

        # Check if DataFrame is empty
        if doc_matrix.empty:
            print('The file is empty. :)')
        else:
            print(doc_matrix.to_string())
        # return
    except Exception as e:
        print(f"An error occurred: {e}")

    # Save the DataFrame to Excel
    doc_matrix.to_excel(write_path, index=False)

produce_matrix()