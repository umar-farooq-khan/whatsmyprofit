import pandas as pd

import requests
from calendar import monthrange
import datetime

import pandas as pd
from bdateutil import isbday
from datetime import date


import requests
import datetime
from calendar import monthrange
#pathh=input("Enter Path of the files:  " )

pathh=r"E:\fiverr\poland\may\stripe.csv"
df = pd.read_csv(pathh,encoding='utf-8', decimal="," ,thousands=' ')
dfamount=df['amount'].astype(float)
print("full df")
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

def multiplybyexchangerate(row):

    print("row before"+str(row['amount']))
    rate=r['rates'][i]['mid']
    row['amount']=float(row['amount'])*rate
    return row



#df= df.apply(lambda row: multiplybyexchangerate(row), axis=1)


newdatelist=[]
newratelist=[]
# appended=pd.concat([df,df_missing] , axis=1,ignore_index=False)
# print("appended")
# print(appended)

for k in range(0,len(df_missing)):
    if(k==0):
        newratelist.append(float(df_missing['ExchangeRate'].iloc[0]))
        newdatelist.append(df_missing['dt'].iloc[0])
        print(newdatelist)
        print(newratelist)
    if(k==len(df_missing)):
        print("dont add anything")
    onedate=str(df['date'].iloc[k])
    print("tofinddate"+onedate)
    # creating and passsing series to new column
    xx=df_missing.loc[df_missing['dt'] == onedate]
    if(xx.empty==False):
        print("not found")
        print("rate going to append"+str(xx['ExchangeRate'].values.min()))
        print("date going to append"+str(onedate))
        newratelist.append(float(xx['ExchangeRate'].values.min()))
        newdatelist.append(onedate)
    if(xx.empty==True):
        print("this date not found" + str(onedate))
        print("date going to append:"+onedate)
        print("rate going to append: pichla wala"+str(newratelist[-1]))
        newdatelist.append(onedate)
        newratelist.append(float(newratelist[-1]))

print("date rate list")
print(newdatelist)
print(newratelist)

# for j in range(0, len(newdatelist)):
#     print(newdatelist[j])
#
#     print(newratelist[j])

newratelist=newratelist[::-1]
newdatelist=newdatelist[::-1]
df_accurateexchangerate = pd.DataFrame({'dt': newdatelist, 'ExchangeRate': newratelist})
print(df_accurateexchangerate)





