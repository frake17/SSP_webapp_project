# EMail: Hr@gmail.com
# password: HRPa$$w0rd
import bcrypt
from cryptography.fernet import Fernet

password = 'HRPa$$w0rd'
salt = bcrypt.gensalt(rounds=16)
# A hashed value is created with hashpw() function, which takes the cleartext value and a salt as
# parameters.
hash_password = bcrypt.hashpw(password.encode(), salt)
print(hash_password)

phone = '1111 1111'
key = Fernet.generate_key()
f = Fernet(key)
phone = f.encrypt(phone.encode())
print(key)
print(phone)

email = 'shengsionghr@gmail.com'
key = Fernet.generate_key()
# Load the key into the Crypto API
print('key: ', key)
print('key(decode): ', key.decode('utf-8'))
f = Fernet(key)
# Encrypt the email and convert to bytes by calling f.encrypt()
encryptedEmail = f.encrypt(email.encode())
print(encryptedEmail)

decryptedEmail = f.decrypt(encryptedEmail)
print(decryptedEmail)
