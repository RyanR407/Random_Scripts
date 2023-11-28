
'''
This Python script is designed to copy files from subfolders within a specified directory (source folder) to the root of that directory, renaming the files in the process to avoid naming conflicts. The script is structured into functions for modularity and readability. Here's an overview of its components and functionality:
1. get_subfolders Function:
 1.1. This function takes a directory path as input and returns a list of all subfolders within that directory. It uses os.scandir to scan the directory and filters the results to include only directories (subfolders).
2. copy_files_from_subfolders Function:
 2.1. This function takes a source folder path as input.
 2.2. It first ensures that the source folder exists (creating it if necessary).
 2.3. It then retrieves all subfolders in the source folder using the get_subfolders function.
 2.4. For each subfolder, it iterates over all files, generating a new file name that includes the subfolder name and a sequence number to ensure uniqueness.
 2.5. These files are then copied to the source folder.
 2.6. The function includes error handling to print any issues encountered during the file copying process.
3. main Function:
 3.1. This is the entry point of the script.
 3.2. It sets the working_folder (source folder) path and calls copy_files_from_subfolders to execute the file copying process.
 3.3. It also includes error handling to catch and print any exceptions that occur.
4. Execution Block (if __name__ == "__main__":):
 4.1. This block ensures that the main function is called when the script is run directly.
 
How to Use This Script:
1. Set the Source Folder: Modify the working_folder variable in the main function to the path of your desired source directory.
2. Run the Script: Execute the script. It will copy files from each subfolder into the main folder (source folder), renaming them to include the subfolder name and a unique sequence number.
3. Check the Source Folder: After running, you should find all the files from the subfolders in your specified source folder, each renamed to prevent naming conflicts.

Important Considerations:
1. Ensure the working_folder path is correctly set to avoid any unintended actions.
2. This script does not delete the original files or subfolders after copying, leaving them intact in their original location.
3. The script is particularly useful for consolidating files from multiple subfolders into a single location, especially in cases where file organization and naming conflicts need to be managed.
'''

import os
import shutil

def get_subfolders(directory):
    """
    Get a list of all the subfolders in a given directory.

    Args:
    directory (str): The path to the directory from which to get subfolders.

    Returns:
    list: A list of paths to the subfolders in the given directory.
    """
    return [f.path for f in os.scandir(directory) if f.is_dir()]

def copy_files_from_subfolders(source_folder):
    """
    Copies files from subfolders of a given source folder into the source folder,
    renaming the files to include their subfolder name and a sequence number.

    Args:
    source_folder (str): The path to the source folder.
    """
    # Create the destination folder if it doesn't exist
    os.makedirs(source_folder, exist_ok=True)

    # Get a list of all the subfolders in the source folder
    subfolders = get_subfolders(source_folder)

    # Iterate over each subfolder
    for folder in subfolders:
        folder_name = os.path.basename(folder)
        files = [f.path for f in os.scandir(folder) if f.is_file()]
        
        # Iterate over each file in the subfolder
        for i, file in enumerate(files):
            try:
                file_name = os.path.basename(file)
                
                # Generate the new file name
                new_file_name = f'{folder_name} - {str(i+1).zfill(3)}_{file_name}'
                
                # Create the destination path for the file
                destination_path = os.path.join(source_folder, new_file_name)
                
                # Copy the file to the destination folder
                shutil.copy(file, destination_path)
            except Exception as e:
                print(f"Error copying {file}: {e}")

def main():
    """
    Main function to execute the file copying process.
    """
    # Set the paths for the source folder
    working_folder = r"C:\test\test"

    try:
        copy_files_from_subfolders(working_folder)
        print('Files copied successfully.')
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()