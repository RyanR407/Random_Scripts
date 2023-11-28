
'''
This Python script is designed to create directories based on a list of names provided in a multiline string. It's structured into functions, enhancing its readability and modularity. Here's an overview of its components and functionality:
1. split_data Function:
 1.1. Takes a multiline string as input and splits it into a list of items (lines).
 1.2. Any empty lines in the input string are removed in the process.
 1.3. This function is particularly useful for parsing input data that's formatted with each item on a new line.
2. create_directories Function:
 2.1. Accepts a base path and a list of items (directory names).
 2.2. Iterates through the items, creating a directory for each item at the specified base path.
 2.3. Includes error handling to print any issues encountered during directory creation.
3. main Function:
 3.1. Acts as the entry point of the script.
 3.2. It contains a multiline string data with directory names, which is passed to split_data to convert into a list.
 3.3. The base path for creating directories is set to the current working directory (though it can be modified to a specific path).
 3.4. Calls create_directories to create directories for each item in the list.
 3.5. Includes error handling for any exceptions that occur.
4. Execution Block (if __name__ == "__main__":):
 4.1. Ensures that the main function is called when the script is run directly.
 
How to Use This Script:
1. Provide Directory Names: Modify the data multiline string in the main function with the names of the directories you want to create, each name on a new line.
2. Set the Base Path: Optionally, you can change the base_path in the main function to a specific path where you want the directories to be created.
3. Run the Script: Execute the script. It will create a directory for each name in the data string at the specified base path.
4. Check the Results: After running, you should find new directories at the base path corresponding to the names provided in the data string.

Important Considerations:
1. The script is useful for bulk creation of directories, especially when dealing with a structured list of names.
2. Make sure the base path is correctly set to avoid creating directories in unintended locations.
3. The script does not handle the existence of directories with the same name, but it won't overwrite them due to the use of exist_ok=True in os.makedirs.
'''

import os

def split_data(data):
    """
    Splits a multiline string into a list, removing any empty lines.

    Args:
    data (str): A multiline string with each line representing an item.

    Returns:
    list: A list of items from the string.
    """
    return [item for item in data.split('\n') if item]

def create_directories(base_path, items):
    """
    Creates directories at the specified base path for each item in the list.

    Args:
    base_path (str): The base path where directories will be created.
    items (list): A list of directory names to be created.
    """
    for item in items:
        try:
            folder_path = os.path.join(base_path, item)
            os.makedirs(folder_path, exist_ok=True)
        except Exception as e:
            print(f"Error creating folder {folder_path}: {e}")

def main():
    """
    Main function to execute the directory creation tasks.
    """
    data = """
    11-290-1515LS-0700-1
    11-290-1515LS-2400-1
    11-290-1515LS-2400-2
    11-290-1515LS-2650-1
    11-290-1515LS-2650-2
    11-290-2651-24295-1
    11-290-2651-24295-2
    11-290-3106
    11-290-3286
    11-290-3450
    11-290-13098
    11-290-14120
    11-290-14132
    """

    data_list = split_data(data)
    base_path = os.getcwd()  # or set to a specific path

    try:
        create_directories(base_path, data_list)
        print("Folders created successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()