from __future__ import division
from urllib.request import urlopen
from pprint import pprint
import urllib.request, urllib.parse, urllib.error
import json
from datetime import datetime
import time

# SMA algo
def get_SMA(values, size):
    for selection in values :
        return sum(selection) / size


# gestion de la pile pour calculer les valeurs de SMA
def depiler_values(values) :
    pile = []
    for element in values :
        pile.append(element)
    x = pile[0]
    del pile[0]
    return pile


# tester si la date compris entre date1 et date2
def test_date(date):
    print(date)
    date1 = "05/25/2018"
    date2 = "16/10/2018"
    date_1 = datetime.strptime(date1, "%m/%d/%Y")
    date_2 = time.strptime(date2, "%d/%m/%Y")
    date_new = datetime.strptime(str(date), "%d/%m/%Y")
    if (date_new > date_1 and date_new<date_2) :
        return True
    return False



# calcul des SMA et les prix moyens :
def calcul (symb):
    # calcul des prix moyen
    prix_moyen = []
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo".format(symb)
    stockdata = urllib.request.urlopen(url)
    data = stockdata.read().decode()
    js = json.loads(data)
    jstring = 'Time Series (Daily)'
    for entry in js:
        i = js[jstring].keys()
        for jkeys in i:
            # tester selon la date ; 25/05/2018 au 16/10/2018
            if( test_date(js[jstring][jkeys])):
               # dans ce cas calculer le prix moyen de ce jours
               prix  = ( int(js[jstring][jkeys]['2. high'])+ int (js[jstring][jkeys]['3. low']))/2
              # ajouter ce prix dans la liste de prix_moyen
               prix_moyen.append(prix)

    # calcul SMA
    n = 0
    values=[]
    SMA= [ ]
    for entry2 in js :
        i = js[jstring].keys()
        for jkeys in i:
            n = n+1
            close = int(js[jstring][jkeys]['2. close'])
            # commencer a ajouter les valeurs de close
            values.append(close)
            if (len(values) < 5):
                 continue
            else :
                # tester selon la date ; 25/05/2018 au 16/10/2018
                if (test_date(js[jstring][jkeys])):
                    # dans ce cas on aura notre premiere SMA
                    sma_val = get_SMA(values,5)
                    # depiler la premiere valeurs pour emplier par suite la nouvelle valeur pour la nouvelle SMA
                    depiler_values(values)
                    # ajouter cette SMA dans la liste pour la comparaer par suite
                    SMA.append(sma_val)
                # on depilera uniquement les valeurs sans calculer SMA psq elle n'est pas dans ces deux dates
                depiler_values(values)

    return(SMA,values)



def comparaison(SMA,prix_moyen ):
    # Comparaison entre les deux liste ceux de SMA et prix_moyen si val > 0 on achete sinon on vente
    i =0
    while (i > len(SMA)):
            benefice  = int(SMA[i])-int(prix_moyen[i])
    return benefice


#----------------------------------MAIN -----------------------------------------

# affichage  des donnée
url = ("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo")
u = urlopen(url)
data_json = json.loads(u.read().decode('utf-8'))
pprint(data_json) # affichage des données

# recuperation pour les deux liste SMA et prix_moyen pour la comparaison  :
SMA,prix_moyen = calcul('MSFT')
# affichage du benefice :
benefice = comparaison(SMA,prix_moyen )
print(benefice)



# get SMA :

