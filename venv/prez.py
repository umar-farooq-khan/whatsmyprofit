

#Month = input("Of which month are these csv files?")
import datetime
from calendar import monthrange
import pandas as pd
import requests
from bdateutil import isbday
import os

# the accurate file accurate script for prez
print("HELP/NOTE")
print("1) There must be a file named accurateexchangerate, accurateexchange file will be generated automatically when you run this script for the first time")
print("2) Add a new column in this file, name of it column must be 'toconvert'")
print("3) After running this script first time, now in this accurateexchangerate file write all the amounts to be converted")
print("4) Now run this script again")
print("5) Your input column should not have comma instead of dot(for thousands) and spaces in the numbers")
# strippe file has header named "created"
    # stripe ki file main start date ki row zaroori honi chhye aur end date bhi lazmi honi chhye,warna vo miss kar dega row
    # means agar last day of month main koi order stripe pe nahe aya,yan phir first day of month ma order nahe aya hua to masla ho jaega.



print("\n")

workingpath=input("Enter working path: ")
#workingpath=r"C:\Users\Hp\Downloads"
checkfile=workingpath+r"\accurateexchangerate.csv"
is_avail=os.path.isfile(checkfile)
Month = input("Of which month are these csv files?")


if(is_avail==False):

    Month = "0" + str(Month)
    if (len(Month) == 3):
        Month = Month[1] + Month[2]
    now = datetime.datetime.now()

    maxdays = monthrange(2021, int(Month))
    #print(maxdays[1])
    pichlamonth = int(Month) - 1
    pichlamonth = "0" + str(pichlamonth)
    #print("pichla month",pichlamonth)
    if (len(pichlamonth) == 3):
        pichlamonth = pichlamonth[1] + pichlamonth[2]

    pichlamonthmaxdays = monthrange(2021, int(pichlamonth))
    #print("pichlamonthmax",str(pichlamonthmaxdays))
    isbusdaybool = False

    finditday = str(pichlamonthmaxdays[1])
    while (isbusdaybool == False):
        print("in while loop")
        datetocheck = "2021-" + pichlamonth + "-" + str(finditday)
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
    #print(url)
    #url= "http://api.nbp.pl/api/exchangerates/rates/a/usd/2020-11-30/2020-12-30/?format=json"
    r = requests.get(url).json()

    dates = []
    exchangerate = []
    ###############################3
    for i in range(0, len(r['rates'])):
        dates.append(str(r['rates'][i]['effectiveDate']))
        exchangerate.append(r['rates'][i]['mid'])
    df_missing = pd.DataFrame({'dt': dates, 'ExchangeRate': exchangerate})

    newdatelist = []
    newratelist = []
    from datetime import date, timedelta

    d1 = date(int(now.year), int(Month), 1)
    d2 = date(int(now.year), int(Month), maxdays[1])
    delta = d2 - d1
    datelist=[]
    for i in range(delta.days + 1):
        datelist.append(d1 + timedelta(days=i))
    print((datelist[1]))
    finalproductdate=datelist
    print(len(finalproductdate))



    for k in range(0, len(finalproductdate)):
        if (k == 0):
            newratelist.append(float(df_missing['ExchangeRate'].iloc[0]))
            newdatelist.append(df_missing['dt'].iloc[0])
            #print(newdatelist)
            #print(newratelist)
        if (k == 30):
            print("#$%^&")
        #onedate = str(finalproduct['created_utc'].iloc[k])
        onedate = str(finalproductdate[k])   #fulldatedf, kahi aur se b uthai ja skti hai


        #print("tofind"+onedate)
        # creating and passsing series to new column
        xx = df_missing.loc[df_missing['dt'] == onedate]
        if (xx.empty == False):
            #print("not found")
            #print("rate going to append"+str(xx['ExchangeRate'].values.min()))
            #print("date going to append"+str(onedate))
            newratelist.append(float(xx['ExchangeRate'].values.min()))
            newdatelist.append(onedate)
        if (xx.empty == True):
            #print("this date not found" + str(onedate))
            #print("date going to append:"+onedate)
            #print("rate going to append: pichla wala"+str(newratelist[-1]))

            newdatelist.append(onedate)
            newratelist.append(float(newratelist[-1]))
        print("xxxxxxxxxxxxxx")

    newdatelist.pop()
    newratelist.pop()


    newratelist = newratelist[::-1]
    newdatelist = newdatelist[::-1]
    df_accurateexchangerate = pd.DataFrame({'dt': newdatelist, 'ExchangeRate': newratelist})
    #print("dfaccurateexchangeratedf")
    #print(df_accurateexchangerate)
    #df_accurateexchangerate
    #abhi likh raha ye line
    #neche wale abhi comment kee
    #finalproduct = pd.read_csv(pathh + r"\finalproduct.csv", encoding='utf-8')


    df_accurateexchangerate.to_csv(checkfile, encoding="utf-8")

# , encoding="ISO-8859-1"
if(is_avail==True):
    finalizeddataframe = pd.read_csv(checkfile)


    def replacecomma(row):
        return row['toconvert'].replace(",", ".")

    def replacewhitespace(row):
        return row['toconvert'].replace("\s", "")


    #inalizeddataframe['toconvert'] = finalizeddataframe.apply(lambda row: replacecomma(row), axis=1)
    #print((finalizeddataframe))

    #finalizeddataframe['toconvert'] = finalizeddataframe['toconvert'].str.replace("\s", "")

    #finalizeddataframe['toconvert'] =finalizeddataframe.apply(lambda row: replacewhitespace(row), axis=1)
    #print((finalizeddataframe))


    finalizeddataframe['toconvert']=finalizeddataframe['toconvert'].astype(float)

    def multiplyit(row):
        floatt = row['ExchangeRate']
        xx=row['toconvert']
        #print(xx)
        in_pln = floatt * float(xx)
        return in_pln


    #print(finalizeddataframe)

    finalizeddataframe['PLN'] = finalizeddataframe.apply(lambda row: multiplyit(row), axis=1)

    #print("Finalfileputting")
    #print(finalizeddataframe)
    finalizeddataframe.to_csv(workingpath + "\SingleColumn" + str(Month) + ".csv", encoding='utf-8')


    # strippe file has header named "created"
    # stripe ki file main start date ki row zaroori honi chhye aur end date bhi lazmi honi chhye,warna vo miss kar dega row
    # means agar last day of month main koi order stripe pe nahe aya,yan phir first day of month ma order nahe aya hua to masla ho jaega.
