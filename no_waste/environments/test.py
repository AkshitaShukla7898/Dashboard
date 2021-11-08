import json
import csv
import pandas as pd
import plotly.graph_objects as go

import plotly.io as pio


ward_61= json.load(open('ward_61.json','r'))

l=[]

print(ward_61['features'][0]['properties'])

i=0
for feature in ward_61['features']:
    if feature['properties']['name'] is None:
        feature['properties']['name']='random_'+str(i)
        i+=1
    l.append(feature['properties']['name'])
fields = ['name']
row=[]
for i in l:
    row.append([i])

filename = "dummy_w.csv"

# writing to csv file
with open(filename, 'w') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(fields)

    # writing the data rows
    csvwriter.writerows(row)






