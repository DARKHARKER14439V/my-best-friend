import os
import zipfile
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import urlsafe_b64encode, urlsafe_b64decode
import secrets
import sys

def zip_folder(folder_path, zip_name="repo_temp.zip"):
    """Compress the entire folder into a zip file"""
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, folder_path)
                zipf.write(full_path, rel_path)
    return zip_name

def derive_key(password: str, salt: bytes):
    """Derive a 256-bit AES key from the password"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=200000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt_file(input_file, output_file, password):
    """Encrypt file using AES-256-GCM"""
    salt = secrets.token_bytes(16)
    iv = secrets.token_bytes(12)
    key = derive_key(password, salt)

    with open(input_file, 'rb') as f:
        data = f.read()

    encryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv),
        backend=default_backend()
    ).encryptor()

    encrypted_data = encryptor.update(data) + encryptor.finalize()

    with open(output_file, 'wb') as f:
        f.write(salt + iv + encryptor.tag + encrypted_data)

    print(f"🔒 Encrypted successfully -> {output_file}")

def decrypt_file(encrypted_file, output_file, password):
    """Decrypt the AES-GCM encrypted file"""
    with open(encrypted_file, 'rb') as f:
        salt = f.read(16)
        iv = f.read(12)
        tag = f.read(16)
        encrypted_data = f.read()

    key = derive_key(password, salt)

    decryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv, tag),
        backend=default_backend()
    ).decryptor()

    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    with open(output_file, 'wb') as f:
        f.write(decrypted_data)

    print(f"🔓 Decrypted successfully -> {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:\n  lock_repo.py lock <folder_path>\n  lock_repo.py unlock <lockfile>")
        sys.exit(1)

    mode = sys.argv[1].lower()
    target = sys.argv[2]
    password = "Ayush@2009"  # Your password (you can change this)

    if mode == "lock":
        zip_name = zip_folder(target)
        encrypt_file(zip_name, "repo.lock", password)
        os.remove(zip_name)  # clean up
    elif mode == "unlock":
        decrypt_file(target, "repo_unlocked.zip", password)
        print("Now unzip 'repo_unlocked.zip' to access your files.")
    else:
        print("Unknown command. Use 'lock' or 'unlock'.")
