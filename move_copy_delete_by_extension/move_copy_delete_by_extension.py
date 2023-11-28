
'''
This Python script is a file management tool that allows users to perform Copy, Move, or Delete actions on files of a specified type within a directory and its subdirectories. The script is well-structured into functions and a main execution block, providing a user-interactive experience. Here's an overview of its functionality:
1. Functions for File Operations:
 1.1. delete(file_type, start_dir): Deletes files of a specified type in a given directory and all its subdirectories. It asks for user confirmation before proceeding and prints status messages.
 1.2. copy(file_type, start_dir, end_dir): Copies files of a specified type from a starting directory to a destination directory, including creating necessary subdirectories in the destination. User confirmation is required before proceeding.
 1.3. move(file_type, start_dir, end_dir): Moves files of a specified type from a starting directory to a destination directory, similar to the copy function, but also deletes empty folders from the starting directory after moving the files.
2. Main Function (main):
 2.1. Handles user input to determine the action type (Copy, Move, Delete), the file type to be acted upon, and the source and destination directories.
 2.2. Validates the existence of the starting directory and, for Copy and Move actions, the destination directory.
 2.3. Calls the appropriate function based on the user's choice of action.
3. User Interaction:
 3.1. The script interacts with the user through the command line, prompting for necessary information and confirming actions.
 3.2. Includes input validation to ensure correct and expected user inputs.
4. Error Handling:
 4.1. Each function includes try-except blocks to handle potential errors during file operations and provides relevant error messages to the user.
5. Execution Block:
 5.1. The script's execution starts in the if __name__ == "__main__": block, which calls the main function.

How to Use This Script:
1. Run the Script: Place the script in a directory from where you want to perform file operations and run it.
Follow Prompts: The script will ask you to choose an action (Copy, Move, Delete), specify a file type (extension or "*" for all files), and provide the source and (if applicable) destination directories.
2. Confirm Action: Before executing, the script will ask for confirmation. Respond with "Y" to proceed or "N" to cancel.
3. Check Results: After the operation is complete, the script will display a message. Check the source and destination directories to verify the changes.

Important Considerations:
1. Use caution, especially with the Delete and Move functions, as they can permanently alter your file system.
2. Ensure the paths for the source and destination directories are correctly entered.
3. Before using the Move or Delete functions, consider creating backups of your files. These actions are irreversible, and having backups can prevent accidental data loss.
4. Be precise when specifying the file type for the operations. A small mistake (like a typo) could lead to unintended files being copied, moved, or deleted.
5. Ensure that the destination directory in Copy or Move actions has sufficient space to accommodate the files being transferred.
6. Be aware that moving or deleting files and directories can change the structure of your file system. Ensure you understand the impact of these changes, particularly when working with nested directories.
7. Be aware of file permissions. The script may encounter errors if it attempts to move or delete files for which the current user does not have appropriate permissions.
'''

import os
from os import path
import shutil
import re

# Delete Function
def delete(file_type, start_dir):
    """
    Deletes files of a specified type in a given directory and its subdirectories.
    
    Args:
    file_type (str): The file extension type to be deleted.
    start_dir (str): The starting directory from where files will be deleted.
    """
    # Confirmation of Delete action on the folder/sub-folders for the file type
    print(f"\nAre you sure that you want to Delete all files with the file type: {file_type.upper()}")
    print(f"from: {start_dir} and all sub-folders")
    confirm_action = input("Y or N? ")
    print()
    # Guarantees that it is either N or Y so it can proceed
    while confirm_action != "Y" and confirm_action != "N":
        confirm_action = input("Y or N? ")
        print()
    if confirm_action == 'Y':
        # Message saying it will start
        print(f"Files with file type {file_type.upper()} will now be Deleted from: ")
        print(f"{start_dir}")
        # Moves directory to the start_dir
        os.chdir(start_dir)
        # This does an os.walk() which will step through every file in the folder
        # and have lists of all of the folders, sub-folders and file names
        # topdown = False means that it starts from the base folder and spiders out
        try:
            for folderName, subfolders, filenames in os.walk(start_dir, topdown=False):
                # made it so there is an order to operations using a for loop
                for i in range(2):
                    # first operation will delete the files
                    if i == 0:
                        for filename in filenames:
                            try:
                                file_path = os.path.join(folderName, filename)
                                # this deletes all files in all of the folders within the start_dir
                                if file_type == "*":
                                    os.remove(file_path)
                                # this deletes all files with .file_type at the end within the start_dir
                                elif filename.endswith(f'.{file_type}'):
                                    os.remove(file_path)
                            except FileNotFoundError:
                                print(f"File not found: {file_path}")
                            except PermissionError:
                                print(f"Permission denied: {file_path}")
                    # second operation will delete folders that are empty
                    # inside of the start_dir folder.
                    elif i == 1:
                        for filename in filenames:
                            try:
                                if folderName != start_dir:
                                    # deletes empty folders that are not the start_dir
                                    try: os.rmdir(folderName)
                                    # if there are files missing in the list or folders missing
                                    # these exceptions just let the problem keep going
                                    except FileNotFoundError: pass
                                    except OSError: pass
                            except OSError:
                                pass  # Directory not empty
                    else:
                        print("\nIndex Error for File Deletion Sequence")
                        # Pauses program and exits when Enter is pressed
                        try: input("Press Enter to exit the program")
                        except SyntaxError: os._exit(1)
                        os._exit(1)
            # message after the actions are completed
            print("\nFile and Sub-Folder Deletion Completed")
            
        except Exception as e:
            print(f"An error occurred: {e}")
            
        print("\nFile and Sub-Folder Deletion Completed")
    # If confirmation is marked as N, displays canceled and closes
    elif confirm_action == 'N':
        print("\nFile and Sub-Folder Deletion Canceled")
        pass
    # Pauses program and exits when Enter is pressed
    try: input("\nPress Enter to exit the program")
    except SyntaxError: os._exit(1)
    os._exit(1)

