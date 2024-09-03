# MAL
Removes antivirus

Target All File Types: The code is designed to handle any file type without restrictions. It reads files in binary mode, which allows it to process any kind of file, including images, documents, and executable files.

Directory Support: The encrypt_directory function allows you to encrypt all files within a specified directory, making it easy to handle multiple files at once.

Robust Logging: The logging statements provide feedback on the operations performed, errors encountered, and successful encryption or decryption.

Usage
To encrypt a single file:
python MAL.py encrypt path_to_your_file --password YourStrongPasswordHere

To encrypt all files in a directory:
python MAL.py encrypt path_to_your_directory --password YourStrongPasswordHere

To decrypt a single encrypted file:
python MAL.py decrypt path_to_your_encrypted_file.encrypted --password YourStrongPasswordHere
