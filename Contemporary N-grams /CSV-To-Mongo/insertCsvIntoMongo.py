import pymongo
import csv
import json
import sys

csvFilePath = 'all-the-news/articles1.csv'
jsonFilePath = 'tempNewsJson.json'

csv.field_size_limit(sys.maxsize)   # This is required to increase csv reader's limit

arr = []
with open(csvFilePath) as csvFile:
    csvReader = csv.DictReader(csvFile)
    #print csvReader
    for csvRow in csvReader:
        arr.append(csvRow)
    #print arr

# Creating a new JSON file

with open(jsonFilePath, 'a+') as jsonFile:
    jsonFile.write(json.dumps(arr, indent = 4))

client = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = client['newsTemp']
mycol = mydb['articles']

x = mycol.insert_many(arr)