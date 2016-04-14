#!/usr/bin/env python

"""
tableview.py  Kiya Govek  Jan 2015
create html table for each printer model with snmp info for each printer
uses objects from printerclass.py to retrieve information

uses itty to create webpage
install itty by:
download zip from github
run python setup.py build
run sudo python setup.py install
"""

from processdata import *
from itty import *
import webbrowser

# output of this function is displayed at http://127.0.0.1:5000/printers/
@get("/printers/")
def printer_page(request):
    queryAll()
    html = '<!DOCTYPE html><html><head><meta http-equiv="refresh" content="90"><title>Printers- ITS Helpdesk</title>'
    html += '<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">'
    html += '<style>'
    html += '.ready {color: #006600;} .half {color: #336600;}.low {color: #995500;}\
    .empty {color: #CC0000;}.unknown {color: purple;}.error {color: blue;}'
    html += '.model {color: #505050;-ms-transform: rotate(270deg); \
    -moz-transform: rotate(270deg);-o-transform: rotate(270deg); \
    -webkit-transform: rotate(270deg);transform: rotate(270deg);width: 40px;} \
    .trayWidth {width: 78px;} .statusWidth {width: 130px;} .keyWidth {width: 100px;}</style>'
    html += '</head><body>'
    for model in modelOrderToDisplay:
        html += '<table border="1"><tr>'
        html += '<th rowspan="'+str(len(modelToPrinter[model])*2+1)+'"><p class="model">'+model.getModel()+'</p></th>'
        html += '<th class="trayWidth">Printer</th><th class="statusWidth">Status</th>'
        for tray in range(model.getTrayNum()):
            html += '<th class="trayWidth">Tray '+str(tray+1)+'</th>'
        for toner in model.getTonerNames():
            html += '<th class="trayWidth">'+toner+'</th>'
        html += '<th>On Screen / Errors</th>'
        
        #create row for each printer - each printer row is rowspan=2
        for printer in modelToPrinter[model]:
            html += '<tr><td>'+printer.getName()+'</td>'
            if printer.getStatus() != 'Not Responding':
                html += '<td>'+printer.getStatusIcon()+' '+printer.getStatus()+'</td>'
                for tray in range(printer.getTrayNum()):
                    html += '<td>'+ printer.getPaperLevels()[tray]
                    if model.givesTypeInfo:
                        html += printer.getPaperTypes()[tray] + '</td>'
                    else:
                        html += '</td>'
                html += '<td></td>'*(model.getTrayNum() - printer.getTrayNum())
                for toner in printer.getToner():
                    html += '<td>'+toner+'</td>'
                html += '<td >'+printer.getMessage()+'</td>'
                html += '</tr><tr>'
            else:
                colspan = str(model.getTrayNum() + model.getTonerNum())
                html += '<td  >'+printer.getStatusIcon()+' Not Responding</td>'
                html += '<td  colspan="'+colspan+'">Error - Printer is not responding</td>'
                html += '<td ></td>'
                html += '<tr></tr>'
            html += '</tr>'
        html += '</table>'
    html += '<table><tr><th colspan="5">Key</th></tr>'
    html += '<tr><td class="keyWidth"><i class="material-icons ready" style="font-size:12px">brightness_1</i> = Full</td>'
    html += '<td class="keyWidth"><i class="material-icons half" style="font-size:12px">brightness_2</i> = Half</td>'
    html += '<td class="keyWidth"><i class="material-icons low" style="font-size:12px">brightness_3</i> = Low</td>'
    html += '<td class="keyWidth"><i class="material-icons empty" style="font-size:12px">panorama_fish_eye</i> = Empty</td>'
    html += '<td class="keyWidth"><span style="font-size:20px" class="unknown">? </span> = Unknown</td>'
    html += '</tr></table>'
    html += '</body></html>'
    html = str(html)
    return html
    
    
if __name__ == "__main__":
    webbrowser.open('http://127.0.0.1:5000/printers',new=2)
    run_itty(port=5000)