#Unconfirmed Bitcoin Transactional Tracker 
---

###Brief Overview

---

The Bitcoin(BTC) transactional tracker is a web scrapping software that  scrapes realtime data after every minute
in order to find an aggregate of the top ten transactions, as per the BTC value from lowest to highest.
The transactional data is scrapped from https://www.blockchain.com/btc/unconfirmed-transactions.

---
##Webscrapping(get the data)
If we inspect the page, we notice that each result row is inside a <div> tag with a 'sc-1g6z4xm-0 hXyplo' class. 
The elements that we’re looking for are situated in the following selectors:
``  

    Transactioncontent : Represensts all transctions at the momement
    'Hash': hashh,
    'Time': scrapperTime,
    'Amount BTC': amtBTC,
    'Amount USD': amtUSD


To get the transactional data from the website, I employ the BeautifulSoup from the bs4 package. 
The following code is a reprsenstation of the variable here above;



    transaction_content = soup.find_all('div', class_='sc-1g6z4xm-0 hXyplo')

    for transaction in transaction_content:
        hashh = transaction.find('a',class_='sc-1r996ns-0 fLwyDF sc-1tbyx6t-1 kCGMTY iklhnl-0 eEewhk d53qjk-0 ctEFcK').text
        time = transaction.find('span', class_='sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC').text
        amtBTC = transaction.find('div', class_='sc-1au2w4e-0 fTyXWG').find('span', class_='sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC').text
        amtUSD = transaction.find('div', class_='sc-1au2w4e-0 fTyXWG').find_next_sibling('div').find('span', class_='sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC').text



##Storing/Logging the data
As the scrapper runs, the transactions are appended to a text/csv file, from lowest to highest. On the first instance,
the scrapper should run and store the data in a text/csv file. Every minute it should log in new information in the initial txt/csv file.



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

