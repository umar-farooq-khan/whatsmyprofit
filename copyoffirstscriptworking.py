
import pandas as pd
from bdateutil import isbday
# created utc naam hona chhye
# file main first tareekh honi chhye aur last

pathh = input("Enter Path of the files:  ")
#pathh = r"E:\fiverr\poland\stripe\may ok"
dfstripe = pd.read_csv(pathh + "\stripe.csv", encoding='utf-8')
paypaldf = pd.read_excel(pathh + "\paypal.xlsx", decimal=",", thousands=' ')
date = paypaldf.iloc[14:-2, 0]  # date
# date=date.dropna()
# paypaldf.to_csv(pathh+"\date.csv", encoding="utf-8")

C = paypaldf.iloc[14:-2, 2]  # C=2

C = C.str.replace(",", ".")

C = C.str.replace("\s", "")
C = C.astype(float)


D = paypaldf.iloc[14:-2, 3]  # D=3
# print(D)

D = D.str.replace("\s", "")
D = D.str.replace(",", ".")
D = D.astype(float)


F = paypaldf.iloc[14:-2, 5]  # F=5
# print(F)
F = F.str.replace("\s", "")
F = F.str.replace(",", ".")
F = F.astype(float)


G = paypaldf.iloc[14:-2, 6]  # G=6
G = G.str.replace("\s", "")
G = G.str.replace(",", ".")
G = G.astype(float)


paypaldf['totalprofitpaypal'] = C + D + F + G
paypaldf = paypaldf.iloc[14:]  # deleted upper 14 rows
paypaldf = paypaldf.iloc[:-2]

dfstripe = dfstripe.set_index(pd.to_datetime(dfstripe['created_utc']))
# except KeyError:
#     dfstripe = dfstripe.set_index(pd.to_datetime(dfstripe['created']))

dfstripe = dfstripe.resample('D').sum()
#################################dfstripe=dfstripe.loc[3]

dfstripe = dfstripe['net']
dfstripe = dfstripe.iloc[::-1]

paypaldf.to_csv(pathh + r"\temp_totalprofit_paypal.csv")
dfstripe.to_csv(pathh + r"\temp_totalprofit_stripe.csv")

newstripe = pd.read_csv(pathh + r"\temp_totalprofit_paypal.csv", encoding='utf-8')
newpaypal = pd.read_csv(pathh + r"\temp_totalprofit_stripe.csv", encoding='utf-8')

appended = pd.concat([newpaypal, newstripe], axis=1, ignore_index=False)
print("appendeddd")
print(appended)

appended['PayP+Stripe'] = appended.iloc[:,1] + appended['totalprofitpaypal']

import requests
import datetime
from calendar import monthrange

dates = []
exchangerate = []
print("appendeddd")
print(appended)
appended.to_csv(pathh + r"\Netprofit.csv")


import os

os.remove(pathh + r"\temp_totalprofit_paypal.csv")
os.remove(pathh + r"\temp_totalprofit_stripe.csv")
# nownewdf = pd.read_csv(pathh + r"\Netprofit.csv",
#                            usecols=['created_utc', 'net', 'totalprofitpaypal', 'PayP+Stripe'], encoding='utf-8')
# ye abhi comment kia q k is main sare cols mojood nahe thy
nownewdf = pd.read_csv(pathh + r"\Netprofit.csv",
                           encoding='utf-8')
print("nownewwwwwww")
print(nownewdf)
# except ValueError:
#     nownewdf = pd.read_csv(pathh + r"\Netprofit.csv", usecols=['created', 'net', 'totalprofitpaypal', 'PayP+Stripe'],
#                            encoding='utf-8')
#nownewdf=DataFrame(nownewdf).columns=['created_utc', 'net']

#nownewdf.to_csv(pathh + r"\finalproduct.csv", header="")
os.remove(pathh + r"\Netprofit.csv")
# normalize that format in which both can be compared
#finalproduct = pd.read_csv(pathh + r"\finalprodt.csv", encoding='utf-8')
#ye change kar ke
#finalproduct = pd.read_csv(pathh + r"\Netprofit.csv", encoding='utf-8')
finalproduct=nownewdf
finalproduct = finalproduct.iloc[::-1]


Month = input("Of which month are these csv files?")
# Month="6"
Month = "0" + str(Month)
if (len(Month) == 3):
    Month = Month[1] + Month[2]
now = datetime.datetime.now()

maxdays = monthrange(2020, int(Month))
print(maxdays[1])
pichlamonth = int(Month) - 1
pichlamonth = "0" + str(pichlamonth)
print("pichla month",pichlamonth)
if (len(pichlamonth) == 3):
    pichlamonth = pichlamonth[1] + pichlamonth[2]

