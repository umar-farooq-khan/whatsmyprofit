import requests
from calendar import monthrange
from datetime import datetime, timedelta
import pandas as pd
date_today = datetime.now()

Month=input("Of which month are these csv files?")
now = datetime.datetime.now()
maxdays=monthrange(2020,int(Month))
print(maxdays[1])
url='http://api.nbp.pl/api/exchangerates/rates/a/usd/'+str(now)+"-"+str(Month)+"-01/"+str(now.year)+"-"+str(Month)+"-"+str(maxdays[1])+"/?format=json"
print(url)

r =requests.get(url).json()
r
dates=[]
exchangerate=[]
print(len(r['rates']))
for i in range(0,21):
    dates.append(str(r['rates'][i]['effectiveDate']))
    exchangerate.append(r['rates'][i]['mid'])
import pandas as pd
df_missing = pd.DataFrame({'dt': dates, 'ExchangeRate': exchangerate})
