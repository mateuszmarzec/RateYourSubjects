import hashlib, binascii
import os
import base64


def create_password_hash(password):
    salt = binascii.hexlify(os.urandom(16))
    hash = binascii.hexlify(hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000, dklen=None))
    return salt.decode(), hash.decode()


def check_password(salt, hash, password):
    if hash == binascii.hexlify(
            hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000, dklen=None)).decode():
        return True
    else:
        return False


# string to chect te password 1234567890-=QWERTYUIOP{}|ASDFGHJKL:zxcvbnm,./<>:ąśćńźżółąĄŚŹŻÓ

# New with Polski singns
# dla python3
def encode(clear):
    key = '559609be873940010b28422432beea50'
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)))
        enc.append(enc_c)
    return "".join(enc).encode()


'''
Ta wersja kodowanie nie potrafi kodować polskich znaków
#dla pythona 2
def encode(clear):
    key = '559609be873940010b28422432beea50'
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = unichr((ord(clear[i]) + ord(key_c)))
        enc.append(enc_c)

    return "".join(enc).encode("utf-8")
'''


# Dla python2
def decode(enc):
    key = '559609be873940010b28422432beea50'
    dec = []
    enc = enc.decode('utf-8')
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = unichr((ord(enc[i]) - ord(key_c)))
        dec.append(dec_c)
    return "".join(dec)

# ----------------------------------------------------------------------------------
