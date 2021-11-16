import datetime
import pandas as pd

df=pd.read_csv('ward_61_data_1.csv')

print(datetime.date(2021,2,2))

dl=df['coll_date'].unique()
dl=pd.to_datetime(dl)
print(dl)
print(dl.max())
print(type(df['coll_date'][0]))