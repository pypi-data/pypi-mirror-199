## Algomojo - Arrow API Python Client V1

## ABOUT

Algomojo is a Python library that facilitates the development of trading algorithms using the [Algomojo Free API](https://algomojo.com/) and Free Algo Trading Platform. The library supports both REST-API interfaces and provides features such as real-time order execution, smartorder execution, placing options orders, placing multi orders, order modification/cancellation, and access to order book, trade book, open positions, orderstatus, position square-off functionalities, getquotes, profile and fund details. For a comprehensive understanding of each API's behavior, please refer to the Algomojo API documentation.


## License
Algomojo  (c) 2023. Licensed under the MIT License.


## Documentation
[Algomojo Rest API documentation ](https://amapi.algomojo.com/v1/docs/)




## Installation
Install from PyPI

        pip install Algomojo

Alternatively, install from source. Execute setup.py from the root directory.
python setup.py install

Always use the newest version while the project is still in alpha!


## Usage Examples
In order to call Algomojo trade API, you need to sign up for an trading account with one of the partner broker and obtain API key pairs and enjoy unlimited access to the API based trading. Replace api_key and api_secret_key with what you get from the web console.


## Getting Started

After downloading package import the package and create the object with api credentials


        from algomojo.pyapi import *





## Creating  Object

For creating an object there are 3 arguments which would be passed

        api_key : str
        User Api key (logon to algomojo account to find api credentials)
        api_secret : str
        User Api secret (logon to algomojo account to find api credentials)
        version : str
        The current version of the API.

Sample:
        
        algomojo=api(api_key="14ca89ea8fxd944609eea66e59cde3495fb",
                        api_secret="76360446900d005cac830d40e03efd9c")
        
## Using Object Methods
obj.method(mandatory_parameters)  or obj.method(madatory_parameters+required_parameters)


# Avaliable Methods
        
### 1. PlaceOrder:  

        Function with mandatory parmeters: 
                PlaceOrder(broker,symbol,exchange,action,product,pricetype,quantity)
        
        Function with all parametrs:       
                PlaceOrder(broker,exchange,symbol,action,product,pricetype,quantity,price,
                                        strategy,disclosed_quantity,trigger_price,amo,splitorder,split_quantity,api_key,api_secret)
                
        Sample :        
                from algomojo.pyapi import *
                
                # Set the API Key and API Secret key obtained from Algomojo MyAPI Section
                algomojo=api(api_key="14ca89ea8fxd944609eea66e59cde3495fb",
                                api_secret="76360446900d005cac830d40e03efd9c")

                # Place Market Order in the trading symbol RELIANCE-EQ
                algomojo.PlaceOrder(broker="ab",
                                strategy="Python Example",
                                exchange="NSE",
                                symbol="RELIANCE-EQ",
                                action="BUY",
                                product="MIS",
                                quantity=10)
                
                #Place Limit Order in the trading symbol ZOMATO-EQ
                algomojo.PlaceOrder(broker="ab",
                                strategy="Python Example",
                                exchange="NSE",
                                symbol="ZOMATO-EQ",
                                action="BUY",
                                product="MIS",
                                quantity=10,
                                pricetype="LIMIT",
                                price=54)

                #Place Larger Order in options with Split Order mode enabled
                algomojo.PlaceOrder(broker="ab",
                                strategy="Python Example",
                                exchange="NFO",
                                symbol="NIFTY23FEB18000CE",
                                action="BUY",
                                product="NRML",
                                quantity=5200,
                                pricetype="MARKET",
                                splitorder="YES",
                                split_quantity=1800)
                
### 2. PlaceBOOrder:  

        Function with mandatory parmeters: 
                PlaceBOOrder(broker,symbol,exchange,action,pricetype,quantity,price,squareoff,stoploss,trailing_stoploss)
        
        Function with all parametrs:       
                PlaceBOOrder(broker,symbol,exchange,action,pricetype,quantity,price,squareoff,stoploss,trailing_stoploss
                        strategy,disclosed_quantity,trigger_price,api_key,api_secret)
                
        Sample :        
                algomojo.PlaceBOOrder(broker="ab",
                                        strategy="Python Example",
                                        exchange="NSE",
                                        symbol="YESBANK-EQ",
                                        action="BUY",
                                        pricetype="LIMIT",
                                        quantity="1",
                                        price="16.5",
                                        squareoff="2",
                                        stoploss="2",
                                        trailing_stoploss="1",
                                        trigger_price="0",
                                        disclosed_quantity="0")   

### 3. PlaceCOOrder:  

        Function with mandatory parmeters: 
                PlaceCOOrder(broker,symbol,exchange,action,pricetype,quantity,price,stop_price)
        
        Function with all parametrs:       
                PlaceCOOrder(broker,symbol,exchange,action,pricetype,quantity,price,stop_price
                        strategyapi_key,api_secret)
                
        Sample :        
                algomojo.PlaceCOOrder(broker="ab",
                                        strategy="Python Example",
                                        exchange="NSE",
                                        symbol="YESBANK-EQ",
                                        action="BUY",
                                        pricetype="LIMIT",
                                        quantity="1",
                                        price="16.5",
                                        stop_price="15") 
### 4. PlaceFOOptionsOrder:  

        Function with mandatory parmeters: 
                PlaceFOOptionsOrder(broker,spot_symbol,expiry_date,action,product,pricetype,quantity,price,option_type,strike_int)
        
        Function with all parametrs:       
                PlaceFOOptionsOrder(broker,spot_symbol,expiry_date,action,product,pricetype,quantity,price,option_type,strike_int
                        strategy,offset,trigger_price,splitorder,split_quantity,api_key,api_secret)
                
        Sample :        
                algomojo.PlaceFOOptionsOrder(broker="ab",
                                                strategy="Python Example",
                                                spot_symbol="NIFTY",
                                                expiry_date="23FEB",
                                                action="BUY",
                                                product="NRML",
                                                pricetype="MARKET",
                                                quantity="50",
                                                price="0",
                                                option_type="CE",
                                                strike_int="50",
                                                offset="-2",
                                                splitorder="NO",
                                                split_quantity="50")

### 5. PlaceSmartOrder:  

        Function with mandatory parmeters: 
                PlaceSmartOrder(broker,symbol,exchange,action,product,pricetype,quantity,price,position_size)
        
        Function with all parametrs:       
                PlaceSmartOrder(broker,symbol,exchange,action,product,pricetype,quantity,price,position_size
                        strategy,disclosed_quantity,trigger_price,amo,splitorder,split_quantity,api_key,api_secret)
                
        Sample :        
                algomojo.PlaceSmartOrder(broker="ab",
                                        strategy="Python Example",
                                        exchange="NSE",
                                        symbol="YESBANK-EQ",
                                        action="BUY",
                                        product="CNC",
                                        pricetype="MARKET",
                                        quantity="7",
                                        price="0",
                                        position_size="7",
                                        trigger_price="0",
                                        disclosed_quantity="0",
                                        amo="NO",
                                        splitorder="NO",
                                        split_quantity="2") 

### 6. PlaceStrategyOrder:  

        Function with mandatory parmeters: 
                PlaceStrategyOrder(strategy_id,action)
        
        Function with all parametrs:       
                PlaceStrategyOrder(strategy_id,action,api_key,api_secret)
                
                Sample :        
                algomojo.PlaceStrategyOrder(strategy_id="ALGO",
                                                action="BUY") 


### 7. PlaceMultiOrder:  

        Function with mandatory parmeters: 
                PlaceMultiOrder(broker,symbol,exchange,action,product,pricetype,quantity,price)
        
        Function with all parametrs:       
                PlaceMultiOrder(broker,symbol,exchange,action,product,pricetype,quantity,price,
                        strategy,disclosed_quantity,trigger_price,amo,splitorder,split_quantity,api_key,api_secret)
                
        Sample : 

                orders=[{"api_key":"gusat281627asa827382gasg177n79","api_secret":"d872s766suwys78s7aji78673sads","broker":"ab","symbol":"IDEA-EQ","exchange":"NSE","product":"CNC","pricetype":"MARKET","quantity":2,"action":"BUY","splitorder":"YES","split_quantity":2},{"api_key":"aji7827382gasgd87273sads177n79","api_secret":"628162gusats766suwys78s77asa8","broker":"tc","symbol":"KRETTOSYS","exchange":"BSE","product":"MIS","pricetype":"LIMIT","quantity":1,"price":"0.68","action":"BUY"}]

                algomojo.PlaceMultiOrder(orders)

### 8. PlaceMultiBOOrder:  

        Function with mandatory parmeters: 
                PlaceMultiBOOrder(broker,symbol,exchange,action,pricetype,quantity,price,squareoff,stoploss,trailing_stoploss)
        
        Function with all parametrs:       
                PlaceMultiBOOrder(broker,symbol,exchange,action,pricetype,quantity,price,squareoff,stoploss,trailing_stoploss
                        strategy,disclosed_quantity,trigger_price,api_key,api_secret)
                
        Sample : 

                orders=[{"api_key":"gusat281627asa827382gasg177n79","api_secret":"d872s766suwys78s7aji78673sads","broker":"ab","symbol":"YESBANK-EQ","exchange":"NSE","pricetype":"MARKET","quantity":1,"action":"BUY","squareoff":"2","stoploss":"2","trailing_stoploss":"1"},{"api_key":"aji7827382gasgd87273sads177n79","api_secret":"628162gusats766suwys78s77asa8","broker":"tc","symbol":"BHEL-EQ","exchange":"NSE","pricetype":"LIMIT","quantity":1,"price":"75.5","action":"BUY","squareoff":"2","stoploss":"2","trailing_stoploss":"1"}]

                algomojo.PlaceMultiBOOrder(orders) 


### 9. PlaceMultiFOOptionsOrder:  

        Function with mandatory parmeters: 
                PlaceMultiFOOptionsOrder(broker,spot_symbol,expiry_date,action,product,pricetype,quantity,price,option_type,strike_int)
        
        Function with all parametrs:       
                PlaceMultiFOOptionsOrder(broker,spot_symbol,expiry_date,action,product,pricetype,quantity,price,option_type,strike_int
                        strategy,offset,trigger_price,splitorder,split_quantity,api_key,api_secret)
                
        Sample : 

                orders=[{"api_key":"gusat281627asa827382gasg177n79","api_secret":"d872s766suwys78s7aji78673sads","broker":"ab","strategy":"Python Example","spot_symbol":"NIFTY","expiry_date":"23FEB","action":"BUY","product":"NRML","pricetype":"MARKET","quantity":"150","price":"0","option_type":"CE","strike_int":"50","offset":"-2","splitorder":"NO","split_quantity":"50"},{"api_key":"aji7827382gasgd87273sads177n79","api_secret":"628162gusats766suwys78s77asa8","broker":"tc","spot_symbol":"NIFTY","expiry_date":"02MAR23","action":"BUY", "product":"NRML","pricetype":"MARKET", "quantity":"150","option_type":"CE","strike_int":"50","offset":"-2","splitorder":"YES","split_quantity":"50"}]

                algomojo.PlaceMultiFOOptionsOrder(orders) 

### 10. ModifyOrder:  

        Function with mandatory parmeters: 
                ModifyOrder(broker,symbol,exchange,order_id,action,product,pricetype,quantity,price)
        
        Function with all parametrs:       
                ModifyOrder(broker,symbol,exchange,order_id,action,product,pricetype,quantity,price,
                        strategy,disclosed_quantity,trigger_price,strategy,api_key,api_secret)
                
        Sample :        
                algomojo.ModifyOrder(broker="ab",
                                     exchange="NSE",
                                     symbol="YESBANK-EQ",
                                     order_id="200010639230213",
                                     action="BUY",
                                     product="CNC",
                                     pricetype="LIMIT",
                                     price="16.65",
                                     quantity="1",
                                     disclosed_quantity="0",
                                     trigger_price="0",
                                     strategy="Python Example") 

### 11. CancelOrder:  

        Function with mandatory parmeters: 
                CancelOrder(broker,order_id)
        
        Function with all parametrs:       
                CancelOrder(broker,order_id,strategy,api_key,api_secret)
                
        Sample :        
                algomojo.CancelOrder(broker="ab",strategy="Python Example",
                                        order_id="230001063923021") 

### 12. CancelAllOrder:  

        Function with mandatory parmeters: 
                CancelAllOrder(broker)
        
        Function with all parametrs:       
                CancelAllOrder(broker,strategy,api_key,api_secret)
                
        Sample :        
                algomojo.CancelAllOrder(broker="ab",strategy="Python Example") 

### 13. OrderHistory:  

        Function with mandatory parmeters: 
                OrderHistory(broker,order_id)
        
        Function with all parametrs:       
                OrderHistory(broker,order_id,api_key,api_secret)
                
        Sample :        
                algomojo.OrderHistory(broker="ab",
                                order_id="230001063923021") 

### 14. OrderBook:  

        Function with mandatory parmeters: 
                OrderBook(broker)
        
        Function with all parametrs:       
                OrderBook(broker,api_key,api_secret)
                
        Sample :        
                algomojo.OrderBook(broker="ab")  

### 15. OrderStatus:  

        Function with mandatory parmeters: 
                OrderStatus(broker,order_id)
        
        Function with all parametrs:       
                OrderStatus(broker,order_id,api_key,api_secret)
                
        Sample :        
                algomojo.OrderStatus(broker="ab",
                                order_id="230001063923021")

### 16. TradeBook:  

        Function with mandatory parmeters: 
                TradeBook(broker)
        
        Function with all parametrs:       
                TradeBook(broker,api_key,api_secret)
                
        Sample :        
                algomojo.TradeBook(broker="ab")  

### 17. PositionBook:  

        Function with mandatory parmeters: 
                PositionBook(broker)
        
        Function with all parametrs:       
                PositionBook(broker,api_key,api_secret)
                
        Sample :        
                algomojo.PositionBook(broker="ab") 

### 18. OpenPositions:  

        Function with mandatory parmeters: 
                OpenPositions(broker)
        
        Function with all parametrs:       
                OpenPositions(broker,symbol,product,api_key,api_secret)
                
        Sample :        
                algomojo.OpenPositions(broker="ab",
                                        symbol= "YESBANK-EQ",
                                        product="CNC")

### 19. AllPositions:  

        Function with mandatory parmeters: 
                OpenPositions(broker)
        
        Function with all parametrs:       
                OpenPositions(broker,symbol,product,api_key,api_secret)
                
        Sample :        
                algomojo.AllPositions(broker="ab",
                                        symbol= "YESBANK-EQ",
                                        product="CNC")

### 20. SquareOffPosition:  

        Function with mandatory parmeters: 
                SquareOffPosition(broker,exchange,symbol,product)
        
        Function with all parametrs:       
                SquareOffPosition(broker,exchange,symbol,product,strategy,api_key,api_secret)
                
        Sample :        
                algomojo.SquareOffPosition(broker="ab",
                                        exchange="NSE",
                                        product="CNC",
                                        symbol= "IDEA-EQ",
                                        strategy="Python Example")

### 21. SquareOffAllPosition:  

        Function with mandatory parmeters: 
                SquareOffAllPosition(broker)
        
        Function with all parametrs:       
                SquareOffAllPosition(broker,strategy,api_key,api_secret)
                
        Sample :        
                algomojo.SquareOffAllPosition(broker="ab",strategy="Python Example")) 

### 22. Holdings:  

        Function with mandatory parmeters: 
                Holdings(broker)
        
        Function with all parametrs:       
                Holdings(broker,api_key,api_secret)
                
        Sample :        
                algomojo.Holdings(broker="ab") 

### 23. Funds:  

        Function with mandatory parmeters: 
                Funds(broker)
        
        Function with all parametrs:       
                Funds(broker,api_key,api_secret)
                
        Sample :        
                algomojo.Funds(broker="ab") 

### 24. ExitBOOrder:  

        Function with mandatory parmeters: 
                ExitBOOrder(broker,order_id)
        
        Function with all parametrs:       
                ExitBOOrder(broker,order_id,strategy,api_key,api_secret)
                
        Sample :        
                algomojo.ExitBOOrder(broker="ab",
                                order_id="230001063923021",
                                strategy="Python Example")) 

### 25. ExitCOOrder:  

        Function with mandatory parmeters: 
                ExitCOOrder(broker,order_id)
        
        Function with all parametrs:       
                ExitCOOrder(broker,order_id,strategy,api_key,api_secret)
                
        Sample :        
                algomojo.ExitCOOrder(broker="ab",
                                order_id="230001063923021",
                                strategy="Python Example")) 

### 26. GetQuote:  

        Function with mandatory parmeters: 
                GetQuote(broker,exchange,symbol)
        
        Function with all parametrs:       
                GetQuote(broker,exchange,symbol,api_key,api_secret)
                
        Sample :        
                algomojo.GetQuote(broker="ab",
                                exchange="NSE",
                                symbol= "IDEA-EQ")

### 27. Profile:  

        Function with mandatory parmeters: 
                Profile(broker)
        
        Function with all parametrs:       
                Profile(broker,api_key,api_secret)
                
        Sample :        
                algomojo.Profile(broker="ab") 