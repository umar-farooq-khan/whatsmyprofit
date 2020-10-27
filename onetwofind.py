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
import pandas as pd

#Month=input("Of which month are these csv files?")
Month="04"
now = datetime.datetime.now()
maxdays=monthrange(2020,int(Month))
print(maxdays[1])
url='http://api.nbp.pl/api/exchangerates/rates/a/usd/'+str(now.year)+"-"+str(Month)+"-01/"+str(now.year)+"-"+str(Month)+"-"+str(maxdays[1])+"/?format=json"
print(url)

r =requests.get(url).json()

dates=[]
exchangerate=[]
print(len(r['rates']))         #YYYY-MM-DD
for i in range(0,len(r['rates'])):
    dates.append(str(r['rates'][i]['effectiveDate']))
    exchangerate.append(r['rates'][i]['mid'])
df_missing = pd.DataFrame({'dt': dates, 'ExchangeRate': exchangerate})


newdatelist=[]
newratelist=[]

for k in range(0,len(finalproduct)):
    onedate=str(finalproduct['created_utc'].iloc[k])
    # creating and passsing series to new column
    xx=df_missing.loc[df_missing['dt'] == onedate]
    if(xx.empty==False):
        x=xx['ExchangeRate'].values.min()
        print(x)
        print("that rate"+str(xx['ExchangeRate'].values.min()))
        print("that date"+str(onedate))
        newratelist.append(str(xx['ExchangeRate'].values.min()))
        newdatelist.append(onedate)
    if(xx.empty==True):
        print("that date not found" + str(onedate))
        newdatelist.append(onedate)
        newratelist.append(newratelist[-1])
    print("xxxxxxxxxxxxxx")







for j in range(0, len(newdatelist)):
    print(newdatelist[j])

    print(newratelist[j])

newratelist=newratelist[::-1]
newdatelist=newdatelist[::-1]
df_accurateexchangerate = pd.DataFrame({'dt': newdatelist, 'ExchangeRate': newratelist})
print(df_accurateexchangerate)
finalproduct = pd.read_csv(r"C:\Users\umar\Downloads\Work\New folder\finalproduct.csv",encoding='utf-8')
finalizeddataframe=pd.concat([finalproduct,df_accurateexchangerate],axis=1,ignore_index=False)

def multiplyit(row):
    print("ex"+str(row['ExchangeRate']))
    print("dat"+str(row['PayP+Stripe']))
    in_pln= float(row['ExchangeRate']*float(row['PayP+Stripe']))
    return in_pln


finalizeddataframe['PLN']= finalizeddataframe.apply(lambda row: multiplyit(row), axis=1)


