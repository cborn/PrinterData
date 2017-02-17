import csv

# ask for information on printer model
print ""
print "Hello! You are now adding a printer model to the printer table."
print "After doing this you will be able to add printers to that printer model."
print "Please input information about the printer model:"
print ""
info = []
name = raw_input("What is the printer model name without spaces (ex. Canon5051, Xerox4600): ").strip()
info.append(name)
tray_num = int(raw_input("How many paper trays does it have? ").strip())
info.append(tray_num)
toner_num = int(raw_input("How many toners does it have? ").strip())
info.append(toner_num)
print ""
print "Input the names of the toners (ex. Black, Magenta, Transfer Roller): "
for index in range(toner_num):
	this_toner = raw_input("What is the name for toner "+str(index+1)+"? ").strip()
	info.append(this_toner)
gives_types = raw_input("Does this printer give information on the paper types in its trays? If you don't know, reply n. (y/n) ").strip()
info.append(gives_types)

# write printer model data to CSV file
csv_file = open("printermodels.csv", 'a')
csv_writer = csv.writer(csv_file, delimiter=',')
csv_writer.writerow(info)
csv_file.close()

