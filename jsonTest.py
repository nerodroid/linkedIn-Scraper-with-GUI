import pandas as pd

select_country_list = pd.read_json("Countries.json")

cun = "Other"
for k in (select_country_list.values):
    if cun == k[0]:
        print (k[1])
