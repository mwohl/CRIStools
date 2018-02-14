import os
import csv
import json
import subprocess
from pprint import pprint
from collections import defaultdict
import copy

pathToDropboxFiles = "C:\Users\molly\Documents\BaxterLab\CRIS\AutomatedCRISDataTesting\DropboxFiles"
pathToCRISFiles = "C:\Users\molly\Documents\BaxterLab\CRIS\AutomatedCRISDataTesting\CRISFiles"
reportFile = "C:\Users\molly\Documents\BaxterLab\CRIS\AutomatedCRISDataTesting\Report.txt"

DropboxFiles = os.listdir(pathToDropboxFiles)
CRISFiles = os.listdir(pathToCRISFiles)

reportObj = {}
reportObj['noCRISfileFound'] = []
reportObj['diffNumCols'] = []
reportObj['sameNumCols'] = {}
reportObj['sameNumCols']['rowsAdded'] = {}
reportObj['sameNumCols']['rowsRemoved'] = {}
reportObj['sameNumCols']['rowValuesChanged'] = {}
reportObj['sameNumCols']['rowValuesChangedColsFiles'] = defaultdict(list)

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

		with open(os.path.join(pathToDropboxFiles, file), 'r') as Dfile, open(os.path.join(pathToCRISFiles, ("CRIS_"+file)), 'r') as Cfile:
			fileDReader = csv.DictReader(Dfile)
			fileCReader = csv.DictReader(Cfile)
			
			colInFileDOnly, colInFileCOnly = sameNumCols(fileDReader, fileCReader)
			if not colInFileDOnly and not colInFileCOnly:
				subprocess.call(['csvdiff', '--style', 'pretty','--output', 'diff.json', 'sample', os.path.join(pathToDropboxFiles, file), os.path.join(pathToCRISFiles, ("CRIS_"+file))], shell=True)
				diffData = json.load(open('diff.json'))

				changedCols = []
				for item in diffData['changed']:
					for subitem in item['fields']:
						if subitem not in changedCols:
							changedCols.append(subitem)
				reportObj['sameNumCols']['rowValuesChanged'][file] = sorted(changedCols)

				if len(diffData['added']) != 0:
					reportObj['sameNumCols']['rowsAdded'][file] = len(diffData['added'])
				if len(diffData['removed']) != 0:
					reportObj['sameNumCols']['rowsRemoved'][file] = len(diffData['removed'])

			else:
				reportObj['diffNumCols'].append(file)

	else:
		reportObj['noCRISfileFound'].append(file)

# Group files with same changed columns:
origDict = reportObj['sameNumCols']['rowValuesChanged']
for key, value in sorted(origDict.iteritems()):
	reportObj['sameNumCols']['rowValuesChangedColsFiles'][tuple(value)].append(key)

with open(reportFile, 'w') as report:
	origSummaryDict = reportObj['sameNumCols']['rowValuesChangedColsFiles']
	# Because the list of files is built up iteratively above and a dictionary key must be immutable,
	# we must have the filenames as values in the dict initially, then we can flip the keys with the tuplized values
	reportObj['sameNumCols']['rowValuesChangedSummary'] = {(tuple(v)): k for k, v in origSummaryDict.iteritems()}
	# Make a deep copy of the reportObj, then remove unnecessary items from the copy (finalReportObj) before writing to file
	finalReportObj = copy.deepcopy(reportObj)
	del finalReportObj['sameNumCols']['rowValuesChanged']
	del finalReportObj['sameNumCols']['rowValuesChangedColsFiles']
	pprint(finalReportObj, stream=report)