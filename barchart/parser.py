'''
Created on Jul 28, 2014

@author: Michael
'''
import csv
import json
import random

class PqsModel():
    # Type    Cost/Liter    Capacity    Energy Cost    MaintCost
    def __init__(self, type, costPerLiter, capacity, totEnergy, totMaint):
        self.type = type
        self.costPerLiter = costPerLiter
        self.capacity = capacity
        self.totEnergy = totEnergy
        self.totMaint = totMaint


#create a dictionary from information in the district info file
def parseEnergyUseData():
    with open('static/barchart/EnergyUseData.csv', 'rb') as csvfile:
        datareader = csv.reader(csvfile)
        regions = dict()
        #DistrictName, Population, Births,BCG issued, OPV issued, Penta, Pneumo, Measles, YF, TT, Total Q, Total V, capReq
        #iterate through rows in the csv file, all but the first
        first = True
        for row in datareader:
            if first:
                first = False
                continue
            #record the district and region name
            region, district = row[0].split("_")
            capReq = float(row[12].strip(' ').replace(',', ''))
            capReq = int(round(capReq))
            births = int(row[2].strip(' ').replace(',', ''))
            cov = (round(100*random.uniform(0.6,1.0)))/100.0
            #csv file has multiple districts per region, so add to existing region entry if 
            #already seen
            if region in regions:
                regions[region]["children"].append({"name": district, "req": capReq, "births": births, "cov": cov})
            else:
                #we've not seen the region so start a json array for it
                #this is where data is probably being lost - first entry of every region is gone
                regions[region] = {"children": [{"name": district, "req": capReq, "births": births, "cov": cov}]}
    return regions

''' write data to a given file '''
def writeToFile(data, filename):
    with open(filename, 'wb') as writefile:
        writefile.write(data)
       
''' encode a json object using the given dictionary '''
def encodeDictToJSON(inDict):
    topChildren = []
    top = {"name": "Tanzania", "children": topChildren}

    for region, children in inDict.items():
        childDict = {"name": region, "children": children['children']}
        topChildren.append(childDict)

    result = json.dumps(top)
    print result
    return result

def parsePqs():
    with open('static/barchart/pqs.csv', 'rb') as csvfile:
        datareader = csv.reader(csvfile)
        #format: Type, Cost/Liter, Capacity, Energy Cost, MaintCost
        #for skipping first row
        first = True
        #create a new pqs object out of each row
        for row in datareader:
            print 'found row'

    
#use a capacity requirement to assign pqs models to 
def assignPqs(capReq, options):
    what = True
    chosen = []
    sortedOptionsByCap = quickSortByCap(options)

#sort options list by capacity using quick sort
def quickSortByCap(options):
    
    if (len(options) <= 1):
        return options
    else:
        pivot = random.choice(options)
        less = []
        greaterOrEqual = []
        for option in options:
            if option.capacity < pivot.capacity:
                less.append(option)
            else:
                greaterOrEqual.append(option)
        lessSorted = quickSortByCap(less)
        greatSorted = quickSortByCap(greaterOrEqual)
        sorted = lessSorted.extend(greatSorted)
        return sorted

''' parse energy use data, encode it to a json object, write to file ''' 
if __name__ == '__main__':
    regions = parseEnergyUseData()
    regions = encodeDictToJSON(regions)
    writeToFile(regions, 'static/barchart/quantity.json')

    