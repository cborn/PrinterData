"""
printerclass.py  Kiya Govek  2016 Jan
creates and fills informational classes for individual printers and models
printerModel has basic information needed for snmp request
printerData will be filled by information from snmp query
"""
import csv

# Model class with tray number and toner name info for each model of printer
class printerModel():

    def __init__(self, model, tray_num, toner_num):
        self.model = model
        self.trayNum = tray_num
        self.tonerNum = toner_num
        self.tonerNames = []
    
    def getModel(self):
        return self.model
        
    def getTrayNum(self):
        return self.trayNum
    
    def getTonerNum(self):
        return self.tonerNum
        
    def getTonerNames(self):
        return self.tonerNames
        
    def setTrayNum(self, tray_num):
        self.trayNum = tray_num
        
    def setTonerNum(self, toner_num):
        self.tonerNum = toner_num
        
    def setTonerAll(self, toner_names):    
        self.tonerNames = toner_names

# Class to hold a single printer's data with get and set methods
# Model refers to an object of the printerModel class
class printerData():
    def __init__(self, name, IP, model):
        self.name = name
        self.IP = IP
        self.model = model
        self.paperTypes = []
        self.paperLevels = []
        self.toners = []
        self.status = "Ready"
        self.statusIcon = ""
        self.message = ""
        
    def getName(self):
        return self.name
        
    def getIP(self):
        return self.IP
        
    def getModel(self):
        return self.model
        
    def getPaperTypes(self):
        return self.paperTypes
        
    def getPaperLevels(self):
        return self.paperLevels
        
    def getToner(self):
        return self.toners
        
    def getStatus(self):
        return self.status
        
    def getStatusIcon(self):
        return self.statusIcon
        
    def getMessage(self):
        return self.message
        
    def getTrayNum(self):
        return len(self.paperLevels)
        
    def getTonerNum(self):
        return len(self.toners)
        
    def setPaperTypes(self, paper_types):
        self.paperTypes = paper_types
        
    def setPaperLevels(self, paper_levels):
        self.paperLevels = paper_levels
        
    def setToner(self, toners):
        self.toners = toners
        
    def setStatus(self, status):
        self.status = status
        
    def setStatusIcon(self, statusIcon):
        self.statusIcon = statusIcon
        
    def setMessage(self, message):
        self.message = message
        
        
modelsDict= {}
modelOrder = [] # for ordering purposes
csv_file = open("C:\\Program Files\\PrinterData\\printermodels.csv", 'r')
csv_reader = csv.reader(csv_file, delimiter=',')
for row in csv_reader:
    if len(row) > 2:
        name = row[0]
        tray_num = int(row[1])
        toner_num = int(row[2])
        if len(row) > 2+toner_num: # only read row if it has all information
            toners = row[3:3+toner_num]
            model = printerModel(name,tray_num,toner_num)
            model.setTonerAll(toners)
            modelsDict[name] = model
            modelOrder.append(name)
    
# create dictionary of next model to go to
modelOrderToDisplay = {}
for i in range(len(modelOrder)):
    if i == len(modelOrder) - 1:
        modelOrderToDisplay[modelOrder[i]] = modelOrder[0]
    else:
        modelOrderToDisplay[modelOrder[i]] = modelOrder[i+1]

csv_file.close()

modelToPrinter = {}

csv_file = open("C:\\Program Files\\PrinterData\\printers.csv", 'r')
csv_reader = csv.reader(csv_file, delimiter=',')
for row in csv_reader:
    if len(row) > 2:
        name = row[0]
        ip_address = row[1]
        model = row[2]
        if model in modelsDict:
            if model not in modelToPrinter:
                modelToPrinter[model] = []
            i = 0
            while i < len(modelToPrinter[model]) and modelToPrinter[model][i].getName() < name:
                i += 1
            modelToPrinter[model].insert(i,printerData(name,ip_address,modelsDict[model]))

