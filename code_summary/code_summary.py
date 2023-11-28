'''
This Python script performs a comprehensive analysis of a specified directory (typically a project folder) and generates a summary report in a text file (codesummary.txt). The main functions of the script include:
1. Directory Analysis (analyze_directory function):
 1.1. Analyzes the given directory, counts characters and lines in various code files (e.g., .py, .html, .js, etc.), and generates a directory tree.
 1.2. Excludes certain folders (those starting with "." and the "public" folder) and counts embedded JavaScript in HTML and .j2 files.
 1.3. Returns a tuple containing a dictionary with file type stats (count, characters, lines) and a list representing the directory tree.
2. Extracting Embedded JavaScript (extract_js_from_html function):
 2.1. Extracts JavaScript code embedded within HTML content, which is then used in the overall analysis.
3. Writing Summary to File (write_summary_to_file function):
 3.1. Writes a detailed summary of the analysis to an output file, including the directory tree and statistics for each tracked file type (percentage of total characters and lines).
4. Execution Flow:
 4.1. The script sets the parent_directory to the current working directory (where the script is run).
 4.2. It then calls analyze_directory to analyze this directory and write_summary_to_file to write the analysis summary to codesummary.txt.
Finally, it prints a message indicating the completion of the analysis.

How to Use This Script:
1. Place the Script in a Parent Directory: This script is designed to be dropped into any parent folder you want to analyze.
2. Run the Script: Execute it. The script will analyze the directory structure, file information, and generate a summary of the files.
3. Review Output: Check the generated codesummary.txt for a detailed report of the directory and file analysis.

Note:
1. The script specifically tracks certain file types (e.g., .py, .html) for detailed analysis, but it can be modified to include or exclude different file types as needed.
2. It's particularly useful for getting an overview of a project's structure and the composition of its codebase.
'''

import os

def analyze_directory(parent_dir):
    """
    Analyzes the specified directory, counting the characters and lines in code files and
    generating a directory tree, while excluding certain folders and counting embedded JS.

    Args:
    parent_dir (str): The parent directory to analyze.

    Returns:
    tuple: A tuple containing a dictionary of file types with their counts, character sums, and LOC,
           and a list representing the directory tree.
    """
    file_types = {}
    total_chars = 0
    total_lines = 0
    directory_tree = []

    for root, dirs, files in os.walk(parent_dir, topdown=True):
        # Skip directories that start with "." and the "public" folder
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'public']

        level = root.replace(parent_dir, '').count(os.sep)
        indent = '│   ' * level
        tree_prefix = '├── ' if level > 0 else ''
        directory_tree.append(f"{indent}{tree_prefix}{os.path.basename(root)}/")

        for file in files:
            if file == 'code_summary.py':  # Skip the script file itself
                continue

            file_path = os.path.join(root, file)
            _, file_ext = os.path.splitext(file)

            # Initialize file type in dictionary if not present
            if file_ext not in file_types:
                file_types[file_ext] = {'count': 0, 'chars': 0, 'lines': 0}

            # Process specific file types
            if file_ext in ['.py', '.html', '.css', '.js', '.json', '.md', '.yml', '.xml', '.j2', '.scss', '.ts', '.sql']:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        file_content = f.readlines()
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")
                    continue

                char_count = sum(len(line) for line in file_content)
                loc_count = len(file_content)

                # Count embedded JavaScript in HTML and .j2 files
                if file_ext in ['.html', '.j2']:
                    js_content = extract_js_from_html('\n'.join(file_content))
                    # Ensure .js key is initialized
                    if '.js' not in file_types:
                        file_types['.js'] = {'count': 0, 'chars': 0, 'lines': 0}
                    file_types['.js']['chars'] += len(js_content)
                    file_types['.js']['lines'] += js_content.count('\n') + 1

                total_chars += char_count
                total_lines += loc_count

                directory_tree.append(f"{indent}│   {file} - {char_count} chars, {loc_count} lines")

                file_types[file_ext]['count'] += 1
                file_types[file_ext]['chars'] += char_count
                file_types[file_ext]['lines'] += loc_count
            else:
                directory_tree.append(f"{indent}│   {file}")

    return file_types, total_chars, total_lines, directory_tree

def extract_js_from_html(html_content):
    """
    Extracts JavaScript code embedded within HTML content.

    Args:
    html_content (str): The HTML content to parse.

    Returns:
    str: Extracted JavaScript code.
    """
    js_code = []
    in_script = False
    for line in html_content.split('\n'):
        if '<script' in line:
            in_script = True
        elif '</script>' in line:
            in_script = False
        elif in_script:
            js_code.append(line)
    return '\n'.join(js_code)

def write_summary_to_file(file_types, total_chars, total_lines, directory_tree, output_file):
    """
    Writes the summary of the analysis and the directory tree to a text file.

    Args:
    file_types (dict): A dictionary of file types with their counts, character sums, and LOC.
    total_chars (int): Total number of characters in the codebase.
    total_lines (int): Total number of lines in the codebase.
    directory_tree (list): The directory tree list.
    output_file (str): Path to the output file where the summary will be written.
    """
    tracked_file_types = ['.py', '.html', '.css', '.js', '.json', '.md', '.yml', '.xml', '.j2', '.scss', '.ts', '.sql']
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("Directory Tree:\n")
            f.write("\n".join(directory_tree))
            f.write("\n\nSummary:\n")
            for ext, data in file_types.items():
                if ext in tracked_file_types:
                    char_percentage = (data['chars'] / total_chars) * 100 if total_chars > 0 else 0
                    line_percentage = (data['lines'] / total_lines) * 100 if total_lines > 0 else 0
                    f.write(f"Type: {ext}, Files: {data['count']}, Total characters: {data['chars']} ({char_percentage:.2f}%), Total lines: {data['lines']} ({line_percentage:.2f}%)\n")
    except Exception as e:
        print(f"Error writing to file {output_file}: {e}")

parent_directory = os.getcwd()  # Current working directory
output_file = 'codesummary.txt'

print("Analyzing directory...")
file_types, total_chars, total_lines, directory_tree = analyze_directory(parent_directory)
print("Writing summary to 'codesummary.txt'...")
write_summary_to_file(file_types, total_chars, total_lines, directory_tree, output_file)
print("Analysis complete.")