pichlamonthmaxdays = monthrange(2020, int(pichlamonth))
print("pichlamonthmaxdays",str(pichlamonthmaxdays))
isbusdaybool = False

finditday = str(pichlamonthmaxdays[1])
while (isbusdaybool == False):
    print("in while loop")
    datetocheck = "2020-" + pichlamonth + "-" + str(finditday)
    print("datetocheck" + str(datetocheck))
    isbusdaybool = isbday(datetocheck)

    print("isbool= " + str(isbusdaybool))
    if (isbusdaybool == True):
        print("true agya")
        break
    finditday = str(int(finditday) - 1)

# previouslastdate= monthrange(2020,int(pichlamonth))
url = 'http://api.nbp.pl/api/exchangerates/rates/a/usd/' + str(now.year) + "-" + str(pichlamonth) + "-" + str(
    finditday) + "/" + str(now.year) + "-" + str(Month) + "-" + str(int(maxdays[1]) - 1) + "/?format=json"
print(url)

r = requests.get(url).json()
#print(r)
dates = []
exchangerate = []
print(len(r['rates']))
#r['rates'][0]['mid']
# YYYY-MM-DD
str(r['rates'][0]['effectiveDate'])
for i in range(0, len(r['rates'])):
    dates.append(str(r['rates'][i]['effectiveDate']))
    exchangerate.append(r['rates'][i]['mid'])
df_missing = pd.DataFrame({'dt': dates, 'ExchangeRate': exchangerate})

#df_missing
newdatelist = []
newratelist = []
print("final prioduct")
print(finalproduct)

for k in range(0, len(finalproduct)):
    if (k == 0):
        newratelist.append(float(df_missing['ExchangeRate'].iloc[0]))
        newdatelist.append(df_missing['dt'].iloc[0])
        print(newdatelist)
        print(newratelist)
    if (k == len(finalproduct)):
        print("dont add anything")
    #onedate = str(finalproduct['created_utc'].iloc[k])
    onedate = str(finalproduct.iloc[k,1])


    # print("tofinddate"+onedate)
    # creating and passsing series to new column
    xx = df_missing.loc[df_missing['dt'] == onedate]
    if (xx.empty == False):
        # print("not found")
        # print("rate going to append"+str(xx['ExchangeRate'].values.min()))
        # print("date going to append"+str(onedate))
        newratelist.append(float(xx['ExchangeRate'].values.min()))
        newdatelist.append(onedate)
    if (xx.empty == True):
        # print("this date not found" + str(onedate))
        # print("date going to append:"+onedate)
        # print("rate going to append: pichla wala"+str(newratelist[-1]))

        newdatelist.append(onedate)
        newratelist.append(float(newratelist[-1]))
    # print("xxxxxxxxxxxxxx")

newdatelist.pop()
newratelist.pop()
len(newratelist)
#newratelist
#newdatelist

# for j in range(0, len(newdatelist)):
#     print(newdatelist[j])
#
#     print(newratelist[j])

newratelist = newratelist[::-1]
newdatelist = newdatelist[::-1]
df_accurateexchangerate = pd.DataFrame({'dt': newdatelist, 'ExchangeRate': newratelist})
#df_accurateexchangerate
#abhi likh raha ye line
#neche wale abhi comment kee
#finalproduct = pd.read_csv(pathh + r"\finalproduct.csv", encoding='utf-8')
finalizeddataframe = pd.concat([finalproduct, df_accurateexchangerate], axis=1, ignore_index=False)


def multiplyit(row):
    # print("row"+str(row["ExchangeRate"]))
    # print("fin"+str(row['PayP+Stripe']))
    floatt = row['ExchangeRate']
    # print(type(row["ExchangeRate"]))
    # print(type(row["PayP+Stripe"]))

    in_pln = floatt * float(row['PayP+Stripe'])

    return in_pln


finalizeddataframe['PLN'] = finalizeddataframe.apply(lambda row: multiplyit(row), axis=1)

finalizeddataframe.to_csv(pathh + "\Final_" + Month + ".csv", encoding='utf-8')

#os.remove(pathh + r"\finalproduct.csv")

press = input("Press Any key to close application")
# strippe file has header named "created"
# stripe ki file main start date ki row zaroori honi chhye aur end date bhi lazmi honi chhye,warna vo miss kar dega row
# means agar last day of month main koi order stripe pe nahe aya,yan phir first day of month ma order nahe aya hua to masla ho jaega.
