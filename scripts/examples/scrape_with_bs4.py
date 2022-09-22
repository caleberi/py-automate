from bs4 import BeautifulSoup
import requests

def get_currency(in_currency:str, out_currency:str, amount:int):
    url = f'https://www.x-rates.com/calculator/?from={in_currency}&to={out_currency}&amount={amount}'
    content = requests.get(url).text
    soup = BeautifulSoup(content,"html.parser")
    rate = soup.find("span", class_ = "ccOutputRslt").get_text()
    rate = float(rate[:-4])

    print(type(rate))
    return rate

print(get_currency("EUR","AUD",1))