# Copy Function
def copy(file_type, start_dir, end_dir):
    """
    Copies files of a specified type from one directory to another, including subdirectories.
    
    Args:
    file_type (str): The file extension type to be copied.
    start_dir (str): The starting directory from where files will be copied.
    end_dir (str): The destination directory to where files will be copied.
    """
    # Confirmation of Copy action on the folder/sub-folders for the file type
    print(f"\nAre you sure that you want to Copy all files with the file type: {file_type.upper()}")
    print(f"from: {start_dir} and all sub-folders")
    print(f"to: {end_dir}")
    confirm_action = input("Y or N? ")
    print()
    # Guarantees that it is either N or Y so it can proceed
    while confirm_action != "Y" and confirm_action != "N":
        confirm_action = input("Y or N? ")
        print()
    if confirm_action == 'Y':
        try:
            # Message saying it will start
            print(f"Files with file type {file_type.upper()} will now be Copied from:")
            print(f"{start_dir} to {end_dir}")
            # Moves directory to the start_dir
            os.chdir(start_dir)
            # This does an os.walk() which will step through every file in the folder
            # and have lists of all of the folders, sub-folders and file names
            # topdown = False means that it starts from the base folder and spiders out
            for folderName, subfolders, filenames in os.walk(start_dir, topdown=False):
                # this one does not need a for loop to do things in order.
                # it only copies files/folders, doesn't need to remove folder after
                for filename in filenames:
                    try:
                        src_path = src_path
                        # searches for sub-folders using the start_dir and other folders
                        # every loop of filename
                        regex = re.compile(re.escape(start_dir) + r"(\\.*)")
                        # finds the current subfolder from the start_dir if there is one
                        # and adds it to the end_dir to match sub-folders
                        subfolderName = re.findall(regex, folderName)
                        try: current_end_dir = str(end_dir + subfolderName[0])
                        # if there is no index, that means there is no sub-folder
                        # so you want the current_end_dir to be the end_dir
                        except IndexError: current_end_dir = str(end_dir)
                        # makes sub-folders and copies all files
                        if file_type == "*":
                            # makes the folders
                            try: os.makedirs(current_end_dir)
                            # if the folder exists, just move on
                            except FileExistsError: pass
                            # copies all files
                            shutil.copy(src_path, os.path.join(current_end_dir, filename))
                        # copies all files with the .file_type at the end
                        elif filename.endswith(f'.{file_type}'):
                            # makes the folders
                            try: os.makedirs(current_end_dir)
                            # if the folder exists, just move on
                            except FileExistsError: pass
                            # copies all files of the certain file type
                            shutil.copy(src_path, os.path.join(current_end_dir, filename))
                    except FileNotFoundError:
                        print(f"File not found: {src_path}")
                    except PermissionError:
                        print(f"Permission denied: {src_path}")
        except Exception as e:
            print(f"An error occurred: {e}")
        print("\nFile and Sub-Folder Copying Completed")
    # If confirmation is marked as N, displays canceled and closes
    elif confirm_action == 'N':
        print("\nFile and Sub-Folder Copying Canceled")
        pass
    # Pauses program and exits when Enter is pressed
    try: input("\nPress Enter to exit the program")
    except SyntaxError: os._exit(1)
    os._exit(1)