#
#
# dates=[]
# exchangerate=[]
# appended.to_csv(pathh+r"\Netprofit.csv")
#
# import os
# os.remove(pathh+r"\temp_totalprofit_paypal.csv")
# os.remove(pathh+r"\temp_totalprofit_stripe.csv")
# try:
#     nownewdf = pd.read_csv(pathh+r"\Netprofit.csv",usecols=['created_utc','net','totalprofitpaypal','PayP+Stripe'],encoding='utf-8')
# except ValueError:
#     nownewdf = pd.read_csv(pathh + r"\Netprofit.csv", usecols=['created', 'net', 'totalprofitpaypal', 'PayP+Stripe'], encoding='utf-8')
#
# nownewdf.to_csv(pathh+r"\finalproduct.csv")
# os.remove(pathh+r"\Netprofit.csv")
# #normalize that format in which both can be compared
# finalproduct = pd.read_csv(pathh+r"\finalproduct.csv",encoding='utf-8')
# finalproduct=finalproduct.iloc[::-1]
#
#
# Month=input("Of which month are these csv files?")
# #Month="6"
# Month="0"+str(Month)
# now = datetime.datetime.now()
#
# maxdays=monthrange(2020,int(Month))
# print(maxdays[1])
# pichlamonth= int(Month)-1
# pichlamonth="0"+str(pichlamonth)
#
# pichlamonthmaxdays=monthrange(2020,int(pichlamonth))
# #pichlamonthmaxdays=pichlamonthmaxdays.split(",")
# pichlamonthmaxdays[1]
# isbusdaybool= False
# type(isbusdaybool)
# isbusdaybool
#
# finditday=str(pichlamonthmaxdays[1])
# while (isbusdaybool ==False):
#     print("in while loop")
#     datetocheck = "2020-" + pichlamonth + "-" + str(finditday)
#     print("datetocheck" + str(datetocheck))
#     isbusdaybool = isbday(datetocheck)
#
#     print("isbool= " + str(isbusdaybool))
#     if (isbusdaybool ==True):
#         print("true agya")
#         break
#     finditday = str(int(finditday) - 1)
#
#
#
#
#
#
# #previouslastdate= monthrange(2020,int(pichlamonth))
# url='http://api.nbp.pl/api/exchangerates/rates/a/usd/'+str(now.year)+"-"+str(pichlamonth)+"-"+str(finditday)+"/"+str(now.year)+"-"+str(Month)+"-"+str(int(maxdays[1])-1)+"/?format=json"
# print(url)
#
# r =requests.get(url).json()
# print(r)
# dates=[]
# exchangerate=[]
# print(len(r['rates']))
# r['rates'][0]['mid']
# #YYYY-MM-DD
# str(r['rates'][0]['effectiveDate'])
# for i in range(0,len(r['rates'])):
#     dates.append(str(r['rates'][i]['effectiveDate']))
#     exchangerate.append(r['rates'][i]['mid'])
# df_missing = pd.DataFrame({'dt': dates, 'ExchangeRate': exchangerate})
#
# df_missing
# newdatelist=[]
# newratelist=[]
#
#
#
#
#
#
# for k in range(0,len(finalproduct)):
#     if(k==0):
#         newratelist.append(float(df_missing['ExchangeRate'].iloc[0]))
#         newdatelist.append(df_missing['dt'].iloc[0])
#         print(newdatelist)
#         print(newratelist)
#     if(k==len(finalproduct)):
#         print("dont add anything")
#     onedate=str(finalproduct['created_utc'].iloc[k])
#
#     #print("tofinddate"+onedate)
#     # creating and passsing series to new column
#     xx=df_missing.loc[df_missing['dt'] == onedate]
#     if(xx.empty==False):
#         #print("not found")
#         #print("rate going to append"+str(xx['ExchangeRate'].values.min()))
#         #print("date going to append"+str(onedate))
#         newratelist.append(float(xx['ExchangeRate'].values.min()))
#         newdatelist.append(onedate)
#     if(xx.empty==True):
#         #print("this date not found" + str(onedate))
#         #print("date going to append:"+onedate)
#         #print("rate going to append: pichla wala"+str(newratelist[-1]))
#
#         newdatelist.append(onedate)
#         newratelist.append(float(newratelist[-1]))
#     #print("xxxxxxxxxxxxxx")
#
#
# newdatelist.pop()
# newratelist.pop()
# len(newratelist)
# newratelist
# newdatelist
#
#
#
#
#
# # for j in range(0, len(newdatelist)):
# #     print(newdatelist[j])
# #
# #     print(newratelist[j])
#
# newratelist=newratelist[::-1]
# newdatelist=newdatelist[::-1]
# df_accurateexchangerate = pd.DataFrame({'dt': newdatelist, 'ExchangeRate': newratelist})
# df_accurateexchangerate
#
# finalproduct = pd.read_csv(pathh+r"\finalproduct.csv",encoding='utf-8')
# finalizeddataframe=pd.concat([finalproduct,df_accurateexchangerate],axis=1,ignore_index=False)
#
# def multiplyit(row):
#     #print("row"+str(row["ExchangeRate"]))
#     #print("fin"+str(row['PayP+Stripe']))
#     floatt=row['ExchangeRate']
#     #print(type(row["ExchangeRate"]))
#     #print(type(row["PayP+Stripe"]))
#
#     in_pln= floatt*float(row['PayP+Stripe'])
#
#     return in_pln
#
#
# finalizeddataframe['PLN'] = finalizeddataframe.apply(lambda row: multiplyit(row), axis=1)
#
#
# finalizeddataframe.to_csv(pathh+"\Final_"+Month+".csv",encoding='utf-8')
#
# os.remove(pathh+r"\finalproduct.csv")
#
# press=input("Press Any key to close application")
#strippe file has header named "created"
# stripe ki file main start date ki row zaroori honi chhye aur end date bhi lazmi honi chhye,warna vo miss kar dega row
#means agar last day of month main koi order stripe pe nahe aya,yan phir first day of month ma order nahe aya hua to masla ho jaega.