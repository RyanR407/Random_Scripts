
'''
This Python script converts all JSON files in the current working directory into Excel (.xlsx) format. It's structured around a single function, json_to_excel, which encapsulates the entire process. Here's a breakdown of its functionality:
1. Function: json_to_excel:
 1.1. The function first retrieves the current working directory.
 1.2. It then iterates through all files in this directory.
 1.3. For each file, the function checks if it is a JSON file.
 1.4. If a JSON file is found, it reads the file's content.
 1.5. The function assumes the JSON structure contains a key that represents the worksheet name, with its value being a list of dictionaries (records).
 1.6. The script converts this list of dictionaries into a pandas DataFrame.
 1.7. The function then identifies any date columns in the DataFrame (checking for 'YYYY-MM-DD' formatted strings) and converts them back to datetime format.
 1.8. The DataFrame is then written to an Excel file, with the filename derived from the original JSON file's key.
 1.9. The script includes error handling at various stages to manage issues like file reading, DataFrame conversion, and Excel file writing.
2. Error Handling:
 2.1. Multiple try-except blocks are used to handle potential errors during JSON reading, DataFrame creation, date column processing, and Excel file writing, ensuring that the script continues processing other files even if one file encounters an issue.
3. Execution:
 3.1. The script calls the json_to_excel function directly, indicating that it's intended to be run as a standalone script.

How to Use This Script:
1. Place the Script in a Directory: Copy the script into a directory containing the JSON files you want to convert.
2. Run the Script: Execute the script in this directory. It will convert each .json file into a corresponding Excel file.
3. Check the Output: After running, you should find Excel files in the same directory, each named after one of the JSON file's key names.

Important Considerations:
1. Ensure that the Python environment has pandas installed, as it's crucial for this script.
2. The script assumes a specific JSON structure (a dictionary where the key is the worksheet name and the value is a list of records). It may require modification to work with other JSON formats.
3. This script is particularly useful for batch converting JSON files to Excel, which is common in data migration and processing tasks.
'''

import os
import pandas as pd
import json
import re

def json_to_excel():
    """
    Converts all JSON files in the current working directory to Excel (.xlsx) format.
    Each JSON file's data is extracted and stored in a separate Excel file.
    Date columns are converted back to their original datetime format.
    """
    folder_path = os.getcwd()  # Get the current working directory

    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        try:
            # Check if the file is a JSON file
            if filename.endswith(".json"):
                try:
                    # Read the JSON file
                    with open(os.path.join(folder_path, filename), "r") as f:
                        data = json.load(f)
                except Exception as e:
                    print(f"Error reading {filename}: {e}")
                    continue

                # Get the name of the worksheet
                worksheet_name = list(data.keys())[0]
                # Get the data as a list of dictionaries
                records = data[worksheet_name]

                try:
                    # Convert the list of dictionaries to a pandas DataFrame
                    df = pd.DataFrame.from_records(records)
                except Exception as e:
                    print(f"Error converting data from {filename} to DataFrame: {e}")
                    continue

                try:
                    # Convert date columns back to datetime format
                    date_cols = [col for col in df.columns if df[col].dtype == 'object' and re.match(r'\d{4}-\d{2}-\d{2}', str(df[col].iloc[0]))]
                    df[date_cols] = df[date_cols].apply(pd.to_datetime)
                except Exception as e:
                    print(f"Error processing date columns in {filename}: {e}")
                    continue

                # Construct the output file path
                output_file = os.path.join(folder_path, worksheet_name + ".xlsx")

                try:
                    # Write the DataFrame to the Excel file
                    df.to_excel(output_file, index=False)
                except Exception as e:
                    print(f"Error writing to {output_file}: {e}")
        except Exception as e:
            print(f"An error occurred with file {filename}: {e}")

# Call the function
json_to_excel()