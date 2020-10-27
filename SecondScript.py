import pandas as pd


pathh=input("Enter full Path of the final file: " )
#pathh=r"E:\fiverr\poland\April"
filename=input("Enter name of the final file:(not file extension/must be a csv file ")
#filename="Final_04"
#pathh=r"E:\fiverr\poland\stripe\june ok\Final_06.csv"
df = pd.read_csv(pathh+r"\\"+filename+".csv", thousands=' ', encoding="ISO-8859-1")


def replacecomma(row):
    return row['toconvert'].replace(",",".")

def replacewhitespace(row):
    return row['toconvert'].replace("\s","")

df['toconvert'] = df['toconvert'].str.replace("\s", "")
print(df['toconvert'])

df['toconvert']=df.apply(lambda row: replacecomma(row), axis=1)
df['toconvert']=df.apply(lambda row: replacewhitespace(row), axis=1)

exchangerate=df['ExchangeRate'].astype(float)
toconvert=df['toconvert'].astype(float)
df['converted']=exchangerate*toconvert
print(df['converted'])


#print(df.to_csv(r"E:\fiverr\poland\stripe\june ok\CustomColumnColumn.csv"))
def multiplyit(row):
    in_pln=float(row['toconvert'].replace("\s", ""))*float(row['ExchangeRate'])
    return  in_pln

print(df['toconvert'])
print(df['PayP+Stripe'])
df['converted'].to_csv(pathh+"\SingleCalculateColumn.csv")

