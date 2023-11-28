
'''
This Python script provides a comprehensive solution for securely deleting files and directories from a specified path. It includes several functions, each serving a unique role in the secure deletion process. Here's a summary of its functions and usage:
1. Random String Generation (get_random_string):
 1.1. Generates a random string of a specified length using ASCII letters and digits.
2. Filling Files with Random Data (fill_file_with_random_data):
 2.1. Writes random data to a specified file, overwriting its content. The size of the random data and the option to print status messages are configurable.
3. Emptying Files (empty_file):
 3.1. Empties the content of a specified file by overwriting it with no data.
4. Secure File Deletion (secure_delete):
 4.1. Securely deletes a file by overwriting it multiple times with random data before finally deleting it. The number of overwrite iterations and the option to print status messages are configurable.
5. Secure Rename and Delete (secure_rename_delete):
 5.1. Securely renames and deletes all files and directories in a specified path. It renames each item with a random string, overwrites files with random data (as per the specified iterations), and finally deletes them. The root directory can also be renamed and deleted based on the deletetop flag.

How to Use This Script:
1. Set the path in secure_rename_delete to the directory you want to securely delete.
2. Configure secure_remove_iterations to specify how many times you want to overwrite files with random data before deletion.
3. Set printremovals to 1 if you want to print status messages during the deletion process, or 0 to suppress them.
4. Decide whether to delete the root directory (deletetop) by setting it to 1 (delete) or 0 (keep).
5. Run the script. It will securely rename and delete files and directories in the specified path according to your configurations.

Important Considerations:
1. Use this script cautiously, as it will irreversibly delete files and directories.
2. Ensure the path is correct to avoid accidental deletion of important files.
3. The script is particularly useful for scenarios where secure data removal is necessary, like preparing a device for disposal or transfer to another user.
4. The script does not employ cryptographic wiping methods, so it may not meet certain regulatory standards for data sanitization.
'''

import os
import shutil
import random
import secrets
import string
from pathlib import Path
import subprocess
import time


# Define the PowerShell command
ps_command = 'Clear-History'


def get_random_string(length):
    """
    Generate a random string of fixed length.
    
    :param length: The length of the random string
    :return: A random string of the specified length
    """
    # Use all ASCII letters and digits as possible characters for the random string
    letters = string.ascii_letters + string.digits
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def fill_file_with_random_data(file_path, size, printremovals):
    """
    Fill a file with random data.
    
    :param file_path: The path of the file to fill with random data
    :param size: The size of the random data to fill the file with
    :param printremovals: If true, print messages about the data removal process
    """
    try:
        # Generate cryptographically secure random data
        random_data = secrets.token_bytes(size)
        # Write the random data to the file
        with open(file_path, 'wb') as f:
            f.write(random_data)
            f.flush()
            os.fsync(f.fileno())
        # Print a message if printremovals is true
        if printremovals and size != 0:
            print(f"Filled {file_path} with random data")
    except Exception as e:
        print(f"An error occurred while filling the file {file_path} with random data: {str(e)}")


def empty_file(file_path, printremovals):
    """
    Empty a file.
    
    :param file_path: The path of the file to empty
    :param printremovals: If true, print messages about the data removal process
    """
    try:
        # Overwrite the file with no data
        fill_file_with_random_data(file_path, 0, printremovals)
        # Print a message if printremovals is true
        if printremovals:
            print(f"Emptied {file_path}")
    except Exception as e:
        print(f"An error occurred while emptying the file {file_path}: {str(e)}")


def secure_delete(file_path, secure_remove_iterations, printremovals):
    """
    Securely delete a file.
    
    :param file_path: The path of the file to delete
    :param secure_remove_iterations: The number of times to overwrite the file with random data before deleting
    :param printremovals: If true, print messages about the data removal process
    """
    try:
        # If secure_remove_iterations is greater than 0, overwrite the file with random data the specified number of times
        if secure_remove_iterations > 0:
            for _ in range(secure_remove_iterations):
                fill_file_with_random_data(file_path, os.path.getsize(file_path), printremovals)
        # Overwrite the file with no data
        empty_file(file_path, printremovals)
        # Delete the file
        os.remove(file_path)
    except Exception as e:
        print(f"An error occurred while securely deleting the file {file_path}: {str(e)}")


def secure_rename_delete(path, secure_remove_iterations, printremovals, deletetop):
    """
    Securely rename and delete all files and folders in a path.
    
    :param path: The path to secure delete
    :param secure_remove_iterations: The number of times to overwrite files with random data before deleting
    :param printremovals: If true, print messages about the data removal process
    :param deletetop: If true, rename and delete the root folder. Otherwise, leave it alone.
    """
    try:
        # Iterate over all subfolders and files in the path
        for foldername, subfolders, filenames in os.walk(path):
            # Handle subfolders
            for subfolder in subfolders:
                old_path = Path(foldername) / subfolder
                new_path = Path(foldername) / get_random_string(16)
                # Rename subfolder
                os.rename(old_path, new_path)
                # Print a message if printremovals is true
                if printremovals:
                    print(f"Changed {old_path} to {new_path}")
                # Recursively secure rename and delete the subfolder
                secure_rename_delete(new_path, secure_remove_iterations, printremovals, deletetop=0)
                if printremovals:
                    print(f"Deleted {new_path}")
            # Handle files
            for filename in filenames:
                old_path = Path(foldername) / filename
                new_path = Path(foldername) / (get_random_string(16) + '.txt')
                # Rename file
                os.rename(old_path, new_path)
                # Print a message if printremovals is true
                if printremovals:
                    print(f"Changed {old_path} to {new_path}")
                # Securely delete the file
                secure_delete(new_path, secure_remove_iterations, printremovals)
                if printremovals:
                    print(f"Deleted {new_path}")
                    
        # If deletetop is true, rename and delete the root folder
        if deletetop:
            # Rename the root folder
            parent_path = Path(path).parent
            new_root_folder_name = get_random_string(16)
            new_path = parent_path / new_root_folder_name
            os.rename(path, new_path)
            # Print a message if printremovals is true
            if printremovals:
                print(f"Changed {path} to {new_path}")
            # Delete the root folder
            shutil.rmtree(new_path)
            if printremovals:
                print(f"Deleted {new_path}")
        
    except Exception as e:
        print(f"An error occurred while securely renaming and deleting the path {path}: {str(e)}")

# Securely delete a path.
secure_rename_delete(path=r"C:\test\test", secure_remove_iterations=0, printremovals=1, deletetop=0)
