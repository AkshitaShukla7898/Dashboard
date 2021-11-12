import json
import pandas as pd

dfr=pd.read_csv('ward_61_data.csv')
dfd=dfr.copy()
#print(dfd)

reg=dfd['region'].unique()

data=[]

fields=['region','total waste','wet waste','dry waste']

for i in reg:
    l=[]
    l.append(i)
    for i in range(3):
        l.append(0)
    data.append(l)


for ind in dfd.index:
    for li in data:
        if li[0]==dfd['region'][ind]:
            li[1]+=dfd['total waste'][ind]
            li[2]+=dfd['wet waste'][ind]
            li[3]+=dfd['dry waste'][ind]
            break

dfm = pd.DataFrame(data, columns = fields)
print(dfm)


