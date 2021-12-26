from additional_directories import production_paths
import sys
'''
Append the system path with where the script will be ran, This may differ
from computer (Test bed) to the deployed server.
'''
for path in production_paths:
    sys.path.append(path)

import os
import re
import generate_key
import gzip
import shutil
import argparse
from cryptography.fernet import Fernet
from datetime import datetime
date = datetime.now().strftime("%Y_%m_%d_%I_%M_%S_%p")


'''
Add a few safeguards on what files are allowed to be encrypted. 
'''

allowed_file_extensions = ['gz', 'txt', 'zip']

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

'''
ALLOW THE PROGRAM TO FIGURE OUT WHERE THE FILES TO OPEN ARE STORED
RELATIVE TO WHERE THE SCRIPT IS BEING CALLED FROM.

EG IF THIS IS RAN FROM YOUR HOME DIRECTORY PYTHON SEES A DIFFERENT PATH FOR FILES
EVEN IF THEY ARE STORED IN THE SAME DIRECTORY..

'''
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

parser = argparse.ArgumentParser(description='Encrypt a file, Save to a new location, Delete the old file')
parser.add_argument('-original_file', '--original_file', help='File location and name')
parser.add_argument('-destination_file_location', '--destination_file_location', help='Destination file location')
parser.add_argument('-destination_file_name', '--destination_file_name', help='Destination file name')

args                        = parser.parse_args()
original_file               = args.original_file
destination_file_location   = args.destination_file_location
destination_file_name       = args.destination_file_name

stop = False
if destination_file_name:
    keys = generate_key.my_key(destination_file_name + "_" + date + ".ENC")
    key_regex = r'^(.*)::(.*)$'
    key_regex = re.compile(key_regex)
    k = key_regex.search(keys)
else:
    stop = True

if not stop:
    if (k[1] and k[2]):
        '''
        k[0] -> full match on the keys string
        k[1] -> File name -> Token
        '''
        token = k[1]
        file_regex = r'(/((\d{1,3})\.){3}(\d{1,3}).*\.' + extensions + ')$'
        file_regex = re.compile(file_regex)
        file = file_regex.search(original_file)
        if file:
            '''
            Validate the user passed in a file and NOT a directory only
            '''
            isFile = os.path.isfile(original_file)
            isDirectory = os.path.isdir(original_file)
            if isDirectory:
                sys.stdout.write("Failed - Original file CANNOT be a directory")
                sys.stdout.flush()
                sys.exit(0)
            elif isFile:
                if file:
                    """
                    The submitted file is in the list of allowed file extensions
                    """
                    if destination_file_location:
                        destinationIsDirectory = os.path.isdir(destination_file_location)
                        if destinationIsDirectory:
                            if destination_file_location[-1] != '/':
                                '''
                                Formats the destination directory to add a / to the end if it's missing.
                                '''
                                destination_file_location = destination_file_location + "/"

                            if destination_file_name:
                                '''
                                Passes all checks up to this point. Encrypt the file and save
                                The file names will be post pended with the date / timestamp the script was ran
                                '''
                                try:
                                    '''
                                    Compress the file
                                    Save to a gz file
                                    '''
                                    with open(original_file, 'rb') as orig_file:
                                        with gzip.open(destination_file_location + destination_file_name + "_" + date + ".gz", 'wb') as zipped_file:
                                            zipped_file.writelines(orig_file)
                                    f = Fernet(token)

                                    with open(destination_file_location + destination_file_name + "_" + date + ".gz", "rb") as file:
                                        file_data = file.read()

                                    '''
                                    Remove the old gz file
                                    '''
                                    os.remove(destination_file_location + destination_file_name + "_" + date + ".gz")

                                    '''
                                    Encrypt the data
                                    '''
                                    encrypted_data = f.encrypt(file_data)

                                    '''
                                    Write the encrypted file
                                    '''
                                    with open(destination_file_location + destination_file_name + "_" + date + ".ENC", "wb") as file:
                                        file.write(encrypted_data)

                                    '''
                                    Print out the location of the final file
                                    '''
                                    sys.stdout.write(destination_file_location + destination_file_name + "_" + date + ".ENC")
                                    sys.stdout.flush()
                                    sys.exit(0)
                                except Exception as ex:
                                    sys.stdout.write("Error opening / encrypting original file ... Aborting")
                                    sys.stdout.flush()
                                    sys.exit(0)
                            else:
                                sys.stdout.write("No destination filename provided ... Aborting")
                                sys.stdout.flush()
                                sys.exit(0)
                    else:
                        sys.stdout.write("No destination provided")
                        sys.stdout.flush()
                        sys.exit(0)
    else:
        sys.stdout.write("Failed")
        sys.stdout.flush()
        sys.exit(0)





