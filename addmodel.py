import csv

# ask for information on printer model
print("")
print("Hello! You are now adding a printer model to the printer table.")
print("After doing this you will be able to add printers to that printer model.")
print("Please input information about the printer model:")
print("")
info = []
name = input("What is the printer model name without spaces (ex. Canon5051, Xerox4600): ").strip()
info.append(name)
tray_num = int(input("How many paper trays does it have? ").strip())
info.append(tray_num)
toner_num = int(input("How many toners does it have? ").strip())
info.append(toner_num)
print("")
print("Input the names of the toners (ex. Black, Magenta, Transfer Roller). If the name is long, please abbreviate it: ")
for index in range(toner_num):
	this_toner = input("What is the name for toner "+str(index+1)+"? ").strip()
	info.append(this_toner)

# write printer model data to CSV file
csv_file = open("printermodels.csv", 'a')
csv_writer = csv.writer(csv_file, delimiter=',')
csv_writer.writerow(info)
csv_file.close()

