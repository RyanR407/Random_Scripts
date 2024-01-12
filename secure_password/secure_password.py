
'''
This Python script includes a function generate_password() for generating a random password. The generated password adheres to common security standards, including a mix of uppercase and lowercase letters, digits, and special characters. The length of the password is randomly set to be 12 to 64 characters. Here's a breakdown of how it works:
1. Password Length: The script determines the password length randomly, choosing a length be 12 to 64 characters.
2. Character Pools: It defines four character pools - uppercase letters, lowercase letters, digits, and special characters (punctuation).
3. Initial Character: The script ensures the password starts with a random letter (either uppercase or lowercase) for additional complexity.
4. Random Character Selection: The remaining characters are chosen randomly from the four defined pools until the password reaches the intended length.
5. Shuffling: After the initial letter, the rest of the password characters are shuffled to randomize their order and enhance security.
6. Password Assembly: The script then assembles the complete password and returns it as a string.
7. Execution and Output: The generate_password() function is called, and the randomly generated password is printed to the console.

How to Use This Script: 
1. Run the Script: Execute this script in a Python environment.
2. Obtain Password: The script will output a randomly generated password, which you can use for your applications or accounts.
3. Customization: If needed, you can modify the character pools or the password length range by editing the script.

Use Cases:
1. Generating secure passwords for new user accounts.
2. Creating passwords for testing purposes in development environments.

Note: While this script generates strong passwords, it's important to use a secure method to store and manage your passwords, such as a password manager. Avoid using simple, predictable modifications of the generated passwords, as it can reduce their security.
'''

import secrets
import string

import secrets
import string

import secrets
import string

def generate_password(length):
    """
    Generates a random password starting with a letter and containing a mix of
    uppercase, lowercase, digits, and special characters. The length of the
    password is determined by the user input.
    """
    # Define character pools
    char_pools = [string.ascii_uppercase, string.ascii_lowercase, string.digits, string.punctuation]
    
    # Start with a random letter
    password = [secrets.choice(string.ascii_letters)]

    # Randomly select characters from different pools
    while len(password) < length:
        char_pool = secrets.choice(char_pools)
        password.append(secrets.choice(char_pool))

    # Shuffle the password, except the first character
    rest_of_password = password[1:]
    secrets.SystemRandom().shuffle(rest_of_password)
    password = [password[0]] + rest_of_password

    return ''.join(password)

# Prompt user for password length
while True:
    user_input = input("Enter the desired password length (12 to 64) or 'q' to quit: ")
    if user_input.lower() == 'q':
        print("Exiting the password generator.")
        break
    try:
        length = int(user_input)
        if length >= 12 and length <= 64:
            random_password = generate_password(length)
            print("Randomly generated password:", random_password)
            break
        else:
            print("Password length must be 12 to 64 characters. Try again.")
    except ValueError:
        print("Invalid input. Please enter a number or 'q' to quit.")
