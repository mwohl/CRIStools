import pandas as pd
import csv

origFileLocation = "C:\Users\molly\Documents\BaxterLab\CRIS\AutomatedCRISDataTesting\CRISexperimentList.csv"

df = pd.read_csv(origFileLocation)

all_cris_files = df['cris']
cris_files = df.cris.dropna()

cris_files = cris_files.astype(int)

expected_files = df['expected']
expected_files.convert_objects(convert_numeric=True)

print "CRIS files not in expected:"

inCRISnotExp = []
inExpnotCRIS = []

for item in cris_files:
	if item not in expected_files:
		inCRISnotExp.append(item)
		#print item

print "Expected files not in CRIS:"

for item in expected_files:
	if item not in cris_files:
		inExpnotCRIS.append(item)
		#print item

with open("C:\Users\molly\Documents\BaxterLab\CRIS\AutomatedCRISDataTesting\inCRISnotExp.csv", 'wb') as f1:
	writer = csv.writer(f1)
	for val in inCRISnotExp:
		writer.writerow([val])

with open("C:\Users\molly\Documents\BaxterLab\CRIS\AutomatedCRISDataTesting\inExpnotCRIS.csv", 'wb') as f2:
	writer = csv.writer(f2)
	for val in inExpnotCRIS:
		writer.writerow([val])

