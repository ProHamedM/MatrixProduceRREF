# MatrixProduceRREF

This project is a console-based Python application for calculating the Reduced Row Echelon Form (RREF) of a matrix. The application reads the matrix from an Excel file, processes it, and saves the result to a new Excel file.

Features

Reads an input matrix from an Excel file.

Processes the matrix to its RREF using Gaussian elimination.

Handles special cases, such as:

Zero pivots (swaps rows automatically).

Empty input files or invalid paths.

Saves the RREF matrix to Answer.xlsx in a user-specified directory.



Installation

Running From Source Code

1- Clone this repository:

	git clone https://github.com/<your-username>/MatrixProduceRREF.git
cd MatrixProduceRREF
2- Install required dependencies:

	pip install pandas numpy openpyxl

License

This project is open-source.