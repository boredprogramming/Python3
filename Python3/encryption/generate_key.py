'''
This file will take in a name and generate a unique key for
encryption purposes.
In essence, the file name acts as a token to generate a key that will encrypt / decrypt a file
'''

import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def my_key(pass_phrase):
    """
    Custom variables - You will need to set these before using.
    The pass_phrase can be whichever variable you would like to identify how to make your encryption key.
    This can be something as simple as the filename postended with something like the date / time / minute of creation
    which will essentially give you a unique passphrase for each file.

    There are better ways to generate these, but that would be the simplest.
    and you would not need to store the key anywhere as it would always generate the appropriate
    string for encryption / decryption as long as the same pass phrase is passed in and you are using the same iterations
    value each time.

    Iterations could also be varried depending on how you want to implement this as long as it's also a unique value
    per file encrypted.

    Along with that, you can also change your salt value to something unique as well for each file.
    This is a 16 byte string. An example is used below.
    """
    iterations = "SOME INTEGER VALUE HERE"
    salt = b"\xb9\x1f|}'S\xa1\x96\xeb\x154\x04\x88\xf3\xdf\x05"
    '''
    Use the file name as the password
    '''
    if pass_phrase:
        password_provided = pass_phrase
        password = password_provided.encode()
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                        length=32,
                        salt=salt,
                        iterations=iterations,
                        backend=default_backend())
        secondary_key = str(Fernet.generate_key(), 'UTF-8')
        key = str(base64.urlsafe_b64encode(kdf.derive(password)), 'UTF-8')
        return_this = key + '::' + secondary_key
        return return_this
    else:
        return False

print(my_key("Test"))