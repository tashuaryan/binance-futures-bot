import hmac
import hashlib
import time
import requests
import logging

logger = logging.getLogger(__name__)

class BinanceFuturesTestnetClient:
    def __init__(self, api_key: str, api_secret: str):
        self.base_url = "https://testnet.binancefuture.com"
        self.api_key = api_key
        self.api_secret = api_secret
        self.headers = {"X-MBX-APIKEY": self.api_key}

    def _generate_signature(self, query_string: str) -> str:
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None, stop_price: float = None):
        timestamp = int(time.time() * 1000)
        
        # Dynamically choose the correct endpoint and setup parameters based on Binance's rules
        if order_type.upper() == "STOP_LIMIT":
            endpoint = "/fapi/v1/algoOrder"
            converted_type = "STOP"
            algo_type = "CONDITIONAL"
        else:
            endpoint = "/fapi/v1/order"
            converted_type = order_type.upper()
            algo_type = None

        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": converted_type,
            "quantity": quantity,
            "timestamp": timestamp
        }
        
        # Inject the mandatory algoType for advanced orders
        if algo_type:
            params["algoType"] = algo_type
        
        if order_type.upper() == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC"
        elif order_type.upper() == "STOP_LIMIT":
            params["price"] = price
            # CRITICAL FIX: Properly passing 'triggerPrice' instead of 'stopPrice'
            params["triggerPrice"] = stop_price  
            params["timeInForce"] = "GTC"
            params["workingType"] = "CONTRACT_PRICE"

        # Safely build the query string ignoring any empty values
        query_string = "&".join([f"{k}={v}" for k, v in params.items() if v is not None])
        signature = self._generate_signature(query_string)
        url = f"{self.base_url}{endpoint}?{query_string}&signature={signature}"

        logger.info(f"Sending Order Request: {params} to endpoint: {endpoint}")
        
        try:
            response = requests.post(url, headers=self.headers, timeout=10)
            response_json = response.json()
            
            if response.status_code == 200:
                logger.info(f"Order Placement Success: {response_json}")
                return {"success": True, "data": response_json}
            else:
                logger.error(f"API Error Response ({response.status_code}): {response_json}")
                return {"success": False, "error": response_json.get("msg", "Unknown API Error")}
                
        except requests.exceptions.RequestException as e:
            logger.critical(f"Network / Connection Error: {str(e)}")
            return {"success": False, "error": f"Network Error: {str(e)}"}