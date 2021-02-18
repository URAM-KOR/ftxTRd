import ccxt
import json
import pandas as pd
import tkinter
import time
import os

# api and secret

apiKey = input("Enter API Key:")
secret = input("Enter Secret Key:")
subaccount = input("Enter Sub Account Name or 0 for Main:")

# exchange detail
exchange = ccxt.ftx({
    'apiKey':apiKey, 'secret':secret, 'enableRateLimit':True
})

# sub Account Check

if subaccount == "0":
    print("This is Main Account")
else:
    exchange.headers = {
        "FTX-SUBACCOUNT" : subaccount,
    }

#Global Variable Setting
pair = 'BTC-PERP'
tf = '5m'

#Get Price Hist Data

def priceHistdata():

        try:
            priceData = pd.DataFrame(exchange.fetch_ohlcv(pair,tf))
        except ccxt.NetworkError as e:
            print(exchanged.id, 'fetch_ohlcv failed due to a network error:', str(e))
            priceData = pd.DataFrame(exchange.fetch_ohlcv(pair,tf))
        except ccxt.ExchangeError as e:
            print(exchange.id, 'fetch_ohlcv failed due to exchange error:', str(e))
            priceData = pd.DataFrame(exchange.fetch_ohlcv(pair,tf))
        except Exception as e:
            print(exchange.id, 'fetch_ohlcv failed with:', str(e))
            priceData = pd.DataFrame(exchange.fetch_ohlcv(pair,tf))

        return priceData

#Variable setting for minimum Range and minimum Profit

buyRecord = []
minimumRange = 10
minimumProfit = 30
minOrder = min(buyRecord, default=0.0)
maxOrder = max(buyRecord, default=10000000.0)
priceData = priceHistdata()
buySignal = round((priceData.iloc[-31:-1,4].mean())*2)/2
sellSignal = round((priceData.iloc[-11:-1,4].mean())*2)/2



def getProduct():
    print("PRODUCT = ", exchange.symbols)
def getPrice():
   #pair = input("Pair:")
    try:
        r1 = json.dumps(exchange.fetch_ticker(pair))
        dataPrice = json.loads(r1)
        print(exchange)
        print(pair + '=',dataPrice['last'])
    except ccxt.NetworkError as e:
        r1 = json.dumps(exchange.fetch_ticker(pair))
        dataPrice = json.loads(r1)
    except ccxt.ExchangeError as e:
        r1 = json.dumps(exchange.fetch_ticker(pair))
        dataPrice = json.loads(r1)
    except Exception as e:
        r1 = json.dumps(exchange.fetch_ticker(pair))
        dataPrice = json.loads(r1)

    return (dataPrice['last'])

#def getBalance():
 #   print("PORT BALANCE =", exchange.fetch_getBalance())

def showPending():
    print("Your Pending Oder")
    df1 = pd.DataFrame(exchange.fetch_open_orders(pair),
                       columns=['id','datetime','status','symbol','type','side','price','amount','filled','average','remaining'])
    display(df1)
    pendingOrder.head(5)
    return pendingOrder

def showMatched():
    print("Your Matched Order")
    df2 = pd.DataFrame(exchange.fechMyTraders(pair),
                       columns=['id', 'datetime', 'status', 'symbol', 'type', 'side', 'price', 'amount', 'filled',
                                'average', 'remaining'])
    display(df2)
    print(matchOrder.head(5))
    return matchedOrder

def sendOrder():
    pair = input("Symbol:")
    types = 'limit'
    side = input("buy or sell:")
    usd = float(input("Size-USD:"))
    price = float(input("Price:"))
    size_order = usd/price
    reduceOnly = False
    postOnly = False
    ioc = False



def sendBuy():
    types = 'limit'
    side = 'buy'
    usd = 1
    price = buySignal + 20
    size_order = usd/price
    reduceOnly = false
    postOnly = false
    ioc = false

def sendSell():
    types = 'limit'
    side = 'sell'
    usd = 1
    price = sellSignal - 20
    size_order = usd/price
    reduceOnly = True
    postOnly = False
    ioc = False

    ## Send Order ##
    exchange.create_order(pair, types, side, size_order, price)

    ## Show Order Status##
    print("    ")
    showPending()
    print("    ")
    showMatched()

def readOrder():
    #Read Order To file
    with open('list.txt', "r") as f:
        for line in f:
            buyRecord.append(float(line.strip()))
    print(buyRecord)

def writeOrder():
    with open("list.txt", "w") as f:  #Write order To file
        for ord in buyRecord:
            f.write(str(ord) + "\n")

#LOGIC SESSION

def chenckBuycondition():

    #Buy condition
    if getPrice() == buySignal and len(buyRecord) <= 30 and buyRecord.count(buySignal) < 1:
        if (minOrder - getPrice()) > minimumRange or (getPrice() - maxOrder) > 10 or len(buyRecord) < 1:
            sendBuy()
            print('Buy 1 USD at' + str(buySignal))
            buyRecord.append(buySignal)
            writeOrder()

        else:
            print('Not enough minimum Range = ' + str(minimumRange))
    else:
        print(getPrice())
        print('waiting for buy signal ' + 'at ' + str(buySignal))

def checksellcondition():

    #sell signal function
    if len(buyRecord) > 0:
        if getPrice() <= sellSignal and getPrice() - minOrder > 0:
            print('sell signal triggered at '+str(sellSignal))
            for ord in buyRecord:
                if getPrice() - ord > minimumProfit:
                    sendSell()
                    buyRecord.remove(ord)
                    print(buyRecord)
                    writeOrder()
                else:
                    print('Not Enough Profit ' + 'Minimum = ' + str(ord + minimumProfit))

        else:
            print('Waiting for last minimum order ' + 'at ' + str(minOrder))
    else: print('No Buy Order Record')
    print("   ")


def cancelOrder():
    id = input("Id Number to Cancel:")
    try:
        exchange.cancel_order(id)
        print('Your ID No. ' + id + ' has been cancelled')
    except:
        print("Please Input Correct Id number")

def checkOrder():
    pair = input("Symbol:")
    try:
        showPending(pair)
        print("     ")
        showMatched(pair)

    except:
        print("please input correct pair")

#getBalance()
#getProduct()
#getPrice()
#sendOrder()
#cancelOrder()
#checkOrder()

#Excute Session

while True:
    getProduct()
    buyRecord = []
    priceData = priceHistdata()
    buySignal = round((priceData.iloc[-31:-1,4].mean())*2) / 2
    sellSignal = round((priceData.iloc[-11:-1,4].mean())*2) / 2
    print(time.ctime())
   #readOrder()
    minOrder = min(buyRecord, default=0.0)
    maxOrder = max(buyRecord, default=10000000.0)
    getPrice()
    chenckBuycondition()
    checksellcondition()
    time.sleep(1)