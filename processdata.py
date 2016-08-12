"""
processdata.py  Kiya Govek  2015 Jan
processes snmp information from snmpquery.py
gives information to tableview.py
"""

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
            if toner_percentage > 5:
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
    printer.setPaperTypes(paper_types)
    
# Convert codes used by printers to corresponding display icons
# No return, set paper level variable of printer object to list of html icon strings
def processPaperLevelInfo(printer, paper_level_info):
    paper_levels = []
    for tray in paper_level_info:
        # Tray is full
        if tray == -3 or tray == 500 or tray == 550:
            paper_levels.append('<i class="material-icons ready" style="font-size:12px">brightness_1</i>')
        # Tray is at half value
        elif tray == 275:
            paper_levels.append('<i class="material-icons half" style="font-size:12px">brightness_2</i>')
        # Tray is low
        elif tray == 50 or tray == 55:
            paper_levels.append('<i class="material-icons low" style="font-size:12px">brightness_3</i>')
        # Tray is empty
        elif tray == 0:
            paper_levels.append('<i class="material-icons empty" style="font-size:12px">panorama_fish_eye</i>')
        # Tray can't read paper level, probably not closed properly
        elif tray == -2:
            paper_levels.append('<span style="font-size:20px" class="unknown">? </span>')
        # Haven't encountered this number before
        else:
            paper_levels.append('<span class="unknown"> ??? </span>')
    printer.setPaperLevels(paper_levels)

# Checks for confusing messages such as hexadecimal 
def messageFormatting(message):
    if message[:2] == "0x":
        new_message = hexToEnglish(message) 
    else:
        new_message = message
    if new_message == ' mudd169-x4600.prin..':
        new_message = 'Printing'
    return new_message

# Converts a hexadecimal message to English          
def hexToEnglish(message):
    message_hex = message[2:].replace('a0','20')
    new_message = message_hex.decode("hex")
    return new_message
  
# Printer is disabled, so query printer for error reason and return reason          
def setDisabledDisplay(printer, status_info):
    printer.setStatus('Disabled')
    error_oid = status_info[1][:22] + '8' + status_info[1][23:]
    message_info = error_message(printer.getIP(),error_oid)
    #printer.setStatusIcon('<i class="material-icons" style="font-size:20px">error_outline</i>')
    return message_info
  
# Calls above methods to get displays to represent the data  
def setDisplays(printer, toner_info, paper_type_info, paper_level_info, status_info):
        printer.setStatusIcon('')
        
        processTonerInfo(printer, toner_info)
        
        processPaperTypeInfo(printer, paper_type_info)
        
        processPaperLevelInfo(printer, paper_level_info)
        
        printer.setStatus(status_info[0])
        
        if status_info[0] == 'Printing is disabled':
            message_info = setDisabledDisplay(printer, status_info)
        else:
            message_info = screen_message(printer.getIP())
        if message_info[0] == 'success':
            message = messageFormatting(message_info[1])
            printer.setMessage(message)
    
# Calls methods from snmpquery to get printer data, checks that data has arrived successfully
def queryPrinter(printer):
    paper_type_info = paper_type(printer.getIP())
    paper_level_info = paper_level(printer.getIP())
    toner_info = toner_level(printer.getIP())
    status_info = status(printer.getIP())
    
    if paper_type_info[0] == 'error' \
        or paper_level_info[0] == 'error' \
        or toner_info[0] == 'error' \
        or status_info[0] == 'error':
        
        printer.setStatus('Not Responding')
        #printer.setStatusIcon('<i class="material-icons" style="font-size:20px">error_outline</i>')
        
    else:
        setDisplays(printer, toner_info, paper_type_info, paper_level_info, status_info)
    

def queryAll():  
    for model in modelToPrinter:
        for printer in modelToPrinter[model]:
            try:
                queryPrinter(printer)
            except pysnmp.error.PySnmpError:
                printer.setStatus('Not Responding')
                #printer.setStatusIcon('<i class="material-icons" style="font-size:20px">error_outline</i>')
            
            
        