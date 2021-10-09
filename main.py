import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import operator
import csv
import os


url = ('https://www.blockchain.com/btc/unconfirmed-transactions')
#create a list to store all the transactions
lstTransactions = []

#get all the data from the page
def getTransactions():
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    transaction_content = soup.find_all('div', class_='sc-1g6z4xm-0 hXyplo')

    for transaction in transaction_content:
        hashh = transaction.find('a',class_='sc-1r996ns-0 fLwyDF sc-1tbyx6t-1 kCGMTY iklhnl-0 eEewhk d53qjk-0 ctEFcK').text
        time = transaction.find('span', class_='sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC').text
        amtBTC = transaction.find('div', class_='sc-1au2w4e-0 fTyXWG').find('span', class_='sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC').text
        amtUSD = transaction.find('div', class_='sc-1au2w4e-0 fTyXWG').find_next_sibling('div').find('span', class_='sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC').text

        # Correct the time deficit, in this case, 2 hours
        scrapperTime = datetime.strptime(time, '%H:%M')
        scrapperTime = scrapperTime + timedelta(hours=2)
        scrapperTime = scrapperTime.strftime("%H:%M")

        lstTransactions.append({
            'Hash': hashh,
            'Time': scrapperTime,
            'Amount BTC': amtBTC,
            'Amount USD': amtUSD
        })
    #sorted according to values
    transactionsAsc = sorted(lstTransactions, key=operator.itemgetter('Amount BTC'))
    transactionsAsc = transactionsAsc[(len(transactionsAsc)-10):len(transactionsAsc)]
    return transactionsAsc

#write to csv file
def logTransactions():
    if os.path.exists('./TopTenTransactions.txt'):
        fieldnames = ['Hash', 'Time', 'Amount BTC', 'Amount USD']
        with open('TopTenTransactions.txt', 'a', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerows(getTransactions())
            f.close()
    else:
        fieldnames = ['Hash','Time', 'Amount BTC','Amount USD']
        with open('TopTenTransactions.txt', 'w', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(getTransactions())

while True:
    getTransactions()
    logTransactions()
    time.sleep(60)