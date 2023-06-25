
"""
# if its this simple im gonna be sad for myself
import pandas as pd

# requires pip install lxml
df = pd.read_xml("fulldatabase.xml") # would work if pandas didnt have 1GB limiter

df.to_csv("data.csv")
"""


import xml.etree.ElementTree as ET
import pandas as pd

tree = ET.parse("fulldatabase.xml")
root = tree.getroot()

get_range = lambda col: range(len(col))
l = [{r[i].tag:r[i].text for i in get_range(r)} for r in root]

df = pd.DataFrame.from_dict(l)
df.to_csv('data.csv')