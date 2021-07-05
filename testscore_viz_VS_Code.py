# -*- coding: utf-8 -*-
"""
IPYNB file is located at
    https://colab.research.google.com/drive/1IMo-3Xp7vRCwMgmq0tg3d2GwQBTlZPQM
"""

#%%
import altair as alt
import pandas as pd
import requests
import codecs
from requests.exceptions import HTTPError
import openpyxl

#Add export?format=xlsx after id
url = "https://docs.google.com/spreadsheets/d/1pUDOO5rROKI20sP5p5_2gVCMvsOoBoFzYUNtz2fZYqA/export?format=xlsx"

try:
  #Send get request
  response = requests.get(url)
  # If the response was successful, no Exception will be raised
  response.raise_for_status()
except HTTPError as http_err:
  print(f'HTTP error occurred: {http_err}')
except Exception as err:
  print(f'Other error occurred: {err}')
else:
  print('Request successfully!')

excelFileName = "excel.xlsx"

writeSuccessful = True
try:
  with codecs.open(excelFileName, 'wb') as f:
    f.write(response.content)
except Exception as err:
  print(f"Error occured when writing file: {err}")
  writeSuccessful = False
else:
  print("Excel file written successfully")

#Get the sheet names in excel. 
sheetNames = openpyxl.load_workbook(excelFileName, read_only=True).sheetnames
sheetNamesDict = {s:'' for s in sheetNames}
print(f"sheetNamesDict = {sheetNamesDict}")

#Altair does not work with russian characters. Define sheet names in english
sheetNamesDict = {'ИТБ': 'ITMB', 'ФЭТ': 'FET', 'ФМ': 'FM'}

if writeSuccessful:
  dataSource = excelFileName
else:
  dataSource = response.content

#Read pandas dataframes from Excel file that was saved
dfs = []
for sheetNameRu in sheetNamesDict:
  df = pd.read_excel(dataSource, header=1, sheet_name=sheetNameRu)
  sheetNameEn = sheetNamesDict[sheetNameRu]
  df['program'] = sheetNameEn
  dfs.append(df)

#Concatenate the dataframes from all sheets
df = pd.concat(dfs, ignore_index=True)

#Drop the columns which have all nan values
df = df.dropna(axis='columns', how = 'all')

columnNamesDict = {col : '' for col in list(df.columns)} 
print(f"columnNamesDict = {columnNamesDict}")

#Remove the columns that you don't need and provide the english translation for the columns left
#columnNamesDict = {'№': '', 'ФИО': '', 'сумма баллов': '', 'Мат.': '', 'Русс.': '', 'ИКТ': '', 'Бюджет/договор': '', 'Program': '', 'Ин.яз': ''}
columnNamesDict = {'ФИО': 'name', 'сумма баллов': 'total_score', 'Мат.': 'math', 'Русс.': 'russian', 'ИКТ': 'it', 'program': 'program', 'Ин.яз': 'foreign_language'}

#Filter only the needed columns
df = df[columnNamesDict.keys()]

#Replace the russian column names with the english stored in the dictionary
columnNamesEn = [columnNamesDict[col_ru] for col_ru in df.columns]
df.columns = columnNamesEn


#%%

alt.Chart(df).mark_circle(size=100).encode(
    x='math',
    y='russian',
    color='program',
    tooltip=['name', 'total_score']
).interactive()