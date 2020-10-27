

import pandas as pd
import pandas as pd

import requests
from calendar import monthrange
import datetime

import pandas as pd
from bdateutil import isbday
from datetime import date
def multiplyit(row):
    inpln=float(row['toconvert'])*float(row['ExchangeRate'])
    return inpln
def replacecomma(row):
    return row['toconvert'].replace(",",".")

try:
    dff=pd.read_csv(r"E:\fiverr\poland\stripe\june ok\accuratedff.csv")

    dff['toconvert'] = dff.apply(lambda row: replacecomma(row), axis=1)
    print("filefound")

    dff['in_PLN']= dff.apply(lambda row: multiplyit(row), axis=1)
    print(dff)
except FileNotFoundError:
    print("not found")

    #Month=input("Of which month are these csv files?")
    Month="6"
    Month="0"+str(Month)
    if(len(Month)==3):
        Month=Month[1]+Month[2]
    now = datetime.datetime.now()

    maxdays=monthrange(2020,int(Month))
    print(maxdays[1])
    pichlamonth= int(Month)-1
    pichlamonth="0"+str(pichlamonth)
    if(len(pichlamonth)==3):
        pichlamonth=pichlamonth[1]+pichlamonth[2]

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






    #previouslastdate= monthrange(2020,int(pichlamonth))
    url='http://api.nbp.pl/api/exchangerates/rates/a/usd/'+str(now.year)+"-"+str(pichlamonth)+"-"+str(finditday)+"/"+str(now.year)+"-"+str(Month)+"-"+str(int(maxdays[1])-1)+"/?format=json"
    print(url)

    r =requests.get(url).json()
    #print(r)
    dates=[]
    exchangerate=[]
    print(len(r['rates']))
    r['rates'][0]['mid']
    #YYYY-MM-DD
    str(r['rates'][0]['effectiveDate'])
    for i in range(0,len(r['rates'])):
        dates.append(str(r['rates'][i]['effectiveDate']))
        exchangerate.append(r['rates'][i]['mid'])
    df_missing = pd.DataFrame({'dt': dates, 'ExchangeRate': exchangerate})

    df_missing
    newdatelist=[]
    newratelist=[]
    # just read stripe file and make sum of it just to get all the dates
    # then make a df
    stripepath=r"E:\fiverr\poland\stripe\june ok\stripe.csv"
    dfstripe= pd.read_csv(stripepath)
    print("createddd", dfstripe['created'])

    dfstripe = dfstripe.set_index(pd.to_datetime(dfstripe['created']))

    dfstripe = dfstripe.resample('D').sum()
    #dfstripe = dfstripe['net']
    print("df stripeeee")
    print(dfstripe.to_csv(r"E:\fiverr\poland\stripe\june ok\stripedfaccuratedate.csv"))
    dfstripe=pd.read_csv(r"E:\fiverr\poland\stripe\june ok\stripedfaccuratedate.csv")
    print(dfstripe['created'])

    dfstripe = dfstripe.iloc[::-1]
    finalproduct=dfstripe
    print("final")
    print(finalproduct)
    for k in range(0,len(finalproduct)):
        if(k==0):
            newratelist.append(float(df_missing['ExchangeRate'].iloc[0]))
            newdatelist.append(df_missing['dt'].iloc[0])
            print(newdatelist)
            print(newratelist)
        if(k==len(finalproduct)):
            print("dont add anything")
        onedate=str(finalproduct['created'].iloc[k])

        #print("tofinddate"+onedate)
        # creating and passsing series to new column
        xx=df_missing.loc[df_missing['dt'] == onedate]
        if(xx.empty==False):
            #print("not found")
            #print("rate going to append"+str(xx['ExchangeRate'].values.min()))
            #print("date going to append"+str(onedate))
            newratelist.append(float(xx['ExchangeRate'].values.min()))
            newdatelist.append(onedate)
        if(xx.empty==True):
            #print("this date not found" + str(onedate))
            #print("date going to append:"+onedate)
            #print("rate going to append: pichla wala"+str(newratelist[-1]))

            newdatelist.append(onedate)
            newratelist.append(float(newratelist[-1]))
        #print("xxxxxxxxxxxxxx")


    newdatelist.pop()
    newratelist.pop()
    len(newratelist)
    print(newratelist)
    print(newdatelist)





    # for j in range(0, len(newdatelist)):
    #     print(newdatelist[j])
    #
    #     print(newratelist[j])

    newratelist=newratelist[::-1]
    newdatelist=newdatelist[::-1]
    df_accurateexchangerate = pd.DataFrame({'dt': newdatelist, 'ExchangeRate': newratelist})
    print(df_accurateexchangerate)
    df_accurateexchangerate=df_accurateexchangerate[::-1]
    df_accurateexchangerate.to_csv(r"E:\fiverr\poland\stripe\june ok\accuratedff.csv")
