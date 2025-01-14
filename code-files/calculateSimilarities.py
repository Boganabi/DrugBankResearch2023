import numpy as np
import pandas as pd
import csv

dfTTCE = pd.read_csv("../csv-files/uniqueTTCEs.csv")
dfDDI = pd.read_csv("../csv-files/uniqueDDIs.csv")

# to filter approved drugs
approvedRaw = pd.read_csv('../csv-files/drugbank05_drugs.csv')
approvedRaw = approvedRaw[approvedRaw["approved"] == 1] # drops values that dont have 1 for approved

dfTTCE = dfTTCE[dfTTCE["Drug ID"].isin(approvedRaw["drugbank_id"])]
dfDDI = dfDDI[dfDDI["drugbank_id"].isin(approvedRaw["drugbank_id"])]

# this program will calculate the inner product of all binary vectors in the TTCE csv file
writeablerows = [ [] ]

header = ["drug ID 1", "drug ID 2", "similarity"]
writeablerows.append(header)

# iterate through all rows in ddi csv file
ddi1 = dfDDI["drugbank_id"].tolist()
ddi2 = dfDDI["interaction_id"].tolist()

# list of all drugs in TTCEs
# converted to dict for faster lookup
# would use set but those dont preserve index
drugs = dict(enumerate(dfTTCE["Drug ID"]))

# also get inverted dict so we can do lookups
inv_drugs = dict(zip(drugs.values(), drugs.keys()))

# inv_drugs holds the index as value and drug id as key, this is our fast lookups

print("setup done, calculating...")

# zip allows me to iterate through both at the same time
for first, second in zip(ddi1, ddi2):
    try:
        # find index in dataset for drugs
        index1 = inv_drugs[first]
        index2 = inv_drugs[second]
    except KeyError:
        # not in TTCE file
        continue

    # get row with found indexes
    f = dfTTCE.iloc[index1][1:]
    s = dfTTCE.iloc[index2][1:]

    # calculate inner product
    prod = np.inner(f, s)

    # put values in list to add to csv
    result = [first, second, prod]
    writeablerows.append(result)

print("writing values...")

# write all values to csv file
with open("../csv-files/approvedInnerProducts.csv", "w", newline='', encoding="utf-8") as file:
    csvWriter = csv.writer(file, delimiter=',')
    csvWriter.writerows(writeablerows)