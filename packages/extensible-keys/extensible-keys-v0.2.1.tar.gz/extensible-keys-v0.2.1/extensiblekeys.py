import hashlib
import base64
import os

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# raised when an .ekf file cannot be parsed
class EkfFileError(Exception):
    def __init__(self, message: str = "Invalid .ekf file"):
        super().__init__(message)


# raised when a key is incorrect or a checksum is failed
class DecryptionError(ValueError):
    def __init__(self, message: str = 'Failed to decrypt file'):
        super().__init__(message)


# creates a SHA-256 hash of all the keys in a file with salt
def create_checksum(keys: dict, salt: bytes) -> bytes():
    checksum = bytes()
    for i in keys.values():
        checksum += i
    return hashlib.sha256(checksum+salt).digest()


# creates a file given a dictionary of keys and a password of any length
def write_file(file_name: str, keys: dict, pw: str):
    # validate file name
    if not file_name.endswith('.ekf'):
        raise ValueError('Invalid File Extension')
    elif os.path.exists(file_name):
        raise FileExistsError()
    # generate cryptographic information
    salt = get_random_bytes(16)
    iv = get_random_bytes(16)
    # a string to be written to the file as the final step of the function
    output = f'{base64.b64encode(salt).decode("ascii")}:{base64.b64encode(iv).decode("ascii")}\nSTART KEYS:\n'
    titles = []
    # generate an AES cipher from the given password and previously generated cryptographic info
    aes_key = hashlib.sha256(pw.encode("utf-8")+salt).digest()
    cipher = AES.new(hashlib.sha256(pw.encode("utf-8")+salt).digest(), AES.MODE_CBC, iv)
    for title in keys:
        # validate key title
        key = keys[title]
        if ':' in title or title == "START KEYS:\n" or title == "STOP KEYS!":
            raise ValueError(f"Invalid Key Title: {title}")
        elif title in titles:
            raise ValueError(f"Repeat Key Title: {title}")
        # encrypt key if asked and save it to output
        if "*" in title:
            data = cipher.encrypt(pad(key, 16))
        else:
            data = key
        output += f'{title}: {base64.b64encode(data).decode("ascii")}\n'
        titles.append(title)
    # generate and store checksum
    output += 'STOP KEYS!\nCHECKSUM: '
    output += base64.b64encode(cipher.encrypt(pad(create_checksum(keys, salt), 16))).decode("ascii")
    # save output 
    with open(file_name, 'w') as f:
        f.write(output)
   

# loads keys from  a file and unencrypts them as needed.
def read_file(file_name: str, pw: str) -> dict:
    # validate .ekf file
    if not file_name.endswith('.ekf'):
        raise EkfFileError()
    with open(file_name) as k: 
        key_dat = k.readlines()
        if key_dat[1] != 'START KEYS:\n' or key_dat[-2] != 'STOP KEYS!\n' or not key_dat[-1].startswith('CHECKSUM:'):
            raise EkfFileError()
    keys = {}
    salt, iv = key_dat[0].split(':')
    salt = base64.b64decode(salt.encode('ascii'))
    iv = base64.b64decode(iv.replace('\n', '').encode('ascii'))
    cipher = AES.new(hashlib.sha256(pw.encode("utf-8")+salt).digest(), AES.MODE_CBC, iv)
    for i in key_dat[2:]:
        if 'STOP KEYS!' in i:
            break
        title, key = i.split(': ')
        key = key.replace('\n', '')
        if '*' in title:
            # decrypt keys if required
            try:
                keys[title] = unpad(cipher.decrypt(base64.b64decode(key.encode("ascii"))), 16)
            # padding errors are presented as value errors, so this is used to make padding errors indistinguishable from
            # the error raised by using an incorrect key (with correct padding), or an invlaid checksum, removing, or at 
            # least mitigating the risk of padding oracle attacks 
            except ValueError: 
                raise DecryptionError()
            
        else: 
            keys[title] = base64.b64decode(key.encode('ascii'))
    # generate and validate a checksum, if it suceeds the function returns the keys, otherwise it raises an error
    checksum = create_checksum(keys, salt)
    check = key_dat[-1].replace('CHECKSUM: ', '')
    if unpad(cipher.decrypt(base64.b64decode(check.encode("ascii"))), 16) != checksum:
        return 'File could not be decrypted'
    return keys


# adds key(s) to a file without disrupting any of the current ones
def append_key(file_name: str, new_keys: dict, pw: str):
    keys =  read_file(file_name, pw)
    keys = keys | new_keys
    os.remove(file_name)
    write_file(file_name, keys, pw)


# removes key(s) from a file
def delete_keys(file_name: str, target_keys: tuple, pw: str):
    keys = read_file(file_name, pw)
    for i in target_keys:
        try:
            del keys[i]
        except KeyError:
            raise ValueError(f'Key {i} not found!')
    os.remove(file_name)
    write_file(file_name, keys, pw)
    
