import pandas as pd
import re
import logging
from datetime import datetime

class BadgerException(Exception):
    def __init__(self, message, row):
        print('Error: ' + message + ' at row ', row)

def checkRequiredFields(l, i):
	# Street, Zip, City, Last Check-in Date and Company.
	# 2 3 4 6 9
	required_fields = ['Street','Zip','City','Last Check-In Date','Company']
	index = 0
	while index < len(required_fields) and isinstance(l[required_fields[index]], str):
		index += 1

	# CHECK IF ROW HAS MINIMUM REQUIRED FIELDS
	if index < len(required_fields):
		BadgerException('Not enough required fields', i)

def quicksort(lst):
    if not lst:
        return []
    return (quicksort([x for x in lst[1:] if x <  lst[0]])
            + [lst[0]] +
            quicksort([x for x in lst[1:] if x >= lst[0]]))

# RE PATTERNS FOR PROCESSING DATAFRAME
datePattern = re.compile("([0]?[1-9]|[12][0-9]|[3][01])/([0]?[1-9]|[1][0-2])/([1][9][4-9][0-9]|[2][0][0-5][0-9])")
telPattern = re.compile("[679][0-9]{8}")
zipPattern = re.compile("[0][1-9][0-9]{3}|[1234][0-9]{4}|[5][012][0-9]{3}")
df = pd.read_csv('Sample test file - Sheet1.csv')

# LOG EMPTY ROWS EXCEPTION
logf = open("nanRows.log", "w")
for index in range(0, len(df.columns)):
	emptyList = list(df.iloc[index].isnull())
	if all(emptyList):
		logf.write("Failed to process, empty row : %i\n" % (index+1))
	checkRequiredFields(df.iloc[index], (index+1))

# DATES PROCESSING
print('Dates Processing')
i = 1
for d in df['Last Check-In Date']:
	if isinstance(d, str):
		if not datePattern.match(d):
			BadgerException('Exception: Wrong date format', i)
	else:
		BadgerException('Exception: NaN date', i)
	i += 1
print()

# PHONES PROCESSING
print('Phones Processing')
i = 1
for p in df['Phone']:
	if isinstance(p, str):
		p = p.replace(" ","")
		if not telPattern.match(p):
			BadgerException('Exception: Wrong phone format', i)
	else:
		BadgerException('Exception: NaN phone number', i)
	i += 1
print()

# ZIPS PROCESSING
print('Zips Processing')
i = 1
for z in df['Zip']:
	if isinstance(z, str):
		if not zipPattern.match(z):
			BadgerException('Exception: Wrong zip format', i)
	else:
		BadgerException('Exception: NaN zip number', i)
	i += 1
print()

# FORMAT DATES AS WISHED AND GET REQUIRED DATES
date_list = list(pd.to_datetime(df['Last Check-In Date'], format = '%d/%m/%Y'))
minDate =  min(date_list)
maxDate = max(date_list)
indexMinDate = date_list.index(minDate)
indexMaxDate = date_list.index(maxDate)
# GET REQUIRED COSTUMERS BY INDEX
minDateCostumer = df.iloc[indexMinDate]
print('Customer with most old last check-in date')
print(minDateCostumer)
print()
maxDateCostumer = df.iloc[indexMaxDate]
print('Customer with most recent last check-in date')
print(maxDateCostumer)
print()

# CREATE LIST FOR FULL NAMES AND SORT IT
namesList = []
for (n1, n2) in zip(df['First Name'].dropna(), df['Last Name'].dropna()):
	namesList.append(n1 + ' ' + n2)
	#namesList.append(n1.lower() + ' ' + n2.lower())
print('Alphabetically sorted name list')
print(sorted(namesList))
#print(quicksort(namesList))