"""
printerclass.py  Kiya Govek  2016 Jan
creates and fills informational classes for individual printers and models
printerModel has basic information needed for snmp request
printerData will be filled by information from snmp query
"""

# Model class with tray number and toner name info for each model of printer
class printerModel():

    def __init__(self, model, tray_num, toner_num):
        self.model = model
        self.trayNum = tray_num
        self.givesTypeInfo = True
        self.tonerNum = toner_num
        self.tonerNames = []
    
    def getModel(self):
        return self.model
        
    def getTrayNum(self):
        return self.trayNum
        
    def getGivesTypeInfo(self):
        return self.givesTypeInfo
    
    def getTonerNum(self):
        return self.tonerNum
        
    def getTonerNames(self):
        return self.tonerNames
        
    def setTrayNum(self, tray_num):
        self.trayNum = tray_num
        
    def setGivesTypeInfo(self, gives_type_info):
        self.givesTypeInfo = gives_type_info
        
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
        
        
# create model objects    
x4600 = printerModel('x4600',3,2)
x4600.setTonerAll(['Toner Cartridge','Drum Cartridge'])
x5550 = printerModel('x5550',5,3)
x5550.setTonerAll(['Toner Cartridge','Drum Cartridge','Maintenance Kit'])
x6360 = printerModel('x6360',3,7)
x6360.setTonerAll(['Cyan','Magenta','Yellow','Black','Imaging Unit','Fuser','Transfer Roller'])
cc5051 = printerModel('cc5051',5,5)
cc5051.setTonerAll(['Black','Cyan','Magenta','Yellow','Waste'])
cc5051.setGivesTypeInfo(False)

# create dictionary to hold which printers go with which models
modelToPrinter = {x4600:[], x5550:[], x6360:[], cc5051:[]}
# ordered list since dictionaries aren't ordered, to show how the tables should be arranged
modelOrderToDisplay = [x4600, x5550, x6360, cc5051]

# create printer objects to add to dictionary of printers
modelToPrinter[x4600].append(printerData('cass101','137.22.12.47',x4600))
modelToPrinter[x4600].append(printerData('mudd169','137.22.12.48',x4600))
modelToPrinter[x4600].append(printerData('will119','137.22.12.49',x4600))
modelToPrinter[x5550].append(printerData('ghue156','137.22.12.34',x5550))
modelToPrinter[x5550].append(printerData('ldc243','137.22.12.44',x5550))
modelToPrinter[x5550].append(printerData('libr451b','137.22.12.36',x5550))
modelToPrinter[x5550].append(printerData('libr451c','137.22.12.37',x5550))
modelToPrinter[x5550].append(printerData('libr451d','137.22.12.38',x5550))
modelToPrinter[x5550].append(printerData('libr451e','137.22.12.33',x5550))
modelToPrinter[x5550].append(printerData('sayl218a','137.22.12.55',x5550))
modelToPrinter[x5550].append(printerData('sayl218b','137.22.12.56',x5550))
modelToPrinter[x6360].append(printerData('wcc138','137.22.12.43',x6360))
modelToPrinter[cc5051].append(printerData('cmc104','137.22.12.40',cc5051))
modelToPrinter[cc5051].append(printerData('ldc220','137.22.12.39',cc5051))
modelToPrinter[cc5051].append(printerData('libr400','137.22.12.62',cc5051))
modelToPrinter[cc5051].append(printerData('wcc020','137.22.12.41',cc5051))