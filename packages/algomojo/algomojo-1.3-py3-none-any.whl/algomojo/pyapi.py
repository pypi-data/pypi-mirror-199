# -*- coding: utf-8 -*-
"""
Rest API Documentation
    https://amapi.algomojo.com/v1/docs/
"""

import requests
import json


class api:

    """
    A class Which has methods to handle all the api calls to algomojo

    """

    def __init__(self, api_key, api_secret, version="v1"):

        """
         Function used to initialize object of class api.
         ...

         Attributes
         ----------
         api_key : str
             User Api key (logon to algomojo account to find api credentials)
         api_secret : str
             User Api secret (logon to algomojo account to find api credentials)
         Broker : str
             This takes broker it generally consists 2 letters , EX: alice blue--> AB, tradejini-->TC, zebu-->ZB

         ----------
         Example:
        test=api(api_key="20323f062bb71ca6fbb178b4df8ac5z6",api_secret="686786a302d7364d81badc233f1d22e3")
         """


        self.api_key = api_key.lower()
        self.api_secret = api_secret.lower()
        self.burl = "https://amapi.algomojo.com/" + str(version) + '/'
        self.headers = {
            'Content-Type': 'application/json'
        }
        
    def PlaceOrder(self,broker: str, exchange: str, symbol: str, action: str, product: str, quantity: int, pricetype: str = "MARKET",   strategy: str = "Python", price: float = 0, trigger_price: float = 0, disclosed_quantity: int = 0, amo: str = "NO", splitorder: str = "NO", split_quantity: int = 1, api_key: str = "default", api_secret: str = "default"):
        """This function places an order for the specified symbol on a specified exchange through the specified broker.

    Parameters:
        broker (str): The name of the broker short code. (e.g ab - aliceblue,an - angelone, fs - firstock, up- upstox, ze- zerodha ). Refer API Docs appendix for complete broker code
        exchange (str): The name of the exchange (NSE,NFO,BSE,BFO,MCX,CDS).
        symbol (str): The symbol for the order.
        action (str): The type of the order (e.g. "BUY", "SELL").
        product (str): The product type for the order (e.g. "CNC,MIS,NRML").
        quantity (int): The number of shares to be ordered.
        pricetype (str, optional): The type of the price (e.g. "MARKET,LIMIT,SL,SL-M"). Defaults to "MARKET".
        price (float, optional): The price of the order. Defaults to 0.
        disclosed_quantity (int, optional): The quantity to be disclosed in the order. Defaults to 0.
        strategy (str, optional): The trading strategy name. Defaults to "Python".
        trigger_price (float, optional): The trigger price for the order. Defaults to 0.
        amo (str, optional): The after market order  (e.g. "NO,YES"). Defaults to "NO".
        splitorder (str, optional): The split order  (e.g. "NO,YES"). Defaults to "NO".
        split_quantity (int, optional): The quantity to be split in the order. Defaults to 1. Set the value max to "Freeze quantity" to slice larger orders
        api_key (str, optional): The API key to use. Defaults to "default".
        api_secret (str, optional): The API secret to use. Defaults to "default".

    Returns:
        dict: A dictionary containing the order response from the Broker.
    """
        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        data = {
            "api_key":api_key,
            "api_secret":api_secret,
            "data":{    
                          "broker":broker,
                          "strategy":strategy,
                          "exchange":exchange,
                          "symbol":symbol,
                          "action":action,
                          "product":product,
                          "pricetype":pricetype,
                          "quantity":str(quantity),
                          "price":str(price),
                          "disclosed_quantity":str(disclosed_quantity),
                          "trigger_price":str(trigger_price), 
                          "amo":amo,
                          "splitorder":splitorder,
                          "split_quantity":str(split_quantity)
                   }
            } 
        url = self.burl + "PlaceOrder"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())
    
    def PlaceBOOrder(self,broker: str,exchange: str,symbol: str,action: str, quantity: int,price: float ,squareoff: float ,stoploss: float ,trailing_stoploss: float ,strategy: str ="Python", pricetype: str = "MARKET", disclosed_quantity: int =0,trigger_price: float = 0, api_key: str ="default", api_secret: str ="default"):
        """ This function places a bracket order for a given stock symbol with the specified broker.

    Parameters:
    broker (str): The name of the broker short code. (e.g ab - aliceblue,an - angelone, fs - firstock, up- upstox, ze- zerodha ). Refer API Docs appendix for complete broker code
    exchange (str): The name of the exchange (NSE,NFO,BSE,BFO,MCX,CDS).
    symbol (str): The symbol for the order.
    action (str): The type of the order (e.g. "BUY", "SELL").
    pricetype (str, optional): The type of the price (e.g. "MARKET,LIMIT,SL,SL-M"). Defaults to "MARKET".
    quantity (int) : Number of stocks to order.
    price (float, optional): The price of the order. Defaults to 0.
    squareoff (float) : Price at which to square off the order.
    stoploss (float) : Price at which to trigger the stop loss.
    trailing_stoploss (float, optional): Price at which to trigger the trailing stop loss.
    strategy (str, optional) : Name of the trading strategy to use, default is "Python".
    disclosed_quantity (int, optional) : Number of stocks to disclose for the order, default is 0.
    trigger_price (float, optional) : Trigger price for the order, default is 0.
    api_key (str, optional) : API key for accessing the broker's trading API, default is "default".
    api_secret (str, optional) : API secret for accessing the broker's trading API, default is "default".

    Returns:
        dict: A dictionary containing the order response from the Broker.
    """
        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        data = {
            "api_key": api_key,
            "api_secret": api_secret,
            "data":
                {
                "broker":broker,
                "strategy":strategy,
                "exchange":exchange,
                "symbol":symbol,
                "action":action,
                "pricetype":pricetype,
                "quantity":str(quantity),
                "price":str(price),
                "squareoff":str(squareoff),
                "stoploss":str(stoploss),
                "trailing_stoploss":str(trailing_stoploss),
                "trigger_price":str(trigger_price), 
                "disclosed_quantity":str(disclosed_quantity)
                }
        }
        url = self.burl + "PlaceBOOrder"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())

      
        
    def PlaceCOOrder(self,broker: str,exchange: str,symbol: str,action: str,quantity: int,price: float, stop_price: float,strategy:str ="Python", pricetype: str = "MARKET", api_key:str ="default", api_secret:str ="default"):
        
        """ This function places a cover order for a given stock symbol with the specified broker.

    Parameters:
    broker (str): The name of the broker short code. (e.g ab - aliceblue,an - angelone, fs - firstock, up- upstox, ze- zerodha ). Refer API Docs appendix for complete broker code
    exchange (str): The name of the exchange (NSE,NFO,BSE,BFO,MCX,CDS).
    symbol (str): The symbol for the order.
    action (str): The type of the order (e.g. "BUY", "SELL").
    pricetype (str, optional): The type of the price (e.g. "MARKET,LIMIT,SL,SL-M"). Defaults to "MARKET".
    quantity (int) : Number of stocks to order.
    price (float, optional): The price of the order. Defaults to 0.
    stop_price (float) : Price at which to trigger the stop loss.
    strategy (str, optional) : Name of the trading strategy to use, default is "Python".
    api_key (str, optional) : API key for accessing the broker's trading API, default is "default".
    api_secret (str, optional) : API secret for accessing the broker's trading API, default is "default".

    Returns:
        dict: A dictionary containing the order response from the Broker.
    """

        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        data = {
            "api_key": api_key,
            "api_secret": api_secret,
            "data":
                {
                  "broker":broker,
                  "strategy":strategy,
                  "exchange":exchange,
                  "symbol":symbol,
                  "action":action,
                  "pricetype":pricetype,
                  "quantity":str(quantity),
                  "price":str(price),
                  "stop_price":str(stop_price),
                }
        }
        url = self.burl + "PlaceCOOrder"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())

    def PlaceFOOptionsOrder(self, broker: str, spot_symbol: str, expiry_date: str, action: str, product: str, quantity: int, option_type: str, strike_int: int, offset: int, strategy: str = "Python", pricetype: str="MARKET", price: float = 0, splitorder: str = "NO", split_quantity: int = 1, api_key: str = "default", api_secret: str = "default"):

        """ This function places a futre options order for a given stock symbol with the specified broker.
    
    Parameters
    ----------
    broker (str): The name of the broker short code. (e.g ab - aliceblue,an - angelone, fs - firstock, up- upstox, ze- zerodha ). Refer API Docs appendix for complete broker code
    spot_symbol(str): The symbol of the underlying stock.
    expiry_date(str): The expiry date of the option in the format "YYYY-MM-DD".
    action(str): The action to be taken (e.g. "BUY", "SELL").
    product(str): The type of product The product type for the order (e.g. "CNC,MIS,NRML").
    pricetype(str): The type of price (e.g. "MARKET,LIMIT,SL,SL-M"). Defaults to "MARKET".
    quantity(int): Number of stocks to order.
    option_type(str): The type of option (e.g. "CE" , "PE").
    strike_int(int): The strike price of the option.
    offset(int): The offset value for the price.
    strategy(str, optional):The name of the strategy to be used, Defaults to "Python".
    price(float, optional): The price for the trade, Defaults to 0.
    splitorder (str, optional): The split order  (e.g. "NO,YES"). Defaults to "NO".
    split_quantity (int, optional): The quantity to be split in the order. Defaults to 1. Set the value max to "Freeze quantity" to slice larger orders
    api_key (str, optional): The API key to use. Defaults to "default".
    api_secret (str, optional): The API secret to use. Defaults to "default".
    
    Returns:
        dict: A dictionary containing the order response from the Broker.
    """
        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        data = {
            "api_key": api_key,
            "api_secret": api_secret,
            "data": {
                "broker": broker,
                "strategy": strategy,
                "spot_symbol": spot_symbol,
                "expiry_date": expiry_date,
                "action": action,
                "product": product,
                "pricetype": pricetype,
                "quantity": str(quantity),
                "price": str(price),
                "option_type": option_type,
                "strike_int": str(strike_int),
                "offset": str(offset),
                "splitorder": splitorder,
                "split_quantity": split_quantity
            }
        }
        url = self.burl + "PlaceFOOptionsOrder"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())


    def PlaceSmartOrder(self, broker: str, exchange: str, symbol: str, action: str, product: str,  quantity: int,  position_size: int, strategy: str = "Python", pricetype: str="MARKET", disclosed_quantity: int=0, price: float=0, trigger_price: float=0, amo: str="NO", splitorder: str="NO", split_quantity: int=1, api_key: str="default", api_secret: str="default"):
       
        """ This function places a smartorder for a given stock symbol with the specified broker.
    
    Parameters
    ----------
    broker (str): The name of the broker short code. (e.g ab - aliceblue,an - angelone, fs - firstock, up- upstox, ze- zerodha ). Refer API Docs appendix for complete broker code
    exchange (str): The name of the exchange (NSE,NFO,BSE,BFO,MCX,CDS).
    symbol (str): The symbol for the order.
    action (str): The type of the order (e.g. "BUY", "SELL").
    pricetype (str, optional): The type of the price (e.g. "MARKET,LIMIT,SL,SL-M"). Defaults to "MARKET".
    quantity (int) : Number of stocks to order.
    price (float, optional): The price of the order. Defaults to 0.
    position_size (int) : size of the position to trade
    disclosed_quantity (int, optional) : quantity to be disclosed . Defaults to 0.
    trigger_price (float, optional) : trigger price for the order. Defaults to 0.
    amo (str, optional) : "YES" or "NO", whether to place the order as AMO .Defaults to "NO".
    splitorder (str, optional): The split order  (e.g. "NO,YES"). Defaults to "NO".
    split_quantity (int, optional): The quantity to be split in the order. Defaults to 1. Set the value max to "Freeze quantity" to slice larger orders
    strategy (str, optional) : Name of the trading strategy to use, default is "Python".
    api_key (str, optional): The API key to use. Defaults to "default".
    api_secret (str, optional): The API secret to use. Defaults to "default".
    
    Returns:
        dict: A dictionary containing the order response from the Broker.
    """
        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        data = {
            "api_key": api_key,
            "api_secret": api_secret,
            "data": {
                "broker": broker,
                "strategy": strategy,
                "exchange": exchange,
                "symbol": symbol,
                "action": action,
                "product": product,
                "pricetype": pricetype,
                "quantity": str(quantity),
                "price": str(price),
                "position_size": str(position_size),
                "trigger_price": str(trigger_price),
                "disclosed_quantity": str(disclosed_quantity),
                "amo": amo,
                "splitorder": splitorder,
                "split_quantity": str(split_quantity)
            }
        } 
        url = self.burl + "PlaceSmartOrder"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())

    
    def PlaceStrategyOrder(self, strategy_id: int, action: str, api_key: str = "default", api_secret: str = "default"):
        
        """ This function places a strategy order with the specified broker.
    
    Parameters
    ----------
    strategy_id (int) : ID of the strategy.
    action (str): The type of the order (e.g. "BUY", "SELL").
    api_key (str, optional): The API key to use. Defaults to "default".
    api_secret (str, optional): The API secret to use. Defaults to "default".
    
    Returns:
        dict: A dictionary containing the order response from the Broker.
    """
        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        data = {
            "api_key": api_key,
            "api_secret": api_secret,
            "data":
                {
                    "strategy_id": strategy_id,
                    "action": action
                }

        }
        url = self.burl + "PlaceStrategyOrder"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())


    def PlaceMultiOrder(self, order_list):

        """ This function places a muliple placeorder at once with the specified broker.
    
    Parameters
    ----------
    order_list (list): A list of dictionaries representing each order. Each dictionary should have the following keys:
        broker (str): The name of the broker short code. (e.g ab - aliceblue,an - angelone, fs - firstock, up- upstox, ze- zerodha ). Refer API Docs appendix for complete broker code
        strategy (str): The strategy to use for the order. Defaults to "Test" if not provided.
        exchange (str): The exchange to place the order on.
        symbol (str): The symbol to place the order for.
        action (str): The action for the order, e.g. "BUY" or "SELL".
        product (str): The product for the order, e.g. "CASH" or "MIS".
        pricetype (str): The price type for the order, e.g. "LIMIT" or "MARKET".
        quantity (str): The quantity for the order.
        price (str): The price for the order. Defaults to "0" if not provided.
        splitorder (str): Whether to split the order into multiple orders. Defaults to "NO" if not provided.
        split_quantity (str): The quantity to split the order into. Defaults to "1" if not provided.
        api_key (str): The API key for authentication. Defaults to `self.api_key` if not provided.
        api_secret (str): The API secret for authentication. Defaults to `self.api_secret` if not provided.

    Returns:
        dict: A dictionary containing the order response from the Broker.
    """

        l = order_list

        def rename(dictn, old, new):
            dictn[new] = dictn.pop(old)
            return dictn

        for i in range(len(l)):
            if "api_key" not in l[i].keys():
                l[i]["api_key"] = self.api_key
                l[i]["api_secret"] = self.api_secret
            if "strategy" not in l[i].keys():
                l[i]["strategy"] = "Test"
            if "splitorder" not in l[i].keys():
                l[i]["splitorder"] = "NO"
            if "price" not in l[i].keys():
                l[i]["price"] = "0"
            if "split_quantity" not in l[i].keys():
                l[i]["split_quantity"] = "1"

            l[i]["quantity"] = str(l[i]["quantity"])
            l[i]["price"] = str(l[i]["price"])
            l[i]["split_quantity"] = str(l[i]["split_quantity"])
            l[i] = rename(l[i], "api_key", "api_key")
            l[i] = rename(l[i], "api_secret", "api_secret")
            l[i] = rename(l[i], "broker", "broker")
            l[i] = rename(l[i], "symbol", "symbol")
            l[i] = rename(l[i], "exchange", "exchange")
            l[i] = rename(l[i], "action", "action")
            l[i] = rename(l[i], "product", "product")
            l[i] = rename(l[i], "pricetype", "pricetype")
            l[i] = rename(l[i], "splitorder", "splitorder")
            
            
        order_data=[]
        for i in l:
            apikeyy=i['api_key']
            apisecrett=i['api_secret']
            broker= i['broker']
            strategy=i['strategy']
            exchange=i['exchange']
            symbol=i['symbol']
            action=i['action']
            product=i['product']
            pricetype=i['pricetype']
            quantity=i['quantity']
            price=i['price']
            splitorder=i['splitorder']
            split_quantity=i['split_quantity']

            data_1={
                "api_key": apikeyy,
                "api_secret": apisecrett,
                "data":
                    {   "broker":broker,
                        "strategy":strategy,
                        "exchange":exchange,
                        "symbol":symbol,
                        "action":action,
                        "product":product,
                        "pricetype":pricetype,
                        "quantity":quantity,
                        "price":price,
                        "splitorder":splitorder,
                        "split_quantity":split_quantity
                       }
            }
            
            order_data.append(data_1)
            

        data = {
            "api_key": self.api_key,
            "api_secret": self.api_secret,
            "data":
                {
                    "orders": order_data   

                }
        }
        url = self.burl + "PlaceMultiOrder"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())

    def PlaceMultiBOOrder(self, order_list):

        """ This function places a muliple bracket order at once with the specified broker.
    
    Parameters
    ----------
    order_list (list): A list of dictionaries representing each order. Each dictionary should have the following keys:
        broker (str): The name of the broker short code. (e.g ab - aliceblue,an - angelone, fs - firstock, up- upstox, ze- zerodha ). Refer API Docs appendix for complete broker code
        exchange (str): The name of the exchange (NSE,NFO,BSE,BFO,MCX,CDS).
        symbol (str): The symbol for the order.
        action (str): The type of the order (e.g. "BUY", "SELL").
        pricetype (str, optional): The type of the price (e.g. "MARKET,LIMIT,SL,SL-M"). Defaults to "MARKET".
        quantity (int) : Number of stocks to order.
        price (float, optional): The price of the order. Defaults to 0.
        squareoff (float) : Price at which to square off the order.
        stoploss (float) : Price at which to trigger the stop loss.
        trailing_stoploss (float, optional): Price at which to trigger the trailing stop loss.
        strategy (str, optional) : Name of the trading strategy to use, default is "Python".
        disclosed_quantity (int, optional) : Number of stocks to disclose for the order, default is 0.
        trigger_price (float, optional) : Trigger price for the order, default is 0.
        api_key (str, optional) : API key for accessing the broker's trading API, default is "default".
        api_secret (str, optional) : API secret for accessing the broker's trading API, default is "default".

    Returns:
        dict: A dictionary containing the order response from the Broker.
    """

        l = order_list

        def rename(dictn, old, new):
            dictn[new] = dictn.pop(old)
            return dictn

        for i in range(len(l)):
            if "api_key" not in l[i].keys():
                l[i]["api_key"] = self.api_key
                l[i]["api_secret"] = self.api_secret
            if "strategy" not in l[i].keys():
                l[i]["strategy"] = "Test"
            if "trigger_price" not in l[i].keys():
                l[i]["trigger_price"] = "0"
            if "price" not in l[i].keys():
                l[i]["price"] = "0"
            if "disclosed_quantity" not in l[i].keys():
                l[i]["disclosed_quantity"] = "0"

            l[i]["quantity"] = str(l[i]["quantity"])
            l[i]["price"] = str(l[i]["price"])
            l[i]["squareoff"] = str(l[i]["squareoff"])
            l[i]["stoploss"] = str(l[i]["stoploss"])
            l[i]["trailing_stoploss"] = str(l[i]["trailing_stoploss"])
            l[i]["trigger_price"] = str(l[i]["trigger_price"])
            l[i]["disclosed_quantity"] = str(l[i]["disclosed_quantity"])
            l[i] = rename(l[i], "api_key", "api_key")
            l[i] = rename(l[i], "api_secret", "api_secret")
            l[i] = rename(l[i], "broker", "broker")
            l[i] = rename(l[i], "symbol", "symbol")
            l[i] = rename(l[i], "exchange", "exchange")
            l[i] = rename(l[i], "action", "action")
            l[i] = rename(l[i], "pricetype", "pricetype")
        
        order_data=[]
        for i in l:
            apikeyy=i['api_key']
            apisecrett=i['api_secret']
            broker= i['broker']
            strategy=i['strategy']
            exchange=i['exchange']
            symbol=i['symbol']
            action=i['action']
            pricetype=i['pricetype']
            quantity=i['quantity']
            price=i['price']
            squareoff=i['squareoff']
            stoploss=i['stoploss']
            trailing_stoploss=i['trailing_stoploss']
            trigger_price=i['trigger_price']
            disclosed_quantity=i['disclosed_quantity']
            
            data_1={
                "api_key": apikeyy,
                "api_secret": apisecrett,
                "data":
                    {   "broker":broker,
                        "strategy":strategy,
                        "exchange":exchange,
                        "symbol":symbol,
                        "action":action,
                        "pricetype":pricetype,
                        "quantity":quantity,
                        "price":price,
                        "squareoff":squareoff,
                        "stoploss":stoploss,
                        "trailing_stoploss":trailing_stoploss,
                        "trigger_price":trigger_price,
                        "disclosed_quantity":disclosed_quantity
                       }
            }
            
            order_data.append(data_1)
            

        data = {
            "api_key": self.api_key,
            "api_secret": self.api_secret,
            "data":
                {
                    "orders": order_data   

                }
        }
        url = self.burl + "PlaceMultiBOOrder"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())
    
    def PlaceMultiFOOptionsOrder(self, order_list):
        """ This function places a muliple future options order at once with the specified broker.
    
    Parameters
    ----------
    order_list (list): A list of dictionaries representing each order. Each dictionary should have the following keys:
        broker (str): The name of the broker short code. (e.g ab - aliceblue,an - angelone, fs - firstock, up- upstox, ze- zerodha ). Refer API Docs appendix for complete broker code
        spot_symbol(str): The symbol of the underlying stock.
        expiry_date(str): The expiry date of the option in the format "YYYY-MM-DD".
        action(str): The action to be taken (e.g. "BUY", "SELL").
        product(str): The type of product The product type for the order (e.g. "CNC,MIS,NRML").
        pricetype(str): The type of price (e.g. "MARKET,LIMIT,SL,SL-M"). Defaults to "MARKET".
        quantity(int): Number of stocks to order.
        option_type(str): The type of option (e.g. "CE" , "PE").
        strike_int(int): The strike price of the option.
        offset(int): The offset value for the price.
        strategy(str, optional):The name of the strategy to be used, Defaults to "Python".
        price(float, optional): The price for the trade, Defaults to 0.
        splitorder (str, optional): The split order  (e.g. "NO,YES"). Defaults to "NO".
        split_quantity (int, optional): The quantity to be split in the order. Defaults to 1. Set the value max to "Freeze quantity" to slice larger orders
        strategy (str, optional) : Name of the trading strategy to use, default is "Python".
        api_key (str, optional): The API key to use. Defaults to "default".
        api_secret (str, optional): The API secret to use. Defaults to "default".

    Returns:
        dict: A dictionary containing the order response from the Broker.
    """

        l = order_list

        def rename(dictn, old, new):
            dictn[new] = dictn.pop(old)
            return dictn

        for i in range(len(l)):
            if "api_key" not in l[i].keys():
                l[i]["api_key"] = self.api_key
                l[i]["api_secret"] = self.api_secret
            if "strategy" not in l[i].keys():
                l[i]["strategy"] = "Test"
            if "trigger_price" not in l[i].keys():
                l[i]["trigger_price"] = "0"
            if "splitorder" not in l[i].keys():
                l[i]["splitorder"] = "NO"
            if "price" not in l[i].keys():
                l[i]["price"] = "0"
            if "split_quantity" not in l[i].keys():
                l[i]["split_quantity"] = "1"
            if "disclosed_quantity" not in l[i].keys():
                l[i]["disclosed_quantity"] = "0"

            l[i]["quantity"] = str(l[i]["quantity"])
            l[i]["price"] = str(l[i]["price"])
            l[i]["strike_int"] = str(l[i]["strike_int"])
            l[i]["offset"] = str(l[i]["offset"])
            l[i]["split_quantity"] = str(l[i]["split_quantity"])
            l[i] = rename(l[i], "api_key", "api_key")
            l[i] = rename(l[i], "api_secret", "api_secret")
            l[i] = rename(l[i], "broker", "broker")
            l[i] = rename(l[i], "spot_symbol", "spot_symbol")
            l[i] = rename(l[i], "expiry_date", "expiry_date")
            l[i] = rename(l[i], "action", "action")
            l[i] = rename(l[i], "product", "product")
            l[i] = rename(l[i], "pricetype", "pricetype")
            l[i] = rename(l[i], "option_type", "option_type")
            l[i] = rename(l[i], "splitorder", "splitorder")
        
        order_data=[]
        for i in l:
            apikeyy=i['api_key']
            apisecrett=i['api_secret']
            broker= i['broker']
            strategy=i['strategy']
            spot_symbol=i['spot_symbol']
            expiry_date=i['expiry_date']
            action=i['action']
            product=i['product']
            pricetype=i['pricetype']
            quantity=i['quantity']
            price=i['price']
            option_type=i['option_type']
            strike_int=i['strike_int']
            offset=i['offset']
            splitorder=i['splitorder']
            split_quantity=i['split_quantity']
            
            data_1={
                "api_key": apikeyy,
                "api_secret": apisecrett,
                "data":
                    {   "broker":broker,
                        "strategy":strategy,
                        "spot_symbol":spot_symbol,
                        "expiry_date":expiry_date,
                        "action":action,
                        "product":product,
                        "pricetype":pricetype,
                        "quantity":quantity,
                        "price":price,
                        "option_type":option_type,
                        "strike_int":strike_int,
                        "offset":offset,
                        "splitorder":splitorder,
                        "split_quantity":split_quantity
                       }
            }
            
            order_data.append(data_1)
            

        data = {
            "api_key": self.api_key,
            "api_secret": self.api_secret,
            "data":
                {
                    "orders": order_data   

                }
        }
        url = self.burl + "PlaceMultiFOOptionsOrder"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())

    
    def ModifyOrder(self,broker: str,exchange: str,symbol: str,order_id: str,action: str,product: str,pricetype: str ,quantity: int,price: float=0,disclosed_quantity: int=0,trigger_price: float=0,   strategy: str = "Python", api_key: str="default", api_secret: str="default"):
        """This function modifies an open order for the specified symbol on a specified exchange through the specified broker.

    Parameters
    ----------
        broker (str): The name of the broker short code. (e.g ab - aliceblue,an - angelone, fs - firstock, up- upstox, ze- zerodha ). Refer API Docs appendix for complete broker code
        exchange (str): The name of the exchange (NSE,NFO,BSE,BFO,MCX,CDS).
        symbol (str): The symbol for the order.
        order_id (str/int): the id of the order to modify.
        action (str): The type of the order (e.g. "BUY", "SELL").
        product (str): The product type for the order (e.g. "CNC,MIS,NRML").
        pricetype (str, optional): The type of the price (e.g. "MARKET,LIMIT,SL,SL-M"). Defaults to "MARKET".
        quantity (int): The number of shares to be ordered.
        price (float, optional): The price of the order. Defaults to 0.
        disclosed_quantity (int, optional): The quantity to be disclosed in the order. Defaults to 0.
        trigger_price (float, optional): The trigger price for the order. Defaults to 0.
        splitorder (str, optional): The split order  (e.g. "NO,YES"). Defaults to "NO".
        split_quantity (int, optional): The quantity to be split in the order. Defaults to 1. Set the value max to "Freeze quantity" to slice larger orders
        strategy (str, optional) : Name of the trading strategy to use, default is "Python".
        api_key (str, optional): The API key to use. Defaults to "default".
        api_secret (str, optional): The API secret to use. Defaults to "default".

    Returns:
        dict: A dictionary containing the modify order response from the Broker.
    """
        
        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        data = {
            "api_key":api_key,
            "api_secret":api_secret,
            "data":{    
                      "broker":broker,
                      "strategy":strategy,
                      "exchange":exchange,
                      "symbol":symbol,
                      "order_id":order_id,
                      "action":action,
                      "product":product,
                      "pricetype":pricetype,
                      "quantity":str(quantity),
                      "price":str(price),
                      "disclosed_quantity":str(disclosed_quantity),
                      "trigger_price":str(trigger_price)
                     
                   }
            } 
        url = self.burl + "ModifyOrder"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())
    
    def CancelOrder(self, broker: str,order_id: str, strategy: str = "Python", api_key: str="default", api_secret: str="default"):

        """This function Cancel the specified open order on the specified broker based on the order id.

    Parameters
    ----------
        broker (str): the broker to cancel the order on
        order_id (str/int): the id of the order to cancel
        strategy (str, optional) : Name of the trading strategy to use, default is "Python".
        api_key (str, optional): The API key to use. Defaults to "default".
        api_secret (str, optional): The API secret to use. Defaults to "default".

    Returns:
        dict: A dictionary containing the Cancel order response from the Broker.
    """

        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        data = {
            "api_key": api_key,
            "api_secret": api_secret,
            "data":
                {
                    "broker": broker,
                    "strategy":strategy,
                    "order_id":str(order_id)
                }

        }
        url = self.burl + "CancelOrder"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())
    
    def CancelAllOrder(self, broker: str, strategy: str = "Python",  api_key: str="default", api_secret: str="default"):
        """This function Cancel's all the open order on the specified broker .

    Parameters
    ----------
        broker (str): the broker to cancel the order on
        strategy (str, optional) : Name of the trading strategy to use, default is "Python".
        api_key (str, optional): The API key to use. Defaults to "default".
        api_secret (str, optional): The API secret to use. Defaults to "default".

    Returns:
        dict: A dictionary containing the order response from the Broker.
    """
        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        data = {
            "api_key": api_key,
            "api_secret": api_secret,
            "data":
                {
                    "broker": broker,
                    "strategy":strategy
                }

        }
        url = self.burl + "CancelAllOrder"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())
    
    def OrderHistory(self, broker: str,order_id: str, api_key: str="default", api_secret: str="default"):
        """This function display's the history of the specified order id on the specified broker .

    Parameters
    ----------
        broker (str): The name of the broker short code. (e.g ab - aliceblue,an - angelone, fs - firstock, up- upstox, ze- zerodha ). Refer API Docs appendix for complete broker code
        order_id (str/int): the id of the order .
        api_key (str, optional): The API key to use. Defaults to "default".
        api_secret (str, optional): The API secret to use. Defaults to "default".

    Returns:
        dict: A dictionary containing the order response from the Broker.
    """

        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        data = {
            "api_key": api_key,
            "api_secret": api_secret,
            "data":
                {
                    "broker": broker,
                    "order_id":str(order_id)
                }

        }
        url = self.burl + "OrderHistory"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())

    def OrderBook(self, broker: str, api_key: str="default", api_secret: str="default"):
        """This function display's the orderbook on the specified broker .

    Parameters
    ----------
        broker (str): The name of the broker short code. (e.g ab - aliceblue,an - angelone, fs - firstock, up- upstox, ze- zerodha ). Refer API Docs appendix for complete broker code.
        api_key (str, optional): The API key to use. Defaults to "default".
        api_secret (str, optional): The API secret to use. Defaults to "default".

    Returns:
        dict: A dictionary containing the order history response from the Broker.
    """
        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        data = {
            "api_key": api_key,
            "api_secret": api_secret,
            "data":
                {
                    "broker": broker
                }

        }
        url = self.burl + "OrderBook"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())
    
    def OrderStatus(self, broker: str,order_id: str, api_key: str="default", api_secret: str="default"):
        """This function display's the status of the order of the specified order id on the specified broker .

    Parameters
    ----------
        broker (str): The name of the broker short code. (e.g ab - aliceblue,an - angelone, fs - firstock, up- upstox, ze- zerodha ). Refer API Docs appendix for complete broker code
        order_id (str/int): the id of the order .
        api_key (str, optional): The API key to use. Defaults to "default".
        api_secret (str, optional): The API secret to use. Defaults to "default".

    Returns:
        dict: A dictionary containing the orderstatus response from the Broker.
    """

        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        data = {
            "api_key": api_key,
            "api_secret": api_secret,
            "data":
                {
                    "broker": broker,
                    "order_id":str(order_id)
                }

        }
        url = self.burl + "OrderStatus"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())
    
    def TradeBook(self,broker: str,api_key: str="default", api_secret: str="default"):
        """This function display's the tradebook of the specified broker .

    Parameters
    ----------
        broker (str): The name of the broker short code. (e.g ab - aliceblue,an - angelone, fs - firstock, up- upstox, ze- zerodha ). Refer API Docs appendix for complete broker code.
        api_key (str, optional): The API key to use. Defaults to "default".
        api_secret (str, optional): The API secret to use. Defaults to "default".

    Returns:
        dict: A dictionary containing the tradebook response from the Broker.
    """
        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        data = {
            "api_key": api_key,
            "api_secret": api_secret,
            "data":
                {
                    "broker": broker
                }

        }
        url = self.burl + "TradeBook"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())
    
    def PositionBook(self,broker: str,api_key: str="default", api_secret: str="default"):
        """This function display's the positionbook of the specified broker .

    Parameters
    ----------
        broker (str): The name of the broker short code. (e.g ab - aliceblue,an - angelone, fs - firstock, up- upstox, ze- zerodha ). Refer API Docs appendix for complete broker code.
        api_key (str, optional): The API key to use. Defaults to "default".
        api_secret (str, optional): The API secret to use. Defaults to "default".

    Returns:
        dict: A dictionary containing the positionbook response from the Broker.
    """

        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        data = {
            "api_key": api_key,
            "api_secret": api_secret,
            "data":
                {
                    "broker": broker
                }

        }
        url = self.burl + "PositionBook"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())
    
    def OpenPositions(self,broker: str,symbol: str="",exchange: str="",product: str="",api_key: str="default", api_secret: str="default"):
        """This function display's the open positions of the specified broker .

    Parameters
    ----------
        broker (str): The name of the broker short code. (e.g ab - aliceblue,an - angelone, fs - firstock, up- upstox, ze- zerodha ). Refer API Docs appendix for complete broker code.
        symbol(str, optional): The symbol for the order.
        exchange (str): The name of the exchange (NSE,NFO,BSE,BFO,MCX,CDS).
        product (str, optional): The product type for the order (e.g. "CNC,MIS,NRML").
        api_key (str, optional): The API key to use. Defaults to "default".
        api_secret (str, optional): The API secret to use. Defaults to "default".

    Returns:
        dict: A dictionary containing the openpositions response from the Broker.
    """

        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        if(symbol==""):
            data = {
                "api_key": api_key,
                "api_secret": api_secret,
                "data":
                    {
                        "broker": broker
                    }

            }
        else:
            data = {
                "api_key": api_key,
                "api_secret": api_secret,
                "data":
                    {
                        "broker": broker,
                        "symbol":symbol,
                        "product":product
                    }

            }
        url = self.burl + "OpenPositions"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())
    

    def AllPositions(self,broker: str,symbol: str="",exchange: str="",product: str="",api_key: str="default", api_secret: str="default"):
        """This function display's the open positions of the specified broker .

    Parameters
    ----------
        broker (str): The name of the broker short code. (e.g ab - aliceblue,an - angelone, fs - firstock, up- upstox, ze- zerodha ). Refer API Docs appendix for complete broker code.
        symbol(str, optional): The symbol for the order.
        exchange (str): The name of the exchange (NSE,NFO,BSE,BFO,MCX,CDS).
        product (str, optional): The product type for the order (e.g. "CNC,MIS,NRML").
        api_key (str, optional): The API key to use. Defaults to "default".
        api_secret (str, optional): The API secret to use. Defaults to "default".

    Returns:
        dict: A dictionary containing the openpositions response from the Broker.
    """

        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        if(symbol==""):
            data = {
                "api_key": api_key,
                "api_secret": api_secret,
                "data":
                    {
                        "broker": broker
                    }

            }
        else:
            data = {
                "api_key": api_key,
                "api_secret": api_secret,
                "data":
                    {
                        "broker": broker,
                        "symbol":symbol,
                        "product":product
                    }

            }
        url = self.burl + "AllPositions"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())
    
    def SquareOffPosition(self,broker: str,exchange: str,product: str,symbol: str, strategy: str = "Python", api_key: str="default", api_secret: str="default"):
        """This function squares off the position for the specified symbol on a specified exchange through the specified broker.

    Parameters
    ----------
        broker (str): The name of the broker short code. (e.g ab - aliceblue,an - angelone, fs - firstock, up- upstox, ze- zerodha ). Refer API Docs appendix for complete broker code
        exchange (str): The name of the exchange (NSE,NFO,BSE,BFO,MCX,CDS).
        product (str): The product type for the order (e.g. "CNC,MIS,NRML").
        symbol (str): The symbol for the order.
        strategy (str, optional) : Name of the trading strategy to use, default is "Python".
        api_key (str, optional): The API key to use. Defaults to "default".
        api_secret (str, optional): The API secret to use. Defaults to "default".

    Returns:
        dict: A dictionary containing the squareoff positions response from the Broker.
    """
        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        data = {
            "api_key": api_key,
            "api_secret": api_secret,
            "data":
                {
                    "broker": broker,
                    "strategy":strategy,
                    "exchange":exchange,
                    "product":product,
                    "symbol":symbol
                }

        }
        url = self.burl + "SquareOffPosition"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())
    
    def SquareOffAllPosition(self,broker: str,strategy: str = "Python", api_key: str="default", api_secret: str="default"):
        """This function squares of all the postion of the specified broker .

    Parameters
    ----------
    broker (str): The name of the broker short code. (e.g ab - aliceblue,an - angelone, fs - firstock, up- upstox, ze- zerodha ). Refer API Docs appendix for complete broker code.
    strategy (str, optional) : Name of the trading strategy to use, default is "Python".
    api_key (str, optional): The API key to use. Defaults to "default".
    api_secret (str, optional): The API secret to use. Defaults to "default".

    Returns:
        dict: A dictionary containing the squareoff all positions response from the Broker.
    """
        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        data = {
            "api_key": api_key,
            "api_secret": api_secret,
            "data":
                {
                    "broker": broker,
                    "strategy":strategy
                }

        }
        url = self.burl + "SquareOffAllPosition"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())
    
    def Holdings(self,broker: str,api_key: str="default", api_secret: str="default"):
        """This function display's the holdings of the specified broker .

    Parameters
    ----------
        broker (str): The name of the broker short code. (e.g ab - aliceblue,an - angelone, fs - firstock, up- upstox, ze- zerodha ). Refer API Docs appendix for complete broker code.
        api_key (str, optional): The API key to use. Defaults to "default".
        api_secret (str, optional): The API secret to use. Defaults to "default".

    Returns:
        dict: A dictionary containing the holdings response from the Broker.
    """
        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        data = {
            "api_key": api_key,
            "api_secret": api_secret,
            "data":
                {
                    "broker": broker
                }

        }
        url = self.burl + "Holdings"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())

    def Funds(self,broker: str,api_key: str="default", api_secret: str="default"):
        """This function display's the funds of the user of the specified broker .

    Parameters
    ----------
    broker (str): The name of the broker short code. (e.g ab - aliceblue,an - angelone, fs - firstock, up- upstox, ze- zerodha ). Refer API Docs appendix for complete broker code.
    api_key (str, optional): The API key to use. Defaults to "default".
    api_secret (str, optional): The API secret to use. Defaults to "default".

    Returns:
        dict: A dictionary containing the funds response from the Broker.
    """

        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        data = {
            "api_key": api_key,
            "api_secret": api_secret,
            "data":
                {
                    "broker": broker
                }

        }
        url = self.burl + "Funds"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())
    
    def ExitBOOrder(self, broker: str,order_id: str, strategy: str = "Python", api_key: str="default", api_secret: str="default"):
        """This function exits the specified open bracket order on the specified broker based on the order id.

    Parameters
    ----------
        broker (str): the broker to cancel the order on
        order_id (str/int): the id of the order to cancel
        strategy (str, optional) : Name of the trading strategy to use, default is "Python".
        api_key (str, optional): The API key to use. Defaults to "default".
        api_secret (str, optional): The API secret to use. Defaults to "default".

    Returns:
        dict: A dictionary containing the Exit BO order response from the Broker.
    """

        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        data = {
            "api_key": api_key,
            "api_secret": api_secret,
            "data":
                {
                    "broker": broker,
                    "strategy":strategy,
                    "order_id":str(order_id)
                }

        }
        url = self.burl + "ExitBOOrder"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())
    
    def ExitCOOrder(self, broker: str,order_id: str, strategy: str = "Python", api_key: str="default", api_secret: str="default"):
        """This function exits the specified open cover order on the specified broker based on the order id.

    Parameters
    ----------
        broker (str): the broker to cancel the order on
        order_id (str/int): the id of the order to cancel
        strategy (str, optional) : Name of the trading strategy to use, default is "Python".
        api_key (str, optional): The API key to use. Defaults to "default".
        api_secret (str, optional): The API secret to use. Defaults to "default".

    Returns:
        dict: A dictionary containing the Exit CO order response from the Broker.
    """
        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        data = {
            "api_key": api_key,
            "api_secret": api_secret,
            "data":
                {
                    "broker": broker,
                    "strategy":strategy,
                    "order_id":str(order_id)
                }

        }
        url = self.burl + "ExitCOOrder"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())
    
    def GetQuote(self,broker: str,symbol: str,exchange: str,api_key: str="default", api_secret: str="default"):
        """This function gets the quote for the specified symbol on a specified exchange through the specified broker.

    Parameters
    ----------
        broker (str): The name of the broker short code. (e.g ab - aliceblue,an - angelone, fs - firstock, up- upstox, ze- zerodha ). Refer API Docs appendix for complete broker code
        exchange (str): The name of the exchange (NSE,NFO,BSE,BFO,MCX,CDS).
        symbol (str): The symbol for the order.
        api_key (str, optional): The API key to use. Defaults to "default".
        api_secret (str, optional): The API secret to use. Defaults to "default".

    Returns:
        dict: A dictionary containing the GetQuote response from the Broker.
    """

        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        data = {
            "api_key": api_key,
            "api_secret": api_secret,
            "data":
                {
                    "broker": broker,
                    "symbol":symbol,
                    "exchange":exchange 
                }

        }
        url = self.burl + "GetQuote"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())
    
    def Profile(self,broker: str,api_key: str="default", api_secret: str="default"):
        """This function display's the profile of the user of the specified broker .

    Parameters
    ----------
        broker (str): The name of the broker short code. (e.g ab - aliceblue,an - angelone, fs - firstock, up- upstox, ze- zerodha ). Refer API Docs appendix for complete broker code.
        api_key (str, optional): The API key to use. Defaults to "default".
        api_secret (str, optional): The API secret to use. Defaults to "default".

    Returns:
        dict: A dictionary containing the trader/investor profile response from the Broker.
    """

        if (api_key == "default" and api_secret == "default"):
            api_key = self.api_key
            api_secret = self.api_secret
        data = {
            "api_key": api_key,
            "api_secret": api_secret,
            "data":
                {
                    "broker": broker
                }

        }
        url = self.burl + "Profile"
        r = requests.post(url, data=json.dumps(data), headers=self.headers)
        return (r.json())