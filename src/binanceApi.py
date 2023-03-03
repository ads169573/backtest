import requests
import json
from datetime import datetime
import hmac
import hashlib
import urllib.parse
import time
import websocket

class Builder(object):

    def __init__(self):
        self.params = dict()
        self.posts = dict()

    def put_url(self, name, value):
        if value is not None:
            if isinstance(value, list):
                self.params[name] = json.dumps(value)
            elif isinstance(value, float):
                self.params[name] = ('%.20f' % (value))[slice(0, 16)].rstrip('0').rstrip('.')
            else:
                self.params[name] = str(value)
    def put_post(self, name, value):
        if value is not None:
            if isinstance(value, list):
                self.posts[name] = value
            else:
                self.posts[name] = str(value)

    def build_url(self):
        if len(self.params) == 0:
            return ""
        encoded_param = urllib.parse.urlencode(self.params)
        return encoded_param

    def build_url_to_json(self):
        return json.dumps(self.params)

class binanceApi():
    
    def __init__(self):
        self.baseUrl = 'https://fapi.binance.com'
        self.api_key = '' #api_key
        self.secret_key = '' #secret_key

    #timestamp to '%Y-%m-%d %H:%M:%S'
    def ts2dateStr(self, ts):
        ts = ts / 1000
        return str(datetime.fromtimestamp(ts))

    #'%Y-%m-%d %H:%M:%S' to timestamp 
    def dateStr2ts(self, dateStr):
        dt_obj = datetime.strptime(dateStr, '%Y-%m-%d %H:%M:%S')
        millisec = dt_obj.timestamp() * 1000
        return int(millisec)

    def getHeader(self):
        header = dict()
        header.update({"X-MBX-APIKEY": self.api_key})
        return header
    #get signature
    def __signature(self,params):
        target = urllib.parse.urlencode(params)
        return hmac.new(
            self.secret_key.encode("utf-8"), target.encode("utf-8"), hashlib.sha256
        ).hexdigest()
        
    #get timestamp
    def get_ts(self):
        return time.time_ns()//1000000
    
    def sendCmd(self, type, url, params):
        url = self.baseUrl + url
        builder = Builder()
        if(params is not None):
            for key in params:
                builder.put_post(key, params[key])
                builder.put_url(key, params[key])
        if(type == 'GET'):
            resp = requests.get(url, headers = self.getHeader(), params = builder.build_url())
        elif(type == 'POST'):
            resp = requests.post(url, headers = self.getHeader(),params = builder.build_url())
        elif(type == 'DELETE'):
            resp = requests.delete(url, params = builder.build_url(), headers = self.getHeader())
        elif(type == 'PUT'):
            resp = requests.put(url, headers = self.getHeader(),params = builder.build_url())
        print(resp.text)
        if(resp.status_code == 200):
            obj = json.loads(resp.text)
            resp.close()
            return obj
        else:
            print(resp.status_code)
            print(resp.text)
        return None
    
    def connect(self, param):
        def on_open(ws):
            print('open connection')
            
        def on_message(ws, message):
            print(json.loads(message))

        def on_close(ws):
            print("closed connection")

        ws = websocket.WebSocketApp('wss://fstream.binance.com/ws/'+param, on_open=on_open, on_message=on_message, on_close=on_close)
        ws.run_forever()
    
