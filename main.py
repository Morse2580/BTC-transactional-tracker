import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from time import gmtime, strftime
import os
import csv
from  pymongo  import  MongoClient
import  pymongo  as mongo
from requests.api import get

class btc_Transactions:
    def __init__(self):
        self.url = 'https://www.blockchain.com/btc/unconfirmed-transactions'
        self.lstTransactions = []

    #get all the data from the page
    def getTransactions(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, 'html.parser')
        transaction_content = soup.find_all('div', class_='sc-1g6z4xm-0 hXyplo')
        
        self.lstTransactions = []
        
        for transaction in transaction_content:
            hashh = transaction.find('a',class_='sc-1r996ns-0 fLwyDF sc-1tbyx6t-1 kCGMTY iklhnl-0 eEewhk d53qjk-0 ctEFcK').text
            time = transaction.find('span', class_='sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC').text
            amtBTC = transaction.find('div', class_='sc-1au2w4e-0 fTyXWG').find('span', class_='sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC').text
            amtBTC = amtBTC.strip(' BTC')
            amtUSD = transaction.find('div', class_='sc-1au2w4e-0 fTyXWG').find_next_sibling('div').find('span', class_='sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC').text
            # Correct the time deficit, in this case, 2 hours
            scrapperTime = datetime.strptime(time, '%H:%M')
            scrapperTime = scrapperTime + timedelta(hours=2)
            scrapperTime = scrapperTime.strftime("%H:%M")

            self.lstTransactions.append({
                'Hash': hashh,
                'Time': scrapperTime,
                'Amount BTC': amtBTC,
                'Amount USD': amtUSD
            })
        #sorted according to BTC_values
        transactionsAsc = sorted(self.lstTransactions, key=lambda price: float(price['Amount BTC']), reverse = True)
        transactionsAsc = transactionsAsc[(len(transactionsAsc) - 10):len(transactionsAsc)]
        return transactionsAsc

    #Add data to a document database, MongoDB
    def mongoDatabase(self):
        connect =  MongoClient()
        db = connect.BTC_db
        collection = db.BTC_transactions
        collection.insert_many(self.getTransactions())

    #write to csv file
    def logTransactions(self):
        if os.path.exists('./TopTenTransactions.txt'):
            fieldnames = ['Hash', 'Time', 'Amount BTC', 'Amount USD']
            with open('TopTenTransactions.json', 'a', encoding='UTF8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                f.write("\n")
                f.write("\n")
                f.write("\n")
                writer.writerows(self.getTransactions())
                f.close()
        else:
            fieldnames = ['Hash','Time', 'Amount BTC','Amount USD']
            with open('TopTenTransactions.txt', 'w', encoding='UTF8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                f.write("\n")
                f.write("\n")
                f.write("\n")
                writer.writerows(self.getTransactions())
                f.close()
    def run_scrapper(self):
        while True:
            self.getTransactions()
            self.mongoDatabase()
            self.logTransactions()
            time.sleep(60)

run_program =  btc_Transactions()
run_program.run_scrapper()
