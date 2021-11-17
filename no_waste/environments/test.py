import json
import pandas as pd

ward_61 = json.load(open('ward61.geojson', 'r'))

def create_csv(ward_61):
    l = []

    for i in ward_61['features']:
        l.append(i['properties'])

    #fields = list(ward_61['features'][0]['properties'].keys()) //columns in geojson properties

    df = pd.DataFrame(l)
    return df


df=create_csv(ward_61)
print(df)