# Move Function
def move(file_type, start_dir, end_dir):
    """
    Moves files of a specified type from one directory to another, including subdirectories.
    
    Args:
    file_type (str): The file extension type to be moved.
    start_dir (str): The starting directory from where files will be moved.
    end_dir (str): The destination directory to where files will be moved.
    """
    # Confirmation of Move action on the folder/sub-folders for the file type
    print(f"\nAre you sure that you want to Move all files with the file type: {file_type.upper()}")
    print(f"from: {start_dir} and all sub-folders")
    print(f"to: {end_dir}")
    confirm_action = input("Y or N? ")
    print()
    # Guarantees that it is either N or Y so it can proceed
    while confirm_action != "Y" and confirm_action != "N":
        confirm_action = input("Y or N? ")
        print()
    if confirm_action == 'Y':
        try:
            # Message saying it will start
            print(f"Files with file type {file_type.upper()} will now be Moved from:")
            print(f" {start_dir} to {end_dir}")
            # Moves directory to the start_dir
            os.chdir(start_dir)
            # This does an os.walk() which will step through every file in the folder
            # and have lists of all of the folders, sub-folders and file names
            # topdown = False means that it starts from the base folder and spiders out
            for folderName, subfolders, filenames in os.walk(start_dir, topdown=False):
                # made it so there is an order to operations using a for loop
                for i in range(2):
                    # first operation will move files and make sub-folders
                    if i == 0:
                        for filename in filenames:
                            try:
                                src_path = os.path.join(folderName, filename)
                                # searches for sub-folders using the start_dir and other folders
                                # every loop of filename
                                regex = re.compile(re.escape(start_dir) + r"(\\.*)")
                                # finds the current subfolder from the start_dir if there is one
                                # and adds it to the end_dir to match sub-folders
                                subfolderName = re.findall(regex, folderName)
                                try: current_end_dir = str(end_dir + subfolderName[0])
                                # if there is no index, that means there is no sub-folder
                                # so you want the current_end_dir to be the end_dir
                                except IndexError: current_end_dir = str(end_dir)
                                # makes sub-folders and moves all files
                                if file_type == "*":
                                    # makes the folders
                                    try: os.makedirs(current_end_dir)
                                    # if the folder exists, just move on
                                    except FileExistsError: pass
                                    # moves all files
                                    shutil.move(os.path.join(folderName, filename), os.path.join(current_end_dir, filename))
                                # moves all files with the .file_type at the end
                                elif filename.endswith(f'.{file_type}'):
                                    # makes the folders
                                    try: os.makedirs(current_end_dir)
                                    # if the folder exists, just move on
                                    except FileExistsError: pass
                                    # moves all files with .file_type at the end
                                    shutil.move(os.path.join(folderName, filename), os.path.join(current_end_dir, filename))
                            except FileNotFoundError:
                                print(f"File not found: {src_path}")
                            except PermissionError:
                                print(f"Permission denied: {src_path}")
                    # second operation will delete folders that are empty
                    # inside of the start_dir folder.
                    elif i == 1:
                        try:
                            for filename in filenames:
                                if folderName != start_dir:
                                    # deletes empty folders that are not the start_dir
                                    try: os.rmdir(folderName)
                                    # if there are files missing in the list or folders missing
                                    # these exceptions just let the problem keep going
                                    except FileNotFoundError: pass
                                    except OSError: pass
                        except OSError:
                            pass  # Directory not empty
                    else:
                        print("\nIndex Error for File Moving Sequence")
                        # Pauses program and exits when Enter is pressed
                        try: input("Press Enter to exit the program")
                        except SyntaxError: os._exit(1)
                        os._exit(1)
        except Exception as e:
            print(f"An error occurred: {e}")
        print("\nFile and Sub-Folder Moving Completed")
    # If confirmation is marked as N, displays canceled and closes
    elif confirm_action == 'N':
        print("\nFile and Sub-Folder Moving Canceled")
        pass
    # Pauses program and exits when Enter is pressed
    try: input("\nPress Enter to exit the program")
    except SyntaxError: os._exit(1)
    os._exit(1)

def main():
    """
    Main function to handle user input and execute file operations based on the input.
    
    The user is prompted to choose an action (Copy, Move, Delete), select a file type, 
    and specify the source and destination directories. The chosen action is then 
    executed using the appropriate function.
    """
    # Initialize variables
    execute_type = ""
    end_dir = ""

    # Prompt user for action type and validate input
    while execute_type not in ["Copy", "Move", "Delete"]:
        execute_type = input("Copy, Move or Delete: ").capitalize()
        if execute_type not in ["Copy", "Move", "Delete"]:
            print("Invalid action. Please enter 'Copy', 'Move', or 'Delete'.")

    # Prompt user for file type
    file_type = input("File Type (\"*\" for all files): ").strip()

    # Validate and get the starting directory
    start_dir = input(f"Directory to {execute_type} from: ").strip()
    while not path.exists(start_dir):
        print("Directory does not exist. Please enter a valid directory.")
        start_dir = input(f"Directory to {execute_type} from: ").strip()

    # Get and validate the ending directory for Copy and Move actions
    if execute_type in ['Copy', 'Move']:
        end_dir = input(f"Directory to {execute_type} to: ").strip()

    # Execute the chosen action
    try:
        if execute_type == 'Delete':
            delete(file_type, start_dir)
        elif execute_type == 'Copy':
            copy(file_type, start_dir, end_dir)
        elif execute_type == 'Move':
            move(file_type, start_dir, end_dir)
    except Exception as e:
        print(f"An error occurred while executing the action: {e}")

    # Exit the program
    input("\nPress Enter to exit the program")

if __name__ == "__main__":
    main()
