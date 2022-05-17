import pandas as pd
import re
from datetime import datetime

class BadgerException(Exception):
    def __init__(self, message, row):
        print('Error: ' + message + 'at row ', row)

datePattern = re.compile("([0]?[1-9]|[12][0-9]|[3][01])/([0]?[1-9]|[1][0-2])/([1][9][4-9][0-9]|[2][0][0-5][0-9])")
telPattern = re.compile("[679][0-9]{8}")
zipPattern = re.compile("[0][1-9][0-9]{3}|[1234][0-9]{4}|[5][012][0-9]{3}")
df = pd.read_csv('Sample test file - Sheet1.csv')

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
print('Zips Processing')
i = 1
for z in df['Zip']:
	if isinstance(z, str):
		#p = p.replace(" ","")
		#print(p)
		if not zipPattern.match(z):
			BadgerException('Exception: Wrong zip format', i)
	else:
		BadgerException('Exception: NaN zip number', i)
	i += 1

print()
date_list = pd.to_datetime(df['Last Check-In Date'], format = '%d/%m/%Y')
#print(date_list) 

for d in date_list:
	print(type(d))

print(date_list.min())
print(date_list.max())
