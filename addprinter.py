import csv

# ask for information on printer model
print ""
print "Hello! You are now adding a printer to the printer table."
print "Please select the correct printer model for the printer,"
print "or create one using addmodel.py before adding this printer."
print ""
info = []
name = raw_input("What is the printer room number without spaces (ex. ldc245, libr451c): ").strip()
info.append(name)
ipAddress = raw_input("What is the IP address of this printer (ex. 137.22.12.47): ").strip()
info.append(ipAddress)
modelOptions = []
print "The models you can choose from are:"
csv_file = open("printermodels.csv", 'r')
csv_reader = csv.reader(csv_file, delimiter=',')
for row in csv_reader:
    print row[0]
    modelOptions.append(row[0])
model = raw_input("Which model is this printer? Please type it exactly has seen above: ").strip()
if model not in modelOptions:
    print "That is not a valid model. Please try again. If it was not in the list above, please run addmodel.py first."
else:
    info.append(model)
    # write printer model data to CSV file
    csv_file = open("printers.csv", 'a')
    csv_writer = csv.writer(csv_file, delimiter=',')
    csv_writer.writerow(info)
    csv_file.close()
