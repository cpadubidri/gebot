import os
from cryptography.fernet import Fernet

class CredentialManager:
    __version__='1.0'
    
    def __init__(self, key_file='./key/key.key', data_file='./resources/cred.dat'):
        self.key_file = key_file
        self.data_file = data_file
        self.key = self.getKey()

    def getKey(self):
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as key_file:
                key = key_file.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as key_file:
                key_file.write(key)
        return key

    def encrypt(self, email, password):
        cipher = Fernet(self.key)
        encrypted_email = cipher.encrypt(email.encode())
        encrypted_password = cipher.encrypt(password.encode())

        with open(self.data_file, 'wb') as data_file:
            data_file.write(encrypted_email + b'\n')
            data_file.write(encrypted_password)

    def decrypt(self):
        cipher = Fernet(self.key)

        with open(self.data_file, 'rb') as data_file:
            encrypted_email = data_file.readline().strip()
            encrypted_password = data_file.readline()

        decrypted_email = cipher.decrypt(encrypted_email).decode()
        decrypted_password = cipher.decrypt(encrypted_password).decode()

        return decrypted_email, decrypted_password
    

    def __getattr__(self, attrib):
        if attrib=="__version__":
            return self.__version__
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{attrib}'")

if __name__== "__main__":
    credential_manager = CredentialManager()
    adminemail = "padubidrichirag0@gmail.com"
    adminpassword = "xxxxx"
    credential_manager.encrypt(adminemail, adminpassword)

