# This script strips the first four characters
# from the names of all files in the directory
# whose path is given in the command line argument
import os

pathname = "C:\Users\molly\Documents\BaxterLab\CRIS\AutomatedCRISDataTesting\SFF_CRISFiles"

directory = os.listdir(pathname)

for file in directory:
	os.rename((os.path.join(pathname, file)), (os.path.join(pathname, file[4:])))
print "Done renaming files"
