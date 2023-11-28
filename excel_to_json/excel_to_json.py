
'''
This Python script is designed to convert all Excel files (.xlsx) in the current working directory into JSON format. The script is structured into a single function, excel_folder_to_text, that performs the entire conversion process. Here's an overview of its functionality:
1. Function: excel_folder_to_text:
 1.1. The function first gets the current working directory.
 1.2. It then loops through all files in the directory.
 1.3. For each file, it checks if the file is an Excel file (.xlsx extension).
 1.4. If an Excel file is found, it reads the file into a pandas DataFrame.
 1.5. The function identifies any date columns in the DataFrame and converts them to string format in 'YYYY-MM-DD' format.
 1.6. The DataFrame is then converted to a JSON string, formatted with each record (row) as a separate JSON object.
 1.7. The JSON data is stored in a new JSON file, named after the original Excel file but in lowercase.
 1.8. The script includes error handling at various stages to manage issues like file reading, date conversion, and JSON file writing.
2. Error Handling:
 2.1. The script includes multiple try-except blocks to handle potential errors during file reading, date processing, and file writing, ensuring that it continues processing other files even if one file encounters an issue.
3. Execution:
 3.1. The script calls the excel_folder_to_text function directly, indicating that it's intended to be run as a standalone script.

How to Use This Script:
1. Place the Script in a Directory: Copy the script into a directory containing the Excel files you want to convert.
2. Run the Script: Execute the script in this directory. It will convert each .xlsx file into a corresponding JSON file.
3. Check the Output: After running, you should find JSON files in the same directory, each named after one of the Excel files but in lowercase.

Important Considerations:
1. Ensure that the Python environment has pandas installed, as it's a key dependency for this script.
2. The script assumes that date columns in the Excel files are recognizable by pandas and can be converted to string format. It might not handle custom date formats without modifications.
3. This script is particularly useful for batch converting Excel files to JSON, a common requirement in data processing and migration tasks.
'''

import os
import pandas as pd
import json

def excel_folder_to_text():
    """
    Converts all Excel (.xlsx) files in the current working directory to JSON format.
    Each file's data is stored in a separate JSON file with the same base name.
    Date columns are converted to string format.
    """
    folder_path = os.getcwd()  # Get the current working directory

    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        try:
            # Check if the file is an Excel file
            if filename.endswith(".xlsx"):
                # Construct the full path to the file
                file_path = os.path.join(folder_path, filename)
                file_name, file_ext = os.path.splitext(filename)
                json_filename = file_name.lower()

                try:
                    # Read the Excel file into a pandas DataFrame
                    df = pd.read_excel(file_path)
                except Exception as e:
                    print(f"Error reading {filename}: {e}")
                    continue

                try:
                    # Convert date columns to string format
                    date_cols = [col for col in df.columns if df[col].dtype == 'datetime64[ns]']
                    df[date_cols] = df[date_cols].apply(lambda x: x.dt.strftime('%Y-%m-%d'))
                except Exception as e:
                    print(f"Error processing date columns in {filename}: {e}")
                    continue

                # Convert the DataFrame to a dictionary
                data = '{"'+json_filename+'": '+df.to_json(orient="records", date_format="iso")+"}"

                # Construct the output file path
                output_file = json_filename + ".json"

                try:
                    # Write the JSON string to the output file
                    with open(output_file, "w") as f:
                        f.write(data)
                except Exception as e:
                    print(f"Error writing to {output_file}: {e}")
        except Exception as e:
            print(f"An error occurred with file {filename}: {e}")

# Call the function
excel_folder_to_text()
