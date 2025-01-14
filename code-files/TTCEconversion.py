import pandas as pd
import csv

df = pd.read_csv("druginfo.csv") # get all drug ids to search for

# get targets, transporters, carriers, and enzymes
targets = pd.read_csv("drugbank_approved_target_polypeptide_ids.csv")
transporters = pd.read_csv("drugbank_approved_transporter_polypeptide_ids.csv")
carriers = pd.read_csv("drugbank_approved_carrier_polypeptide_ids.csv")
enzymes = pd.read_csv("drugbank_approved_enzyme_polypeptide_ids.csv")

# structure of the dictionary/2d array to write to csv
# NOTE: this is formatted to support the massive size of the rows.
# row format: drugID, targetID 1, ..., targetID 3277, transporterID 1, ..., transporterID 294, carrierID 1, ..., carrierID 105, enzymeID 1, ..., enzymeID 518
writeablerows = [ [] ]

# get all drug ids
drugIDs = df["dg_id"].tolist()

# get lists of all targets, transporters, carriers, and enzymes
ta = targets["ID"]
tr = transporters["ID"]
ca = carriers["ID"]
en = enzymes["ID"]

# columns containing the relating drug IDs
dta = targets["Drug IDs"]
dtr = transporters["Drug IDs"]
dca = carriers["Drug IDs"]
den = enzymes["Drug IDs"]

# create header
header = ["Drug ID"]
for h in ta:
    header.append(h)

for h in tr:
    header.append(h)

for h in ca:
    header.append(h)

for h in en:
    header.append(h)

# add header to array for csv file
writeablerows.append(header)

# iterate through all drug IDs
for i, drug in enumerate(drugIDs):

    # temp array to add after each iteration
    temparray = []

    temparray.append(drug)

    # add all targets this drug is found in
    for index, t in enumerate(ta):
        
        # i is drugID and index is the current target in the 2d array
        if drug in dta[index]:
            temparray.append(1)
        else:
            temparray.append(0)
    
    # add all transporters this drug is found in
    for index, t in enumerate(tr):

        # i is drugID and index is the current target in the 2d array
        if drug in dtr[index]:
            temparray.append(1)
        else:
            temparray.append(0)

    # add all carriers this drug is found in
    for index, c in enumerate(ca):

        # i is drugID and index is the current target in the 2d array
        if drug in dca[index]:
            temparray.append(1)
        else:
            temparray.append(0)

    # add all enzymes this drug is found in
    for index, e in enumerate(en):

        # i is drugID and index is the current target in the 2d array
        if drug in den[index]:
            temparray.append(1)
        else:
            temparray.append(0)
    
    writeablerows.append(temparray)

# write all values to csv file
with open("TTCEs.csv", "w+") as file:
    csvWriter = csv.writer(file, delimiter=',')
    csvWriter.writerows(writeablerows)