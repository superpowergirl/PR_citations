import requests
import json
import pandas as pd
#http://api.nobelprize.org/2.0/nobelPrize/phy/1901
year_list = []
nobel_lau_list=[]
for y in range(1990, 2010, 1):
    response = requests.get("http://api.nobelprize.org/2.0/nobelPrize/phy/"+ str(y))
    r = json.loads(response.text)

    ###original code
    # year_list.append(y)
    # for i in r:
    #     if 'laureates' in i:
    #         nobel_lau_list.append([x['knownName']['en'] for x in i['laureates']])
    #     else:
    #         year_list.remove(y)

    ###new code
    for i in r:
        if 'laureates' in i:
            for x in i['laureates']:
                nobel_lau_list.append(x['knownName']['en'])
                year_list.append(y)

d = {'year':year_list, 'nobel_laureates':nobel_lau_list}
df_nobel = pd.DataFrame(d)