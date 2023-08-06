#!/usr/bin/env python3
import argparse
import os
import getpass
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import subprocess

def check_encryption(db_path):
    with open(db_path, 'rb') as f:
        header = f.read(16)
        if header == b'SQLite format 3\x00':
            return False
        else:
            return True

def encrypt_database(db_path, password, output_path):
    # Generate a random initialization vector
    iv = get_random_bytes(AES.block_size)

    # Derive a key from the password using PBKDF2
    salt = get_random_bytes(16)
    key = PBKDF2(password, salt, dkLen=32, count=100000)

    # Initialize the AES cipher with the key and the initialization vector
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Open the database file and read the contents
    with open(db_path, 'rb') as f:
        data = f.read()

    # Pad the data using PKCS7 padding
    padded_data = pad(data, AES.block_size, style='pkcs7')

    # Encrypt the padded data using the AES cipher and write it to the output file
    encrypted_data = cipher.encrypt(padded_data)
    with open(output_path, 'wb') as f:
        f.write(iv + salt + encrypted_data)

def decrypt_database(db_path, password, output_path):
    # Read the initialization vector, salt, and encrypted data from the database file
    with open(db_path, 'rb') as f:
        iv = f.read(AES.block_size)
        salt = f.read(16)
        encrypted_data = f.read()

    # Derive a key from the password using PBKDF2
    key = PBKDF2(password, salt, dkLen=32, count=100000)

    # Initialize the AES cipher with the key and the initialization vector
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt the data using the AES cipher and unpad it using PKCS7 padding
    try:
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size, style='pkcs7')
    except ValueError:
        raise ValueError("Incorrect decryption password.")
        return

    # Write the decrypted data to the output file
    with open(output_path, 'wb') as f:
        f.write(decrypted_data)

if __name__ == '__main__':
    # Parse the command line arguments
    print("""
    crypto_sqlite_browser - For Encrypting & Decrypting SQLite Databases and Browseing it useing litecli Browser
    GitHub : https://github.com/Crypt00o/crypto_sqlite_browser
    Mail : 0xCrypt00o@protonmail.com
    
    """)
    parser = argparse.ArgumentParser(description='Encrypt or decrypt a SQLite database.')
    parser.add_argument('db_path', help='the path to the database file')
    args = parser.parse_args()

    # Check if the database file exists
    if not os.path.isfile(args.db_path):
        print(f"Error: File '{args.db_path}' does not exist.")
        exit(1)

    # Check if the database is already encrypted
    is_encrypted = check_encryption(args.db_path)
    # Decrypt the database if it's already encrypted
    if is_encrypted:
        while True: 
            try:
                password = getpass.getpass(prompt='Enter the decryption password: ')
                decrypt_database(args.db_path, password, args.db_path)
                if not check_encryption(args.db_path):
                    print(f'Decrypted database {args.db_path} successfully.')
                    break
                else:
                    raise ValueError("Incorrect")
            except ValueError:
                print('[-] Incorrect Password')
                continue
            except KeyboardInterrupt:
                exit(0)

    # Open the database with litecli 
    print("\n[+] Starting LiteCli Session\n")
    subprocess.run(["litecli",args.db_path])
    if is_encrypted:
            # Encrypt the database
            encrypt_again = input("\n\nDo you want to encrypt the database with the same password again? (y/n): ")
            if encrypt_again.lower() == 'n':
                # Get a new password and encrypt the database
                while True:
                    new_password = getpass.getpass(prompt='Enter a new encryption password: ')
                    new_password2 = getpass.getpass(prompt='Repeat the new encryption password: ')
                    if new_password == new_password2:
                        encrypt_database(args.db_path, new_password, args.db_path)
                        if check_encryption(args.db_path):
                            print(f'Encrypted database {args.db_path} successfully.')
                            break
                        else:
                            print("[-] Some Thing Go Wrong While Encrypting")
                            exit(-1)
                    else:
                        print("[-] Passwords do not match.")
                        continue
            else :
                encrypt_database(args.db_path, password, args.db_path)
                if check_encryption(args.db_path):
                    print(f'Encrypted database {args.db_path} successfully.')
    else:
        while True:
                new_password = getpass.getpass(prompt='Enter a new encryption password: ')
                new_password2 = getpass.getpass(prompt='Repeat the new encryption password: ')
                if new_password == new_password2:
                    encrypt_database(args.db_path, new_password, args.db_path)
                    if check_encryption(args.db_path):
                        print(f'Encrypted database {args.db_path} successfully.')
                        break
                    else:
                        print("[-] Some Thing Go Wrong While Encrypting")
                        exit(-1)
                else:
                    print("Passwords do not match.") 
