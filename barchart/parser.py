'''
Created on Jul 28, 2014

@author: Michael
'''
import csv
import json

def parseDummyData():
    with open('static/barchart/dummyData.csv', 'rb') as csvfile:
        datareader = csv.reader(csvfile)
        i = 0
        regions = dict()
        for row in datareader:
            if i>5: 
                region, district = row[0].split("_")
                q = '0' if row[14].strip(' ')=='-' else row[14].strip(' ')
                if region in regions:
                    regions[region]["children"].append({"name": district, "size": int(q.replace(',', ''))})
                else:
                    regions[region] = {"children": []}
            i += 1
    return regions

def writeToFile(data, filename):
    with open(filename, 'wb') as writefile:
        writefile.write(data)
       
def encodeDictToJSON(dict):
    topChildren = []
    top = {"name": "Tanzania", "children": topChildren}

    for region, children in dict.items():
        childDict = {"name": region, "children": children['children']}
        topChildren.append(childDict)

    result = json.dumps(top)
    print result
    return result
         
def parseDummyLine(row):
    region, district = row.split("_")
    return region, district

if __name__ == '__main__':
    regions = parseDummyData()
    regions = encodeDictToJSON(regions)
    writeToFile(regions, 'static/barchart/quantity.json')

    