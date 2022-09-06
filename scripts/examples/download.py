import time
import requests
from datetime import datetime

ticker = input("Enter the ticker symbol eg : AAPL")
from_date =  input("Enter start date with format yyyy/mm/dd : ")
to_date =  input("Enter end date with format yyyy/mm/dd : ")

from_time=  datetime.strptime(from_date,"%Y/%m/%d")
to_time =  datetime.strptime(to_date,"%Y/%m/%d")

from_epoch = int(time.mktime(from_time.timetuple()))
to_epoch = int(time.mktime(to_time.timetuple()))


url = f"https://query1.finance.yahoo.com/v7/finance/download/AAPL?period1={from_epoch}&period2={to_epoch}&interval=1d&events=history&includeAdjustedClose=true"


headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
} 

content =  requests.get(url,headers=headers).content

with open("./data.csv","wb") as f:
    f.write(content)
    f.close()
