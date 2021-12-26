from additional_directories import production_paths
import gzip
import argparse
import sys
'''
Append the system path with where the script will be ran, This may differ
from computer (Test bed) to the deployed server.
'''
for path in production_paths:
    sys.path.append(path)
import os
import re
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

from generate_key import my_key
from cryptography.fernet import Fernet, InvalidToken


'''
ALLOW THE PROGRAM TO FIGURE OUT WHERE THE FILES TO OPEN ARE STORED
RELATIVE TO WHERE THE SCRIPT IS BEING CALLED FROM.

EG IF THIS IS RAN FROM YOUR HOME DIRECTORY PYTHON SEES A DIFFERENT PATH FOR FILES
EVEN IF THEY ARE STORED IN THE SAME DIRECTORY..
'''

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

parser = argparse.ArgumentParser(description='Open an encrypted / compressed text file')
parser.add_argument('-file', '--file', help='File location and name of the file to open')

args               = parser.parse_args()
file               = args.file


'''
Add a few safeguards on what files are allowed to be encrypted. 

'''
allowed_file_extensions = ['ENC']
'''
Format the file extensions that are allowed to be encrypted. 
This will help format the regex statement for the checks
'''
extensions = "("
for x in allowed_file_extensions:
    extensions = extensions + x
    if x == allowed_file_extensions[-1]:
        extensions = extensions + ")"
    else:
        extensions = extensions + "|"

def decrypt(file):
    if file:
        '''
        Validate the file exists
        '''
        isFile = os.path.isfile(file)
        if isFile:
            file_regex = r'/(((\d{1,3})\.){3}(\d{1,3}).*\.' + extensions + ')$'
            file_regex = re.compile(file_regex)
            file_name = file_regex.search(file)
            if file_name:
                '''
                file[1] should be the file name only.
                '''
                token = my_key(file_name[1])
                key_regex = r'^(.*)::(.*)$'
                key_regex = re.compile(key_regex)
                k = key_regex.search(token)
                if k[1]:
                    '''
                    Attempt to decrypt the file with the generated key
                    '''
                    f = Fernet(k[1])

                    '''
                    Start of decryption
                    -Get the generated key
                    -Instantiate the f instance!
                        encrypted_data = f.encrypt(file_data)
                    '''
                    with open(file, "rb") as file:
                        '''
                        This decrypted data will be in the form of a gz file in a byte stream
                        '''
                        encrypted_data = file.read()
                    try:
                        decrypted_data = f.decrypt(encrypted_data)
                        contents = gzip.decompress(decrypted_data).decode()
                        sys.stdout.write(contents)
                        sys.stdout.flush()
                        sys.exit(0)
                    except InvalidToken as e:
                        print("Invalid Token")
                else:
                    print("Invalid key.")
            else:
                print("Invalid file type submitted")
        else:
            print("File does not exist. Aborting")
    else:
        print("No file selected")

decrypt(file)