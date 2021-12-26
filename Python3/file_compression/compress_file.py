import os
import sys
import gzip
import shutil
import argparse

parser = argparse.ArgumentParser(description='Read a file, Compress the contents, Save the new file to a new destination.')
parser.add_argument('-ip', '--deviceIp', help='Device Ip')
parser.add_argument('-classification', '--classification', help='Device Classification EG (router | agg | cpe')
parser.add_argument('-inputFile', '--inputFile', help='Input file location and name')
parser.add_argument('-outputFileDirectory', '--outputFileDirectory', help='Output file location')
parser.add_argument('-outputFileName', '--outputFileName', help='Output file name')

args                    = parser.parse_args()
deviceIp                = args.deviceIp
classification          = args.classification
inputFile               = args.inputFile
outputFileDirectory     = args.outputFileDirectory
outputFileName          = args.outputFileName

'''
If the path does not end in / add it to it to prevent incorrect file names
'''
if outputFileDirectory[-1] != '/':
    outputFileDirectory = outputFileDirectory + '/'

'''
ALLOW THE PROGRAM TO FIGURE OUT WHERE THE FILES TO OPEN ARE STORED
RELATIVE TO WHERE THE SCRIPT IS BEING CALLED FROM.

EG IF THIS IS RAN FROM YOUR HOME DIRECTORY PYTHON SEES A DIFFERENT PATH FOR FILES
EVEN IF THEY ARE STORED IN THE SAME DIRECTORY..
'''

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

print("Attempting to open file -> {}".format(inputFile))

'''
COMPRESS THE FILE AND SAVE TO IT'S NEW LOCATION
If the
'''
stop = False

"""
This section is used to flag a specific location for each file to save. 
For example if you are saving your router / core device files into a specific directory etc. 
"""
if (classification == 'router') or (classification == 'agg') or (classification == 'cpe'):
    destination_path = outputFileDirectory
else:
    stop = True

if stop:
    print("No where to save the file as it is an unknown device type!")
else:
    try:
        with open(inputFile, 'rb') as f_in:
            with gzip.open(outputFileDirectory + outputFileName, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    except:
        print("Error opening file")

'''
TEST READ
This is how to read the file back without all the rubbish
with gzip.open(destination_path + "Test_File_name", mode="rt") as f:
    file_content = f.read()
    print(file_content)
'''
