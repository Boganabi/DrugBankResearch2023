import pandas as pd

file = "finalDDIs.csv"
output = "uniqueDDIs.csv"

df = pd.read_csv(file, sep=",")

df.drop_duplicates(subset=None, inplace=True)

df.to_csv(output, index=False)