#Market Data Endpoints    
    
    #Check Server Time
    def Check_Server_Time(self):
        url= self.baseUrl + '/fapi/v1/time'
        
        resp=requests.get(url)
        if(resp.status_code == 200):
            obj = json.loads(resp.text)
            resp.close()
            return obj
        else:   
            print(resp.status_code)
            print(resp.text)
            resp.close()
        return None
    
    #Exchange Information
    def Exchange_Info(self):
        url = self.baseUrl + '/fapi/v1/exchangeInfo'

        resp = requests.get(url)
        if(resp.status_code == 200):
            obj = json.loads(resp.text)
            resp.close()
            return resp
        else:
            print(resp.status_code)
            print(resp.text)
        return None

    #Order Book
    def Order_Book(self, symbol = None, limit = None):
        url = self.baseUrl + '/fapi/v1/depth'

        builder = Builder()
        builder.put_url("symbol", symbol)
        if(limit is not None):
            builder.put_url("limit", limit)
        
        resp=requests.get(url,params=builder.build_url())
        if(resp.status_code == 200):
            obj = json.loads(resp.text)
            resp.close()
            return obj
        else:   
            print(resp.status_code)
            print(resp.text)
            resp.close()
        return None
    
    #Recent Trades List
    def Recent_Trades_List(self, symbol = None, limit = None):
        url = self.baseUrl + '/fapi/v1/trades'

        builder = Builder()
        builder.put_url("symbol", symbol)
        if(limit is not None):
            builder.put_url("limit", limit)
        
        resp=requests.get(url,params=builder.build_url())
        if(resp.status_code == 200):
            obj = json.loads(resp.text)
            resp.close()
            return obj
        else:   
            print(resp.status_code)
            print(resp.text)
            resp.close()
        return None
    
    #Old Trades Lookup
    def Old_Trades_Lookup(self, symbol = None, limit = None, fromId = None):
        url = self.baseUrl + '/fapi/v1/historicalTrades'

        builder = Builder()
        builder.put_url("symbol", symbol)
        if(limit is not None):
            builder.put_url("limit", limit)
        if(fromId is not None):
            builder.put_url('fromId',fromId)
        
        resp=requests.get(url,params=builder.build_url())
        if(resp.status_code == 200):
            obj = json.loads(resp.text)
            resp.close()
            return obj
        else:   
            print(resp.status_code)
            print(resp.text)
            resp.close()
        return None
    
    #Aggregate Trades List
    def Aggregate_Trades_List(self, symbol = None, fromId = None, startTime = None, endTime = None, limit = None):
        url = self.baseUrl + '/fapi/v1/aggTrades'

        builder = Builder()
        builder.put_url("symbol", symbol)
        if(limit is not None):
            builder.put_url("limit", limit)
        if(fromId is not None):
            builder.put_url('fromId',fromId)
        if(startTime is not None):
            builder.put_url('startTime',startTime)
        if(endTime is not None):
            builder.put_url('endTime',endTime)
        
        resp=requests.get(url,params=builder.build_url())
        if(resp.status_code == 200):
            obj = json.loads(resp.text)
            resp.close()
            return obj
        else:   
            print(resp.status_code)
            print(resp.text)
            resp.close()
        return None

    #Kline_Data
    def Kline_Data(self, symbol = None, startTime = None, endTime = None, interval = None, limit = None):
        url = self.baseUrl + '/fapi/v1/klines'

        builder = Builder()
        
        builder.put_url("symbol", symbol)
        builder.put_url("interval", interval)
        if(startTime is not None):
            builder.put_url("startTime", startTime)
        if(endTime is not None):
            builder.put_url("endTime", endTime)
        if(limit is not None):
            builder.put_url("limit", limit)

        resp = requests.get(url, params = builder.build_url())
        if(resp.status_code == 200):
            obj = json.loads(resp.text)
            resp.close()
            return obj
        else:
            print(resp.status_code)
            print(resp.text)
        return None
    
    #Continous Kline Data
    def Continous_Kline_Data(self, pair = None, startTime = None, endTime = None, interval = None, limit = None, contractType = None):
        url = self.baseUrl + '/fapi/v1/continuousKlines'

        builder = Builder()
        
        builder.put_url("pair", pair)
        builder.put_url("interval", interval)
        builder.put_url("contractType", contractType)
        if(startTime is not None):
            builder.put_url("startTime", startTime)
        if(endTime is not None):
            builder.put_url("endTime", endTime)
        if(limit is not None):
            builder.put_url("limit", limit)
        
        resp = requests.get(url, params = builder.build_url())
        if(resp.status_code == 200):
            obj = json.loads(resp.text)
            resp.close()
            return obj
        else:
            print(resp.status_code)
            print(resp.text)
        return None
    
    #Index Price Kline Data
    def Index_Price_Kline_Data(self, pair = None, startTime = None, endTime = None, interval = None, limit = None):
        url = self.baseUrl + '/fapi/v1/indexPriceKlines'

        builder = Builder()
        
        builder.put_url("pair", pair)
        builder.put_url("interval", interval)
        if(startTime is not None):
            builder.put_url("startTime", startTime)
        if(endTime is not None):
            builder.put_url("endTime", endTime)
        if(limit is not None):
            builder.put_url("limit", limit)

        resp = requests.get(url, params = builder.build_url())
        if(resp.status_code == 200):
            obj = json.loads(resp.text)
            resp.close()
            return obj
        else:
            print(resp.status_code)
            print(resp.text)
        return None
    
    #Mark Price Kline Data
    def Mark_Price_Kline_Data(self, symbol = None, startTime = None, endTime = None, interval = None, limit = None):
        url = self.baseUrl + '/fapi/v1/markPriceKlines'

        builder = Builder()
        
        builder.put_url("symbol", symbol)
        builder.put_url("interval", interval)
        if(startTime is not None):
            builder.put_url("startTime", startTime)
        if(endTime is not None):
            builder.put_url("endTime", endTime)
        if(limit is not None):
            builder.put_url("limit", limit)

        resp = requests.get(url, params = builder.build_url())
        if(resp.status_code == 200):
            obj = json.loads(resp.text)
            resp.close()
            return obj
        else:
            print(resp.status_code)
            print(resp.text)
        return None
    
    #Mark Price
    def Mark_Price(self, symbol = None):
        url = self.baseUrl + '/fapi/v1/premiumIndex'
        
        builder=Builder()
        
        if(symbol is not None):
            builder.put_url("symbol",symbol)
        
        resp = requests.get(url, params = builder.build_url())
        
        if(resp.status_code == 200):
            obj = json.loads(resp.text)
            resp.close()
            return obj
        else:
            print(resp.status_code)
            print(resp.text)
        return None
    
    #Get Funding Rate History
    def Get_Funding_Rate_History(self, startTime = None, endTime = None, limit = None, symbol = None):
        url = self.baseUrl + '/fapi/v1/fundingRate'

        builder = Builder()
        
        if(startTime is not None):
            builder.put_url("symbol", symbol)
        if(startTime is not None):
            builder.put_url("startTime", startTime)
        if(endTime is not None):
            builder.put_url("endTime", endTime)
        if(limit is not None):
            builder.put_url("limit", limit)

        resp = requests.get(url, params = builder.build_url())
        if(resp.status_code == 200):
            obj = json.loads(resp.text)
            resp.close()
            return obj
        else:
            print(resp.status_code)
            print(resp.text)
        return None
    
    #24hr Ticker Price Change Statistics
    def get24hr_Ticker_Price_Change_Statistics(self, symbol = None):
        url = self.baseUrl + '/fapi/v1/24hr'
        
        builder=Builder()
        
        if(symbol is not None):
            builder.put_url("symbol",symbol)
        
        resp = requests.get(url, params = builder.build_url())
        
        if(resp.status_code == 200):
            obj = json.loads(resp.text)
            resp.close()
            return obj
        else:
            print(resp.status_code)
            print(resp.text)
        return None
    
    #Symbol Price Ticker
    def Symbol_Price_Ticker(self, symbol = None):
        url = self.baseUrl + '/fapi/v1/price'
        
        builder=Builder()
        
        if(symbol is not None):
            builder.put_url("symbol",symbol)
        
        resp = requests.get(url, params = builder.build_url())
        
        if(resp.status_code == 200):
            obj = json.loads(resp.text)
            resp.close()
            return obj
        else:
            print(resp.status_code)
            print(resp.text)
        return None
    
    #Symbol Order Book Ticker
    def Symbol_Order_Book_Ticker(self, symbol = None):
        url = self.baseUrl + '/fapi/v1/bookTicker'
        
        builder=Builder()
        
        if(symbol is not None):
            builder.put_url("symbol",symbol)
        
        resp = requests.get(url, params = builder.build_url())
        
        if(resp.status_code == 200):
            obj = json.loads(resp.text)
            resp.close()
            return obj
        else:
            print(resp.status_code)
            print(resp.text)
        return None
    
    #Open Interest
    def Open_Interest(self, symbol = None):
        url = self.baseUrl + '/fapi/v1/openInterest'
        
        builder=Builder()
        
        builder.put_url("symbol",symbol)
        
        resp = requests.get(url, params = builder.build_url())
        
        if(resp.status_code == 200):
            obj = json.loads(resp.text)
            resp.close()
            return obj
        else:
            print(resp.status_code)
            print(resp.text)
        return None
    
    #Open Interest Statistics
    def Open_Interest_Statistics(self, symbol = None, period = None, limit = None, startTime = None, endTime = None):
        url = self.baseUrl + '/fapi/v1/openInterestHist'
        
        builder=Builder()
        
        builder.put_url("symbol", symbol)
        builder.put_url("period", period)
        if(startTime is not None):
            builder.put_url("startTime", startTime)
        if(endTime is not None):
            builder.put_url("endTime", endTime)
        if(limit is not None):
            builder.put_url("limit", limit)
        
        resp = requests.get(url, params = builder.build_url())
        
        if(resp.status_code == 200):
            obj = json.loads(resp.text)
            resp.close()
            return obj
        else:
            print(resp.status_code)
            print(resp.text)
        return None
    
    #Top Trader Long/Short Ratio (Accounts)
    def Top_Trader_Long_Short_Ratio_Accounts(self, symbol = None, period = None, limit = None, startTime = None, endTime = None):
        url = self.baseUrl + '/fapi/v1/topLongShortAccountRatio'
        
        builder=Builder()
        
        builder.put_url("symbol", symbol)
        builder.put_url("period", period)
        if(startTime is not None):
            builder.put_url("startTime", startTime)
        if(endTime is not None):
            builder.put_url("endTime", endTime)
        if(limit is not None):
            builder.put_url("limit", limit)
        
        resp = requests.get(url, params = builder.build_url())
        
        if(resp.status_code == 200):
            obj = json.loads(resp.text)
            resp.close()
            return obj
        else:
            print(resp.status_code)
            print(resp.text)
        return None
    
    #Top Trader Long/Short Ratio (Positions)
    def Top_Trader_Long_Short_Ratio_Accounts(self, symbol = None, period = None, limit = None, startTime = None, endTime = None):
        url = self.baseUrl + '/fapi/v1/topLongShortPositionRatio'
        
        builder=Builder()
        
        builder.put_url("symbol", symbol)
        builder.put_url("period", period)
        if(startTime is not None):
            builder.put_url("startTime", startTime)
        if(endTime is not None):
            builder.put_url("endTime", endTime)
        if(limit is not None):
            builder.put_url("limit", limit)
        
        resp = requests.get(url, params = builder.build_url())
        
        if(resp.status_code == 200):
            obj = json.loads(resp.text)
            resp.close()
            return obj
        else:
            print(resp.status_code)
            print(resp.text)
        return None
    
    #Long/Short Ratio
    def Long_Short_Ratio(self, symbol = None, period = None, limit = None, startTime = None, endTime = None):
        url = self.baseUrl + '/fapi/v1/globalLongShortAccountRatio'
        
        builder=Builder()
        
        builder.put_url("symbol", symbol)
        builder.put_url("period", period)
        if(startTime is not None):
            builder.put_url("startTime", startTime)
        if(endTime is not None):
            builder.put_url("endTime", endTime)
        if(limit is not None):
            builder.put_url("limit", limit)
        
        resp = requests.get(url, params = builder.build_url())
        
        if(resp.status_code == 200):
            obj = json.loads(resp.text)
            resp.close()
            return obj
        else:
            print(resp.status_code)
            print(resp.text)
        return None
    
    #Taker Buy_Sell Volume
    def Taker_Buy_Sell_Volume(self, symbol = None, period = None, limit = None, startTime = None, endTime = None):
        url = self.baseUrl + '/fapi/v1/takerlongshortRatio'
        
        builder=Builder()
        
        builder.put_url("symbol", symbol)
        builder.put_url("period", period)
        if(startTime is not None):
            builder.put_url("startTime", startTime)
        if(endTime is not None):
            builder.put_url("endTime", endTime)
        if(limit is not None):
            builder.put_url("limit", limit)
        
        resp = requests.get(url, params = builder.build_url())
        
        if(resp.status_code == 200):
            obj = json.loads(resp.text)
            resp.close()
            return obj
        else:
            print(resp.status_code)
            print(resp.text)
        return None
    
    #Historical_BLVT_NAV_Kline
    def Historical_BLVT_NAV_Kline(self, symbol = None, interval = None, limit = None, startTime = None, endTime = None):
        url = self.baseUrl + '/fapi/v1/lvtKlines'
        
        builder=Builder()
        
        builder.put_url("symbol", symbol)
        builder.put_url("interval", interval)
        if(startTime is not None):
            builder.put_url("startTime", startTime)
        if(endTime is not None):
            builder.put_url("endTime", endTime)
        if(limit is not None):
            builder.put_url("limit", limit)
        
        resp = requests.get(url, params = builder.build_url())
        
        if(resp.status_code == 200):
            obj = json.loads(resp.text)
            resp.close()
            return obj
        else:
            print(resp.status_code)
            print(resp.text)
        return None
    
    #Composite Index Symbol Information
    def Composite_Index_Symbol_Information(self, symbol = None):
        url = self.baseUrl + '/fapi/v1/indexInfo'
        
        builder=Builder()
        
        if(symbol is not None):
            builder.put_url("symbol", symbol)
        
        resp = requests.get(url, params = builder.build_url())
        
        if(resp.status_code == 200):
            obj = json.loads(resp.text)
            resp.close()
            return obj
        else:
            print(resp.status_code)
            print(resp.text)
        return None
    
    #Multi-Assets Mode Asset Index
    def Multi_Assets_Mode_Asset_Index(self, symbol = None):
        url = self.baseUrl + '/fapi/v1/assetIndex'
        
        builder=Builder()
        
        if(symbol is not None):
            builder.put_url("symbol", symbol)
        
        resp = requests.get(url, params = builder.build_url())
        
        if(resp.status_code == 200):
            obj = json.loads(resp.text)
            resp.close()
            return obj
        else:
            print(resp.status_code)
            print(resp.text)
        return None
    
    
