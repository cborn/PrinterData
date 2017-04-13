"""
processdata.py  Kiya Govek  2015 Jan
processes snmp information from snmpquery.py
gives information to tableview.py
"""
from __future__ import division
from snmpquery import *

# Determine how to display the level information for each toner
# No return, set toner variable of printer object to a list of display html strings
def processTonerInfo(printer, toner_info):
    model = printer.getModel()
    toner_levels = []
    for toner_index in range(model.getTonerNum()):
        # First half of toner_info is max value for each toner
        toner_max = float(toner_info[toner_index])
        # Second half of toner_info is actual value for each toner
        toner_actual = float(toner_info[toner_index+model.getTonerNum()])
        if toner_actual == -2:
            toner_levels.append('<span class="unknown"> Unknown </span>')
        elif toner_actual == -3:
            toner_levels.append('<span class="ready"> OK </span>')
        else:
            toner_percentage = int(round(toner_actual/toner_max * 100))
            if toner_percentage > 10:
                toner_levels.append('<i class="material-icons" style="font-size:12px">brightness_1</i> '+str(toner_percentage)+'%')
            # Toner is low, use different icon and color
            else:
                toner_levels.append('<i class="material-icons empty" style="font-size:12px">panorama_fish_eye</i> '+str(toner_percentage)+'%')
    printer.setToner(toner_levels)
    
# Create a convention between models for how to display paper type
# No return, set paper type variable of printer object to list of paper type strings
def processPaperTypeInfo(printer, paper_type_info):
    paper_types = []
    for tray in paper_type_info:
        tray = str(tray)
        if tray[:3] == 'na-' or tray[:3] == 'na_':
            paper_types.append(tray[3:].capitalize())
        elif tray[:3] == 'iso':
            paper_types.append(tray.upper())
        else:
            paper_types.append(tray.capitalize())
    if len(paper_types) > printer.model.getTrayNum():
        message = printer.getMessage() + " Extra trays:"
        for extra_type in paper_types[printer.model.getTrayNum():]:
            message = message+" "+extra_type
        printer.setMessage(message)
        paper_types = paper_types[:printer.model.getTrayNum()]
    printer.setPaperTypes(paper_types)
    
# Convert codes used by printers to corresponding display icons
# No return, set paper level variable of printer object to list of html icon strings
def processPaperLevelInfo(printer, paper_max_info, paper_level_info):
    paper_levels = []
    for index in range(0, len(paper_level_info)):
        tray = float(paper_level_info[index])
        max = float(paper_max_info[index])
        fraction = tray/max
        # tray is not closed properly, or levels unknown
        if tray == -2:
            paper_levels.append('<span style="font-size:20px" class="unknown">? </span>')
        # full
        elif tray == -3:
            paper_levels.append('<i class="material-icons ready" style="font-size:12px">brightness_1</i>')
        # full
        elif fraction > 0.99:
            paper_levels.append('<i class="material-icons ready" style="font-size:12px">brightness_1</i>')
        # half
        elif fraction <= 0.99 and fraction > 0.3:
            paper_levels.append('<i class="material-icons half" style="font-size:12px">brightness_2</i>')
        # low
        elif fraction <= 0.3 and fraction > 0:
            paper_levels.append('<i class="material-icons low" style="font-size:12px">brightness_3</i>')
        # empty
        elif fraction == 0:
            paper_levels.append('<i class="material-icons empty" style="font-size:12px">panorama_fish_eye</i>')
        # some other value
        else:
            paper_levels.append('<span class="unknown"> ??? </span>')
    if len(paper_levels)>printer.model.getTrayNum():
        paper_levels = paper_levels[:printer.model.getTrayNum()]
    printer.setPaperLevels(paper_levels)

# Checks for confusing messages such as hexadecimal 
def messageFormatting(message):
    if message[:2] == "0x":
        new_message = hexToEnglish(message) 
    else:
        new_message = message
    if new_message == ' mudd169-x4600.prin..':
        new_message = 'Printing'
    if new_message == 'Power Saver Mode active - Press OK button to return to Ready.':
        new_message = 'Power Save'
    return new_message

# Converts a hexadecimal message to English          
def hexToEnglish(message):
    message_hex = message[2:].replace('a0','20')
    #new_message = message_hex.decode("hex") # python 2.7
    new_message = bytes.fromhex(message_hex).decode('utf-8') # python 3.5
    return new_message
  
# Printer is disabled, so query printer for error reason and return reason          
def setDisabledDisplay(printer, status_info):
    printer.setStatus('Disabled')
    error_oid = status_info[1][:22] + '8' + status_info[1][23:]
    message_info = error_message(printer.getIP(),error_oid)
    #printer.setStatusIcon('<i class="material-icons" style="font-size:20px">error_outline</i>')
    return message_info
  
# Calls above methods to get displays to represent the data  
def setDisplays(printer, toner_info, paper_type_info, paper_max_info, paper_level_info, status_info):
        if status_info[0] == 'Printing is disabled':
            message_info = setDisabledDisplay(printer, status_info)
        else:
            message_info = screen_message(printer.getIP())
        if message_info[0] == 'success':
            message = messageFormatting(message_info[1])
            printer.setMessage(message)
            
        printer.setStatusIcon('')
        
        processTonerInfo(printer, toner_info)
        
        processPaperTypeInfo(printer, paper_type_info)
        
        processPaperLevelInfo(printer, paper_max_info, paper_level_info)
        
        printer.setStatus(status_info[0])
    
# Calls methods from snmpquery to get printer data, checks that data has arrived successfully
def queryPrinter(printer):
    paper_max_info = paper_max(printer.getIP())
    paper_type_info = paper_type(printer.getIP())
    paper_level_info = paper_level(printer.getIP())
    toner_info = toner_level(printer.getIP())
    status_info = status(printer.getIP())
    
    if paper_max_info[0] == 'error' \
        or paper_type_info[0] == 'error' \
        or paper_level_info[0] == 'error' \
        or toner_info[0] == 'error' \
        or status_info[0] == 'error':
        
        printer.setStatus('Not Responding')
        
    else:
        setDisplays(printer, toner_info, paper_type_info, paper_max_info, paper_level_info, status_info)
    

def queryAll():  
    for model in modelToPrinter:
        for printer in modelToPrinter[model]:
            try:
                queryPrinter(printer)
            except pysnmp.error.PySnmpError:
                printer.setStatus('Not Responding')
                #printer.setStatusIcon('<i class="material-icons" style="font-size:20px">error_outline</i>')
            
            
        