import pandas as pd
# read that csv
# get that date one by one in a loop/indexed
#normalize that format in which both can be compared
finalproduct = pd.read_csv(r"C:\Users\umar\Downloads\Work\New folder\finalproduct.csv",encoding='utf-8')
finalproduct['created_utc']   # format is YYYY-MM-DD
finalproduct=finalproduct.iloc[::-1]

import requests
from calendar import monthrange
import datetime
Month=input("Of which month are these csv files?")
now = datetime.datetime.now()
maxdays=monthrange(2020,int(Month))
print(maxdays[1])
url='http://api.nbp.pl/api/exchangerates/rates/a/usd/'+str(now.year)+"-"+str(Month)+"-01/"+str(now.year)+"-"+str(Month)+"-"+str(maxdays[1])+"/?format=json"
print(url)

r =requests.get(url).json()
r
dates=[]
exchangerate=[]
print(len(r['rates']))         #YYYY-MM-DD
for i in range(0,21):
    formatted_date=r['rates'][i]['effectiveDate']
    dates.append(str(r['rates'][i]['effectiveDate']))
    exchangerate.append(r['rates'][i]['mid'])
import pandas as pd
df_missing = pd.DataFrame({'dt': dates, 'ExchangeRate': exchangerate})
df_missing
finalproduct['created_utc'].iloc[0]
df_missing['dt'].iloc[0]
newdatelist=[]
newratelist=[]
for k in range(len(df_missing)):
    onedate=str(finalproduct['created_utc'].iloc[k])
    seconddate=str(df_missing['dt'].iloc[k])
    if(onedate==seconddate):
        print("same same "+onedate)
        newdatelist.append(onedate)
        newratelist.append(df_missing['ExchangeRate'].iloc[k])

    elif (onedate != seconddate):
        if onedate not in df_missing:
                print("not find in other frame "+onedate)
                newdatelist.append(onedate)
                newratelist.append(newratelist[-1])
        if onedate in seconddate:
            print("yes thats avaiable")
            newdatelist.append(onedate)
            newratelist.append()

for j in range(0, len(newdatelist)):
    print(newdatelist[j])

    print(newratelist[j])

# len(newratelist)
# len(newdatelist)
finalproduct
