import pandas as pd
from datetime import date

date_list=pd.read_csv('date_list.csv')
dat={}
d = date_list['Date'].unique()
d.sort()
print(d)
j = 0
for i in d:
    dat[j] = i
    j += 1

print(dat)