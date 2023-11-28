
'''
This Python script performs the following operations:
1. Set Source and Destination Paths: It starts by defining a working_folder which is both the source of subfolders and the destination for the files to be copied to. In this case, it's set to "C:\test\test".
2. List Subfolders in Source Folder: The script creates a list of all subfolders in the working_folder.
3. Copy Files from Subfolders to Main Folder: For each subfolder, the script:
 3.1. Retrieves all files.
 3.2. Copies each file to the main folder (working_folder), renaming it to include the subfolder's name and a sequential number (formatted with leading zeros for consistency). This avoids file name conflicts.
4 Empty and Delete Subfolders: After copying the files, the script revisits each subfolder:
 4.1. Empties the content of each file (writes an empty string to it).
 4.2. Deletes each file.
 4.3.Removes the subfolder itself.
5. Completion Message: Once the process is complete, it prints a message indicating successful file copying and cleanup.

How to Use This Script:
1. Set Up the Working Folder: Modify the working_folder variable to the path of the folder containing the subfolders you want to manage.
2. Run the Script: Execute the script. This will copy the files from each subfolder into the main folder, renaming them to prevent naming conflicts and then delete the original files and their parent subfolders.
3. Check Results: After running, you should find all files from the subfolders in the main folder, each renamed and the subfolders should be removed.

Important Notes:
1. Ensure that the working_folder path is correct to avoid unintended data loss.
2. This script will permanently delete files and folders, so use it with caution.
3. It's advisable to backup your data before running such scripts.
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

def copy_files_to_main_folder(source_folder):
    """
    Copies files from subfolders of a given source folder into the source folder,
    renaming the files to include their subfolder name and a sequence number.

    Args:
    source_folder (str): The path to the source folder.
    """
    subfolders = get_subfolders(source_folder)

    # Iterate over each subfolder and copy the files to the main folder
    for folder in subfolders:
        folder_name = os.path.basename(folder)
        files = [f.path for f in os.scandir(folder) if f.is_file()]

        # Iterate over each file in the subfolder and copy to the main folder
        for i, file in enumerate(files):
            try:
                file_name = os.path.basename(file)
                new_file_name = f'{folder_name} - {str(i+1).zfill(3)}_{file_name}'
                destination_path = os.path.join(source_folder, new_file_name)
                shutil.copy(file, destination_path)
            except Exception as e:
                print(f"Error copying {file}: {e}")

def delete_subfolders(source_folder):
    """
    Empties and deletes all subfolders in the given source folder.

    Args:
    source_folder (str): The path to the source folder.
    """
    subfolders = get_subfolders(source_folder)

    # Iterate over each subfolder again and delete files, then delete the subfolder
    for folder in subfolders:
        files = [f.path for f in os.scandir(folder) if f.is_file()]

        # Empty and delete each file in the subfolder
        for file in files:
            try:
                with open(file, 'w') as f:
                    f.write('')  # Empty the contents of the file
                os.remove(file)  # Delete the file
            except Exception as e:
                print(f"Error processing {file}: {e}")

        # Delete the now empty subfolder
        try:
            os.rmdir(folder)
        except Exception as e:
            print(f"Error deleting folder {folder}: {e}")

def main():
    """
    Main function to execute the file processing tasks.
    """
    working_folder = r"C:\test\test"

    try:
        copy_files_to_main_folder(working_folder)
        delete_subfolders(working_folder)
        print('Files copied successfully. Source folders emptied and deleted.')
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()