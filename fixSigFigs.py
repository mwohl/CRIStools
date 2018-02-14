import os
import csv
import math
from decimal import *

#colsToFix is list of columns that need to be adjusted to 4 sigfigs
colsToFix = ["B11",
			"Na23",
			"Mg25",
			"Al27",
			"P31",
			"S34",
			"K39",
			"Ca43",
			"Mn55",
			"Fe57",
			"Co59",
			"Ni60",
			"Cu65",
			"Zn66",
			"Zn64",
			"Zn67",
			"Zn68",
			"As75",
			"Se82",
			"Rb85",
			"Sr88",
			"Mo98",
			"Cd111",
			"In115",
			"B11_intensity",
			"B11_conc",
			"B11_IScorrConc",
			"B11_corrConc",
			"B11_normConc",
			"B11_RSD",
			"Na23_intensity",
			"Na23_conc",
			"Na23_IScorrConc",
			"Na23_corrConc",
			"Na23_normConc",
			"Na23_RSD",
			"Mg26_intensity",
			"Mg26_conc",
			"Mg26_IScorrConc",
			"Mg26_corrConc",
			"Mg26_normConc",
			"Mg26_RSD",
			"Al27_intensity",
			"Al27_conc",
			"Al27_IScorrConc",
			"Al27_corrConc",
			"Al27_normConc",
			"Al27_RSD",
			"P31_intensity",
			"P31_conc",
			"P31_IScorrConc",
			"P31_corrConc",
			"P31_normConc",
			"P31_RSD",
			"S34_intensity",
			"S34_conc",
			"S34_IScorrConc",
			"S34_corrConc",
			"S34_normConc",
			"S34_RSD",
			"K39_intensity",
			"K39_conc",
			"K39_IScorrConc",
			"K39_corrConc",
			"K39_normConc",
			"K39_RSD",
			"Ca44_intensity",
			"Ca44_conc",
			"Ca44_IScorrConc",
			"Ca44_corrConc",
			"Ca44_normConc",
			"Ca44_RSD",
			"Fe54_intensity",
			"Fe54_conc",
			"Fe54_IScorrConc",
			"Fe54_corrConc",
			"Fe54_normConc",
			"Fe54_RSD",
			"Mn55_intensity",
			"Mn55_conc",
			"Mn55_IScorrConc",
			"Mn55_corrConc",
			"Mn55_normConc",
			"Mn55_RSD",
			"Co59_intensity",
			"Co59_conc",
			"Co59_IScorrConc",
			"Co59_corrConc",
			"Co59_normConc",
			"Co59_RSD",
			"Ni60_intensity",
			"Ni60_conc",
			"Ni60_IScorrConc",
			"Ni60_corrConc",
			"Ni60_normConc",
			"Ni60_RSD",
			"Cu63_intensity",
			"Cu63_conc",
			"Cu63_IScorrConc",
			"Cu63_corrConc",
			"Cu63_normConc",
			"Cu63_RSD",
			"Zn66_intensity",
			"Zn66_conc",
			"Zn66_IScorrConc",
			"Zn66_corrConc",
			"Zn66_normConc",
			"Zn66_RSD",
			"Zn64_intensity",
			"Zn64_conc",
			"Zn64_IScorrConc",
			"Zn64_corrConc",
			"Zn64_normConc",
			"Zn64_RSD",
			"Zn67_intensity",
			"Zn67_conc",
			"Zn67_IScorrConc",
			"Zn67_corrConc",
			"Zn67_normConc",
			"Zn67_RSD",
			"Zn68_intensity",
			"Zn68_conc",
			"Zn68_IScorrConc",
			"Zn68_corrConc",
			"Zn68_normConc",
			"Zn68_RSD",
			"As75_intensity",
			"As75_conc",
			"As75_IScorrConc",
			"As75_corrConc",
			"As75_normConc",
			"As75_RSD",
			"Se78_intensity",
			"Se78_conc",
			"Se78_IScorrConc",
			"Se78_corrConc",
			"Se78_normConc",
			"Se78_RSD",
			"Se82_intensity",
			"Se82_conc",
			"Se82_IScorrConc",
			"Se82_corrConc",
			"Se82_normConc",
			"Se82_RSD",
			"Rb85_intensity",
			"Rb85_conc",
			"Rb85_IScorrConc",
			"Rb85_corrConc",
			"Rb85_normConc",
			"Rb85_RSD",
			"Sr88_intensity",
			"Sr88_conc",
			"Sr88_IScorrConc",
			"Sr88_corrConc",
			"Sr88_normConc",
			"Sr88_RSD",
			"Y89_intensity",
			"Y89_conc",
			"Y89_IScorrConc",
			"Y89_corrConc",
			"Y89_normConc",
			"Y89_RSD",
			"Mo98_intensity",
			"Mo98_conc",
			"Mo98_IScorrConc",
			"Mo98_corrConc",
			"Mo98_normConc",
			"Mo98_RSD",
			"Cd111_intensity",
			"Cd111_conc",
			"Cd111_IScorrConc",
			"Cd111_corrConc",
			"Cd111_normConc",
			"Cd111_RSD",
			"In115_intensity",
			"In115_conc",
			"In115_IScorrConc",
			"In115_corrConc",
			"In115_normConc",
			"In115_RSD",
			"Mg25_intensity",
			"Mg25_conc", 
			"Mg25_corrConc",
			"Mg25_IScorrConc",
			"Mg25_normConc",
			"Mg25_RSD",
			"Ca43_intensity",
			"Ca43_conc",
			"Ca43_corrConc",
			"Ca43_IScorrConc",
			"Ca43_normConc",
			"Ca43_RSD",
			"Fe57_intensity",
			"Fe57_conc",
			"Fe57_corrConc",
			"Fe57_IScorrConc",
			"Fe57_normConc",
			"Fe57_RSD",
			"Cu65_intensity",
			"Cu65_conc",
			"Cu65_corrConc",
			"Cu65_IScorrConc",
			"Cu65_normConc",
			"Cu65_RSD",
			"Se82_intensity",
			"Se82_conc",
			"Se82_corrConc",
			"Se82_IScorrConc",
			"Se82_normConc",
			"Se82_RSD",
			"weight",
			"SampleWeight"]
