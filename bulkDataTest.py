import os
import csv
import json
import subprocess

pathToDropboxFiles = "C:\Users\molly\Documents\BaxterLab\CRIS\AutomatedCRISDataTesting\DropboxFiles"
pathToCRISFiles = "C:\Users\molly\Documents\BaxterLab\CRIS\AutomatedCRISDataTesting\CRISFiles"

reportFile = "C:\Users\molly\Documents\BaxterLab\CRIS\AutomatedCRISDataTesting\Report.txt"

DropboxFiles = os.listdir(pathToDropboxFiles)
CRISFiles = os.listdir(pathToCRISFiles)
report = open(reportFile, 'w')

def sameNumCols(fileDReader, fileCReader):
	colInFileDOnly = []
	colInFileCOnly = []

	headersD = fileDReader.fieldnames
	headersC = fileCReader.fieldnames

	for header in headersD:
		if header not in headersC:
			colInFileDOnly.append(header)
	for header in headersC:
		if header not in headersD:
			colInFileCOnly.append(header)

	return colInFileDOnly, colInFileCOnly

for file in DropboxFiles:
	if "CRIS_"+file in CRISFiles:
		report.write(file+ " found in CRIS folder.\n")

		with open(os.path.join(pathToDropboxFiles, file), 'r') as Dfile, open(os.path.join(pathToCRISFiles, ("CRIS_"+file)), 'r') as Cfile:
			fileDReader = csv.DictReader(Dfile)
			fileCReader = csv.DictReader(Cfile)
			
			colInFileDOnly, colInFileCOnly = sameNumCols(fileDReader, fileCReader)
			report.write("\tCOLUMN # TEST:\n")
			if not colInFileDOnly and not colInFileCOnly:
				report.write("\tSame number of columns in each file.\n")
				subprocess.call(['csvdiff', '--style', 'pretty','--output', 'diff.json', 'sample', os.path.join(pathToDropboxFiles, file), os.path.join(pathToCRISFiles, ("CRIS_"+file))], shell=True)
				diffData = json.load(open('diff.json'))
				
				numAdded = len(diffData['added'])
				report.write("\t\tNumber of Records Added in CRIS version = "+str(numAdded)+"\n")
				numRemoved = len(diffData['removed'])
				report.write("\t\tNumber of Records Removed in CRIS version = "+str(numRemoved)+"\n")
				numChanged = len(diffData['changed'])
				report.write("\t\tNumber of Records with Values Changed between versions = "+str(numChanged)+"\n")
				# Here, within each iteration of the for loop, need to parse out what we want from each diff.json to add to a summary report

				changedCols = []
				for item in diffData['changed']:
					for subitem in item['fields']:
						if subitem not in changedCols:
							changedCols.append(subitem)
				report.write("\t\tColumns with issue detected:\n")
				for item in changedCols:
					report.write("\t\t\t"+item+"\n")

			else:
				report.write("\tDifferent number of columns in each file.\n")
				report.write("\t\tColumns present in Dropbox version only: \n")
				for col in colInFileDOnly:
					report.write("\t\t\t"+col+"\n")
				report.write("\t\tColumns present in CRIS version only: \n")
				for col in colInFileCOnly:
					report.write("\t\t\t"+col+"\n")

	else:
		report.write(file+ " not found in CRIS folder.\n")