#Account/Trades Endpoints

    #Change_Position_Mode(TRADE)
    def Change_Position_Mode(self, dualSidePosition = None, recvWindow = None):
        params = dict()
        
        params['dualSidePosition'] = dualSidePosition
        params['timestamp'] = self.get_ts()
        if(recvWindow is not None):
            params['recvWindow'] = recvWindow
        params['signature'] = self.__signature(params)
        
        obj = self.sendCmd(type='POST', url = '/fapi/v1/positionSide/dual', params = params)
        return obj

    #Get_Current_Position_Mode
    def Get_Current_Position_Mode(self, recvWindow = None):
        params = dict()
        
        if(recvWindow is not None):
            params['recvWindow'] = self.hashing(recvWindow)
        params['timestamp'] = self.get_ts()
        params['signature'] = self.__signature(params)
        
        obj = self.sendCmd(type='GET', url = '/fapi/v1/positionSide/dual', params = params)
        return obj
    
    #Change Multi-Assets Mode
    def Change_Multi_Assets_Mode(self, multiAssetsMargin = None, recvWindow = None):
        params = dict()
        
        params['multiAssetsMargin'] = multiAssetsMargin
        params['timestamp'] = self.get_ts()
        if(recvWindow is not None):
            params['recvWindow'] = recvWindow
        params['signature'] = self.__signature(params)
        
        obj = self.sendCmd(type='POST', url = '/fapi/v1/positionSide/multiAssetsMargin', params = params)
        return obj
    
    #Get Multi-Assets Mode
    def Get_Multi_Assets_Mode(self, recvWindow = None):
        params = dict()
        
        params['timestamp'] = self.get_ts()
        if(recvWindow is not None):
            params['recvWindow'] = recvWindow
        params['signature'] = self.__signature(params)
        
        obj = self.sendCmd(type='GET', url = '/fapi/v1/positionSide/multiAssetsMargin', params = params)
        return obj
    
    #New Oreder
    def Order(self, symbol = None, side = None, positionSide = None, type = None, timeInForce = None, quantity = None, reduceOnly = None, price = None, newClientOrderId = None, stopPrice = None, closePosition = None, activationPrice = None, callbackRate = None, workingType = None, priceProtect = None, newOrderRespType = None, recvWindow = None):
        params = dict()
        
        params['timestamp'] = self.get_ts()
        params['symbol'] = symbol
        params['side'] = side
        params['type'] = type
        if(positionSide is not None):
            params['positionSide'] = positionSide
        if(timeInForce is not None):
            params['timeInForce'] = timeInForce
        if(quantity is not None):
            params['quantity'] = quantity
        if(reduceOnly is not None):
            params['reduceOnly'] = reduceOnly
        if(price is not None):
            params['price'] = price
        if(newClientOrderId is not None):
            params['newClientOrderId'] = newClientOrderId
        if(stopPrice is not None):
            params['stopPrice'] = stopPrice
        if(closePosition is not None):
            params['closePosition'] = closePosition
        if(activationPrice is not None):
            params['activationPrice'] = activationPrice
        if(callbackRate is not None):
            params['callbackRate'] = callbackRate
        if(workingType is not None):
            params['workingType'] = workingType
        if(priceProtect is not None):
            params['priceProtect'] = priceProtect
        if(newOrderRespType is not None):
            params['newOrderRespType'] = newOrderRespType
        if(recvWindow is not None):
            params['recvWindow'] = recvWindow    
        params['signature'] = self.__signature(params)
        
        obj = self.sendCmd(type='POST', url = '/fapi/v1/order', params = params)
        return obj
    
    #Place Multiple Orders
    def Multiple_Order(self, symbol = None, side = None, positionSide = None, type = None, timeInForce = None, quantity = None, reduceOnly = None, price = None, newClientOrderId = None, stopPrice = None, activationPrice = None, callbackRate = None, workingType = None, priceProtect = None, newOrderRespType = None, batchOrders = None, recvWindow = None):
        params = dict()
        
        params['timestamp'] = self.get_ts()
        params['batchOrders'] = batchOrders
        params['symbol'] = symbol
        params['side'] = side
        params['type'] = type
        if(positionSide is not None):
            params['positionSide'] = positionSide
        if(timeInForce is not None):
            params['timeInForce'] = timeInForce
        if(quantity is not None):
            params['quantity'] = quantity
        if(reduceOnly is not None):
            params['reduceOnly'] = reduceOnly
        if(price is not None):
            params['price'] = price
        if(newClientOrderId is not None):
            params['newClientOrderId'] = newClientOrderId
        if(stopPrice is not None):
            params['stopPrice'] = stopPrice
        if(activationPrice is not None):
            params['activationPrice'] = activationPrice
        if(callbackRate is not None):
            params['callbackRate'] = callbackRate
        if(workingType is not None):
            params['workingType'] = workingType
        if(priceProtect is not None):
            params['priceProtect'] = priceProtect
        if(newOrderRespType is not None):
            params['newOrderRespType'] = newOrderRespType
        if(recvWindow is not None):
            params['recvWindow'] = recvWindow    
        params['signature'] = self.__signature(params)
        
        obj = self.sendCmd(type='POST', url = '/fapi/v1/batchOrders', params = params)
        return obj
     
    #Query Order
    def Query_Order(self, orderId = None, symbol = None, origClientOrderId = None, recvWindow = None):
        params = dict()
        
        params['timestamp'] = self.get_ts()
        params['symbol'] = symbol
        if(recvWindow is not None):
            params['recvWindow'] = recvWindow   
        if(orderId is not None):
            params['orderId'] = orderId 
        if(origClientOrderId is not None):
            params['origClientOrderId'] = origClientOrderId   
        params['signature'] = self.__signature(params)
        
        obj = self.sendCmd(type='GET', url = '/fapi/v1/order', params = params)
        return obj
    
    #Cancel Order
    def Cancel_Order(self, orderId = None, symbol = None, origClientOrderId = None, recvWindow = None):
        params = dict()
        
        params['timestamp'] = self.get_ts()
        params['symbol'] = symbol
        if(recvWindow is not None):
            params['recvWindow'] = recvWindow   
        if(orderId is not None):
            params['orderId'] = orderId 
        if(origClientOrderId is not None):
            params['origClientOrderId'] = origClientOrderId   
        params['signature'] = self.__signature(params)
        
        obj = self.sendCmd(type='DELETE', url = '/fapi/v1/order', params = params)
        return obj
    
    #Cancel All Open Orders
    def Cancel_All_Open_Orders(self, symbol = None, recvWindow = None):
        params = dict()
        
        params['timestamp'] = self.get_ts()
        params['symbol'] = symbol
        if(recvWindow is not None):
            params['recvWindow'] = recvWindow
        params['signature'] = self.__signature(params)
        
        obj = self.sendCmd(type='DELETE', url = '/fapi/v1/allOpenOrders', params = params)
        return obj
    
    #Cancel Multiple Orders 
    def Cancel_Multiple_Orders(self, symbol = None, orderIdList = None, origClientOrderIdList = None, recvWindow = None):
        params = dict()
        
        params['timestamp'] = self.get_ts()
        params['symbol'] = symbol
        if(recvWindow is not None):
            params['recvWindow'] = recvWindow
        if(orderIdList is not None):
            params['orderIdList'] = orderIdList
        if(origClientOrderIdList is not None):
            params['origClientOrderIdList'] = origClientOrderIdList
        params['signature'] = self.__signature(params)
        
        obj = self.sendCmd(type='DELETE', url = '/fapi/v1/batchOrders', params = params)
        return obj
    
    #Auto-Cancel All Open Orders
    def Auto_Cancel_All_Open_Orders(self, symbol = None, countdownTime = None, recvWindow = None):
        params = dict()
        
        params['timestamp'] = self.get_ts()
        params['symbol'] = symbol
        params['countdownTime'] = countdownTime
        if(recvWindow is not None):
            params['recvWindow'] = recvWindow
        params['signature'] = self.__signature(params)
        
        obj = self.sendCmd(type='POST', url = '/fapi/v1/countdownCancelAll', params = params)
        return obj
    
    #Query Current Open Order
    def Query_Current_Open_Order(self, symbol = None,  orderId = None, origClientOrderId = None, recvWindow = None):
        params = dict()
        
        params['timestamp'] = self.get_ts()
        params['symbol'] = symbol
        if(recvWindow is not None):
            params['recvWindow'] = recvWindow
        if(recvWindow is not None):
            params['orderId'] = orderId
        if(origClientOrderId is not None):
            params['origClientOrderId'] = origClientOrderId
        params['signature'] = self.__signature(params)
        
        obj = self.sendCmd(type='GET', url = '/fapi/v1/openOrder', params = params)
        return obj
    
    #Current All Open Orders
    def Current_All_Open_Orders(self, symbol = None, recvWindow = None):
        params = dict()
        
        params['timestamp'] = self.get_ts()
        params['symbol'] = symbol
        if(recvWindow is not None):
            params['recvWindow'] = recvWindow
        params['signature'] = self.__signature(params)
        
        obj = self.sendCmd(type='GET', url = '/fapi/v1/openOrders', params = params)
        return obj
    
    #All Orders (USER_DATA)
    def All_Ordersdef(self, symbol = None, orderId = None, startTime = None, endTime = None, limit = None, recvWindow = None):
        params = dict()
        
        params['timestamp'] = self.get_ts()
        params['symbol'] = symbol
        if(recvWindow is not None):
            params['recvWindow'] = recvWindow
        if(orderId is not None):
            params['orderId'] = orderId
        if(startTime is not None):
            params['startTime'] = startTime
        if(endTime is not None):
            params['endTime'] = endTime
        if(limit is not None):
            params['limit'] = limit
        params['signature'] = self.__signature(params)
        
        obj = self.sendCmd(type='GET', url = '/fapi/v1/allOrders', params = params)
        return obj
    
    #Futures Account Balance V2 (USER_DATA)
    def Futures_Account_Balance_V2(self, recvWindow = None):
        params = dict()
        
        params['timestamp'] = self.get_ts()
        if(recvWindow is not None):
            params['recvWindow'] = recvWindow
        params['signature'] = self.__signature(params)
        
        obj = self.sendCmd(type='GET', url = '/fapi/v2/balance', params = params)
        return obj
    
    #Account Information V2 (USER_DATA)
    def Account_Information_V2(self, recvWindow = None):
        params = dict()
        
        params['timestamp'] = self.get_ts()
        if(recvWindow is not None):
            params['recvWindow'] = recvWindow
        params['signature'] = self.__signature(params)
        
        obj = self.sendCmd(type='GET', url = '/fapi/v2/account', params = params)
        return obj
    
    #Change Initial Leverage (TRADE)
    def Change_Initial_Leverage(self, symbol = None, leverage = None, recvWindow = None):
        params = dict()
        
        params['timestamp'] = self.get_ts()
        params['symbol'] = symbol
        params['leverage'] = leverage
        if(recvWindow is not None):
            params['recvWindow'] = recvWindow
        params['signature'] = self.__signature(params)
        
        obj = self.sendCmd(type='POST', url = '/fapi/v1/leverage', params = params)
        return obj
    
    #Change Margin Type (TRADE)
    def Change_Margin_Type(self, symbol = None, marginType = None, recvWindow = None):
        params = dict()
        
        params['timestamp'] = self.get_ts()
        params['symbol'] = symbol
        params['marginType'] = marginType
        if(recvWindow is not None):
            params['recvWindow'] = recvWindow
        params['signature'] = self.__signature(params)
        
        obj = self.sendCmd(type='POST', url = '/fapi/v1/marginType', params = params)
        return obj
    
    #Get Position Margin Change History (TRADE)
    def Get_Position_Margin_Change_History(self, symbol = None, type = None, startTime = None, endTime = None, limit = None, recvWindow = None):
        params = dict()
        
        params['timestamp'] = self.get_ts()
        params['symbol'] = symbol
        if(recvWindow is not None):
            params['recvWindow'] = recvWindow
        if(type is not None):
            params['type'] = type
        if(startTime is not None):
            params['startTime'] = startTime
        if(endTime is not None):
            params['endTime'] = endTime
        if(limit is not None):
            params['limit'] = limit
        params['signature'] = self.__signature(params)
        
        obj = self.sendCmd(type='GET', url = '/fapi/v1/positionMargin/history', params = params)
        return obj
    
    #Position Information V2 (USER_DATA)
    def Position_Information_V2(self, symbol = None, recvWindow = None):
        params = dict()
        
        params['timestamp'] = self.get_ts()
        if(symbol is not None):
            params['symbol'] = symbol
        if(recvWindow is not None):
            params['recvWindow'] = recvWindow
        params['signature'] = self.__signature(params)
        
        obj = self.sendCmd(type='GET', url = '/fapi/v2/positionRisk', params = params)
        return obj
    
    #Account Trade List (USER_DATA)
    def Account_Trade_List(self, symbol = None, fromId = None, startTime = None, endTime = None, limit = None, recvWindow = None):
        params = dict()
        
        params['timestamp'] = self.get_ts()
        params['symbol'] = symbol
        if(recvWindow is not None):
            params['recvWindow'] = recvWindow
        if(fromId is not None):
            params['fromId'] = fromId
        if(startTime is not None):
            params['startTime'] = startTime
        if(endTime is not None):
            params['endTime'] = endTime
        if(limit is not None):
            params['limit'] = limit
        params['signature'] = self.__signature(params)
        
        obj = self.sendCmd(type='GET', url = '/fapi/v1/userTrades', params = params)
        return obj
    
    #Get Income History (USER_DATA)
    def Get_Income_History(self, symbol = None , incomeType = None, startTime = None, endTime = None, limit = None, recvWindow = None):
        params = dict()
        
        params['timestamp'] = self.get_ts()
        if(symbol is not None):
            params['symbol'] = symbol
        if(recvWindow is not None):
            params['recvWindow'] = recvWindow
        if(incomeType is not None):
            params['incomeType'] = incomeType
        if(startTime is not None):
            params['startTime'] = startTime
        if(endTime is not None):
            params['endTime'] = endTime
        if(limit is not None):
            params['limit'] = limit
        params['signature'] = self.__signature(params)
        
        obj = self.sendCmd(type='GET', url = '/fapi/v1/income', params = params)
        return obj
    
    #Notional and Leverage Brackets (USER_DATA)
    def Notional_and_Leverage_Brackets(self, symbol = None, recvWindow = None):
        params = dict()
        
        params['timestamp'] = self.get_ts()
        if(symbol is not None):
            params['symbol'] = symbol
        if(recvWindow is not None):
            params['recvWindow'] = recvWindow
        params['signature'] = self.__signature(params)
        
        obj = self.sendCmd(type='GET', url = '/fapi/v1/leverageBracket', params = params)
        return obj
    
    #Position ADL Quantile Estimation (USER_DATA)
    def Position_ADL_Quantile_Estimation(self, symbol = None, recvWindow = None):
        params = dict()
        
        params['timestamp'] = self.get_ts()
        if(symbol is not None):
            params['symbol'] = symbol
        if(recvWindow is not None):
            params['recvWindow'] = recvWindow
        params['signature'] = self.__signature(params)
        
        obj = self.sendCmd(type='GET', url = '/fapi/v1/adlQuantile', params = params)
        return obj
    
    #User's Force Orders (USER_DATA)
    def User_Force_Orders(self, symbol = None, autoCloseType = None, startTime = None, endTime = None, limit = None, recvWindow = None):
        params = dict()
        
        params['timestamp'] = self.get_ts()
        if(symbol is not None):
            params['symbol'] = symbol
        if(recvWindow is not None):
            params['recvWindow'] = recvWindow
        if(autoCloseType is not None):
            params['autoCloseType'] = autoCloseType
        if(startTime is not None):
            params['startTime'] = startTime
        if(endTime is not None):
            params['endTime'] = endTime
        if(limit is not None):
            params['limit'] = limit
        params['signature'] = self.__signature(params)
        
        obj = self.sendCmd(type='GET', url = '/fapi/v1/forceOrders', params = params)
        return obj
    
    #Futures Trading Quantitative Rules Indicators (USER_DATA)
    def Futures_Trading_Quantitative_Rules_Indicators(self, symbol = None, recvWindow = None):
        params = dict()
        
        params['timestamp'] = self.get_ts()
        if(symbol is not None):
            params['symbol'] = symbol
        if(recvWindow is not None):
            params['recvWindow'] = recvWindow
        params['signature'] = self.__signature(params)
        
        obj = self.sendCmd(type='GET', url = '/fapi/v1/apiTradingStatus', params = params)
        return obj
    
    #User Commission Rate (USER_DATA)
    def User_Commission_Rate(self, symbol = None, recvWindow = None):
        params = dict()
        
        params['timestamp'] = self.get_ts()
        params['symbol'] = symbol
        if(recvWindow is not None):
            params['recvWindow'] = recvWindow
        params['signature'] = self.__signature(params)
        
        obj = self.sendCmd(type='GET', url = '/fapi/v1/commissionRate', params = params)
        return obj
    
    #Get Download Id For Futures Transaction History (USER_DATA)
    def Get_Download_Id_For_Futures_Transaction_History(self, startTime = None, endTime = None, recvWindow = None):
        params = dict()
        
        params['timestamp'] = self.get_ts()
        params['startTime'] = startTime
        params['endTime'] = endTime
        if(recvWindow is not None):
            params['recvWindow'] = recvWindow
        params['signature'] = self.__signature(params)
        
        obj = self.sendCmd(type='GET', url = '/fapi/v1/income/asyn', params = params)
        return obj
    
    #Get Futures Transaction History Download Link by Id (USER_DATA)
    def Get_Futures_Transaction_History_Download_Link_by_Id(self, downloadId = None, recvWindow = None):
        params = dict()
        
        params['timestamp'] = self.get_ts()
        params['downladId'] = downloadId
        if(recvWindow is not None):
            params['recvWindow'] = recvWindow
        params['signature'] = self.__signature(params)
        
        obj = self.sendCmd(type='GET', url = '/fapi/v1/income/asyn/id', params = params)
        return obj

#User Data Streams
    #Start User Data Stream (USER_STREAM)
    def Start_User_Data_Stream(self):
        params = dict()
        
        obj = self.sendCmd(type='POST', url = '/fapi/v1/listenKey', params = params)
        return obj
    
    #Keepalive User Data Stream (USER_STREAM)
    def Keepalive_User_Data_Stream(self):
        params = dict()
        
        obj = self.sendCmd(type='PUT', url = '/fapi/v1/listenKey', params = params)
        return obj
    
    #Close User Data Stream (USER_STREAM)
    def Close_User_Data_Stream(self):
        params = dict()
        
        obj = self.sendCmd(type='DELETE', url = '/fapi/v1/listenKey', params = params)
        return obj
    #Connect To User Data Stream
    def Connect_To_User_Data_Stream(self):
        listenKey = self.Start_User_Data_Stream()['listenKey']
        
        self.connect(listenKey)
        
        self.Close_User_Data_Stream()
        return None
    