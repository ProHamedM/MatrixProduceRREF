import pandas as pd

# Ask client path
path = input ('Please enter excel File\'s Path & Sheet?').strip() #Remove extra spaces
# Convert path to string
path = str(path)
print(path)



def produce_matrix ():
    try:
        # Read matrix from Excel file
        doc_matrix = pd.read_excel(path)  # Exclude the first column

        # Print column names to debug
        print("Column names in the file:")
        print(doc_matrix.index)

        # Check if DataFrame is empty
        if doc_matrix.empty:
            print('The file is empty. :)')
        else:
            print(doc_matrix.to_string())
        # return
    except Exception as e:
        print(f"An error occurred: {e}")

produce_matrix()