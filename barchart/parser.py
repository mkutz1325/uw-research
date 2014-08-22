'''
Created on Jul 28, 2014

@author: Michael
'''
''' basic information about refrigerator models for vis '''

import csv
import json
import random
import sys

class PqsModel():
    # Type    Cost/Liter    Capacity    Energy Cost    MaintCost
    def __init__(self, pqsType, costPerLiter, capacity, totEnergy, totMaint):
        self.pqsType = pqsType
        self.costPerLiter = costPerLiter
        self.capacity = capacity
        self.totEnergy = totEnergy
        self.totMaint = totMaint
        
    def __str__(self):
        return self.pqsType
    def __repr__(self):
        return self.pqsType
    
allPqsModels = []

''' create a dictionary from information in the district info file.
    looks through district csv for annual births, vaccine volume, district
    cold chain capacity requirements. Assigns pqs models based on capacity
    requirements and a local algorithm, and calculates cost statistics
    using total cost of ownership data from PATH'''
def parseEnergyUseData():
    with open('static/barchart/DistrictInfo.csv', 'rb') as csvfile:
        datareader = csv.reader(csvfile)
        regions = dict()
        #DistrictName, Population, Births,BCG issued, OPV issued, Penta, Pneumo, Measles, YF, TT, Total Q, Total V, capReq
        #iterate through rows in the csv file, all but the first
        first = True
        #save national info for django model
        nationBirths = 0
        nationReq = 0.0
        nationVol = 0.0
        nationCost = 0.0
        nationEnergy = 0.0
        nationMaint = 0.0
        for row in datareader:
            if first:
                first = False
                continue
            #record the district and region name
            region, district = row[0].split("_")
            totVol = float(row[11].strip(' ').replace(',', ''))
            totVol = int(round(totVol))
            capReq = float(row[12].strip(' ').replace(',', ''))
            capReq = int(round(capReq))
            # assign pqs models to the district
            # TODO bad code structure to only allow parser.py access district info
            districtPqsModels = assignPqs(capReq, allPqsModels)
            totCost, totEnergy, totMaint = calcStatsOfSelection(districtPqsModels)
            births = int(row[2].strip(' ').replace(',', ''))
            #add to nation totals
            nationCost += totCost
            nationEnergy += totEnergy
            nationMaint += totMaint
            nationReq += capReq
            nationVol += totVol
            #add to district dictionary
            #csv file has multiple districts per region, so add to existing region entry if 
            #already seen
            if region in regions:
                regions[region]["children"].append({"name": district, "req": capReq, 
                        "births": births, "cost": totCost, 
                        "energy": totEnergy, "maint": totMaint,
                        "volume": totVol})
            else:
                #we've not seen the region so start a json array for it
                #this is where data is probably being lost - first entry of every region is gone
                regions[region] = {"children": [{"name": district, "req": capReq, 
                        "births": births, "cost": totCost, 
                        "energy": totEnergy, "maint": totMaint,
                        "volume": totVol}]}
    print nationCost, " ", nationEnergy, " ", nationMaint
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

''' parse the pqs csv file and return a list of models.
    pqs csv file contains cost information from PATH total
    cost of ownership model.''' 
def parsePqs():
    models = []
    with open('static/barchart/pqs.csv', 'rb') as csvfile:
        datareader = csv.reader(csvfile)
        #format: Type, Cost/Liter, Capacity, Energy Cost, MaintCost
        #for skipping first row
        first = True
        #create a new pqs object out of each row
        for row in datareader:
            if first:
                first = False
                continue
            pqsType, cpl, cap, en, mnt = row
            pqsType = str(pqsType)
            # round dollar values
            cpl = round(float(cpl)*100.0)/100.0
            en = round(float(en)*100.0)/100.0
            mnt = round(float(mnt)*100.0)/100.0
            cap = float(cap)
            model = PqsModel(pqsType, cpl, cap, en, mnt)
            models.append(model)
    return models
    
''' use a capacity requirement to assign pqs models to a district.
   assign a potentially inefficient set of models using a greedy
   algorithm to simply meet the requirement'''
def assignPqs(capReq, models):
    #keep track of which models are chosen
    chosen = []
    #sort by capacity for greedy selection algorithm
    #goal is not to choose most efficient options; want 
    #a sub-optimal selection to make visualization more interesting
    models.sort(key=lambda x: x.capacity)
    filled = 0
    #while the requirement not filled (will not run more than twice
    #given the current data)
    while filled < capReq:
        for i in range(0, len(models)):
            model = models[i]
            #if this model fills capacity requirement
            if model.capacity >= (capReq - filled):
                chosen.append(model)
                filled += model.capacity
                #don't check any more models
                break
            #if this is the last option, and cap req not filled
            if i == len(models) - 1:
                #add it to options
                chosen.append(model)
                #record how much has been filled, and go through
                #loop of model choice again
                filled += model.capacity
    return chosen

''' return some cost statistics of a given selection of pqs models.
    includes total annuallized cost of ownership, total annual energy cost,
    and total annual maintenance cost (reg maintenance + major repairs)'''
def calcStatsOfSelection(selections):
    totCost = 0
    totEnergy = 0
    totMaint = 0
    for selection in selections:
        totCost += (selection.costPerLiter*selection.capacity)
        totEnergy += selection.totEnergy
        totMaint += selection.totMaint
    return totCost, totEnergy, totMaint

''' parse energy use data, encode it to a json object, write to json file
    for visualization to use later. ''' 
if __name__ == '__main__':
    #store models in class variable
    allPqsModels = parsePqs()
    regions = parseEnergyUseData()
    regions = encodeDictToJSON(regions)
    writeToFile(regions, 'static/barchart/quantity.json')

#     selections = assignPqs(232, models)
#     print selections
#     totCost, totEnergy, totMaint = calcStatsOfSelection(selections)
#     print totEnergy, " dollars spent on energy"
#     print totMaint, " dollars spent on maintenance"
#     print totCost, "dollars spent"

    