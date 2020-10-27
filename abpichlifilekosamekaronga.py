import pandas as pd

import requests
from calendar import monthrange
import datetime

import pandas as pd
from bdateutil import isbday
from datetime import date

pathh=input("Enter Path of the files:  " )
pathh=r"E:\fiverr\poland\may\stripe.csv"

df = pd.read_csv(pathh,encoding='utf-8', decimal=",", thousands=" ")
#date=date.dropna()
#paypaldf.to_csv(pathh+"\date.csv", encoding="utf-8")


#C=C.str.replace(",",".")
#
#C=C.str.replace("\s","")
df['amount']=df['amount'].astype(float)

print(df)


Month=input("Of which month are these csv files?")
#Month="6"
Month="0"+str(Month)
now = datetime.datetime.now()

maxdays=monthrange(2020,int(Month))
print(maxdays[1])
pichlamonth= int(Month)-1
pichlamonth="0"+str(pichlamonth)

pichlamonthmaxdays=monthrange(2020,int(pichlamonth))
#pichlamonthmaxdays=pichlamonthmaxdays.split(",")
pichlamonthmaxdays[1]
isbusdaybool= False
type(isbusdaybool)
isbusdaybool

finditday=str(pichlamonthmaxdays[1])
while (isbusdaybool ==False):
    print("in while loop")
    datetocheck = "2020-" + pichlamonth + "-" + str(finditday)
    print("datetocheck" + str(datetocheck))
    isbusdaybool = isbday(datetocheck)

    print("isbool= " + str(isbusdaybool))
    if (isbusdaybool ==True):
        print("true agya")
        break
    finditday = str(int(finditday) - 1)


url='http://api.nbp.pl/api/exchangerates/rates/a/usd/'+str(now.year)+"-"+str(pichlamonth)+"-"+str(finditday)+"/"+str(now.year)+"-"+str(Month)+"-"+str(int(maxdays[1])-1)+"/?format=json"
print(url)
r =requests.get(url).json()
print(r)
i=0
dates=[]
exchangerate=[]
#YYYY-MM-DD
str(r['rates'][0]['effectiveDate'])
for i in range(0,len(r['rates'])):
    dates.append(str(r['rates'][i]['effectiveDate']))
    exchangerate.append(r['rates'][i]['mid'])
df_missing = pd.DataFrame({'dt': dates, 'ExchangeRate': exchangerate})
print("df missing")
print(df_missing)