###################################################################################################################################
pathToDropboxFiles = "C:/Users/molly/Downloads/tmp_Dropbox"
pathToCRISFiles = "C:/Users/molly/Downloads/tmp_CRIS"
pathToSFFDropboxFiles = "C:/Users/molly/Downloads/tmp_SFF_Dropbox"
pathToSFFCRISFiles = "C:/Users/molly/Downloads/tmp_SFF_CRIS"

DropboxFiles = os.listdir(pathToDropboxFiles)
CRISFiles = os.listdir(pathToCRISFiles)
####################################################################################################################################
def round_to_sigfigs(x, n):
	#### returns x rounded to n significant figures ####
	#return round(x, int(n - math.ceil(math.log10(abs(x)))))
	roundedFloat = round(x, -int(math.floor(math.log10(abs(x))) - (n - 1)))
	#return str("{:0>2f}".format(roundedFloat))
	#return Decimal(roundedFloat).quantize(Decimal('.01'))
	return round(x, 2)

for file in DropboxFiles:
	with open(os.path.join(pathToDropboxFiles, file), 'rU') as fileToFix, open(os.path.join(pathToSFFDropboxFiles, ("SFF_"+file)), 'wb') as fixedFile:
		reader = csv.DictReader(fileToFix)
		fieldnames = reader.fieldnames
		writer = csv.DictWriter(fixedFile, fieldnames)
		writer.writeheader()

		for row in reader:
			for col in colsToFix:
				if col in fieldnames:
					if (row[col] != "NA"):
						try:
							toFix = float(row[col])
							row[col] = round_to_sigfigs(toFix, 4)
						except ValueError:
							row[col] = "oops"
			writer.writerow(row)
		print "fixed file " + file

for file in CRISFiles:
	with open(os.path.join(pathToCRISFiles, file), 'rU') as fileToFix, open(os.path.join(pathToSFFCRISFiles, ("SFF_"+file)), 'wb') as fixedFile:
		reader = csv.DictReader(fileToFix)
		fieldnames = reader.fieldnames
		writer = csv.DictWriter(fixedFile, fieldnames)
		writer.writeheader()

		for row in reader:
			for col in colsToFix:
				if col in fieldnames:
					if (row[col] != "NA"):
						try:
							toFix = float(row[col])
							row[col] = round_to_sigfigs(toFix, 4)
						except ValueError:
							row[col] = "oops"
					elif (row[col] == ""):
						row[col] = "empty"
			writer.writerow(row)
		print "fixed file " + file