
'''
This Python script provides an asynchronous solution for archiving folders using WinRAR. It utilizes asyncio, a Python library for writing concurrent code using the async/await syntax. Here's a breakdown of its functions and usage:
1. Asynchronous Folder Archiving (archive_folder):
 1.1. Asynchronously archives a specified folder using WinRAR.
 1.2. Accepts the folder name to be archived and the file path to the WinRAR executable.
 1.3. Constructs and executes a WinRAR command to archive the folder, compressing it into a .rar file in the same directory.
2. Main Function (main):
 2.1. Handles the asynchronous archiving of all folders in the current working directory.
 2.2. Accepts the path to the WinRAR executable.
 2.3. Gathers a list of all folders in the current directory and asynchronously archives each using archive_folder.
3. Execution Block:
 3.1. Sets the path to the WinRAR executable (needs to be specified by the user).
 3.2. Creates an asyncio event loop and runs the main function to archive all folders in the current directory.

How to Use This Script:
1. Set WinRAR Path: Modify the winrar_path variable to the path of your WinRAR executable (e.g., C:\Program Files\WinRAR\WinRAR.exe).
2. Run the Script: Execute the script in a Python environment with asyncio support.
3. Archiving Process: The script will asynchronously archive each folder in the current working directory into separate .rar files.

Important Considerations:
1. WinRAR Installation: Ensure WinRAR is installed on your system and the path to WinRAR.exe is correctly set in the script.
2. Asynchronous Operations: The script performs archiving operations asynchronously, which can be efficient for handling multiple folders simultaneously.
3. Current Working Directory: The script archives folders in its current working directory. Make sure you run the script in the directory containing the folders you want to archive.
4. File Overwriting: If an archive with the same name already exists, it will be replaced. Ensure there are no conflicts with existing archives.
5. Error Handling: The script includes basic error handling for the archiving process, but it's advisable to monitor its output for any issues.

This script is particularly useful for users who need to quickly archive multiple folders without manually using the WinRAR interface.
'''

import os
import asyncio

# Function to archive a folder
async def archive_folder(folder_name, winrar_path):
    """
    Asynchronously archives a given folder using WinRAR.

    Args:
    folder_name (str): The name of the folder to be archived.
    winrar_path (str): The file path to the WinRAR executable.
    """
    folder_path = os.path.join(os.getcwd(), folder_name)
    
    # Ensure we're only working with folders
    if os.path.isdir(folder_path):
        rar_file_path = os.path.join(os.getcwd(), f'{folder_name}.rar')

        # Construct the WinRAR command
        command = f'"{winrar_path}" a -m1 -mt20 -df "{rar_file_path}" "{folder_path}"'

        try:
            # Run the command
            process = await asyncio.create_subprocess_shell(command)
            await process.communicate()
        except Exception as e:
            print(f"Error archiving {folder_name}: {e}")

async def main(winrar_path):
    """
    Main function to handle the asynchronous archiving of folders.

    Args:
    winrar_path (str): The file path to the WinRAR executable.
    """
    # Get list of all folders
    folders = [f for f in os.listdir(os.getcwd()) if os.path.isdir(os.path.join(os.getcwd(), f))]

    # Run the archiving function for each folder
    await asyncio.gather(*(archive_folder(folder, winrar_path) for folder in folders))

if __name__ == "__main__":
    # Replace this with the path to your WinRAR.exe
    winrar_path = r'C:\Program Files\WinRAR\WinRAR.exe'

    # Create an asyncio event loop and run the main function
    asyncio.run(main(winrar_path))