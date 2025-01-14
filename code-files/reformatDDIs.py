import pandas as pd
import csv

df = pd.read_csv("druginfo.csv")

# get columns
ids = df["dg_id"]
ddi_ids = df["dg_interactions"].tolist()

# setup csv writing
field_names = ["drugbank_id", "interaction_id"]

drugs = []

last_id = ""

for index, id in enumerate(ids):
    
    # iterate through the interaction field and add each one to the list
    interactions = str(ddi_ids[index]).split(';')
    for inter in interactions:
        # dict structure to write to csv
        structure = {
            "drugbank_id": id,
            "interaction_id": inter
        }
        drugs.append(structure)

# write list of dicts to csv file
with open("finalDDIs.csv", "w") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(drugs)