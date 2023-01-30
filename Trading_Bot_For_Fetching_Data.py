import os
import requests
import dateutil.parser



#Login function for login into the account through login creditials 
#if two factor authetication in enabled, manuelly fill the twofact code into the 
#variable 

def login_into(userid, password, _2fact):
    session = requests.Session()
    response = session.post('https://kite.zerodha.com/api/login', data={
        "userid":userid,
        "password":password
    })
    response = session.post('https://kite.zerodha.com/api/twofa', data={
        "request_id": response.json()['data']['request_id'],
        "_2fact": _2fact,
        "user_id": response.json()['data']['user_id']
    })
    encodetoken = response.cookies.get('encodetoken')
    if encodetoken:
        return encodetoken
    else:
        raise Exception("Enter Valid Details")

    
class KiteApp:    
    def __init__(self, encodetoken):
        self.headers = {"Authorization": f"encodetoken {encodetoken}"}
        self.session = requests.session()
        self.root_url = "https://api.kite.trade"
        self.session.get(self.root_url, headers=self.headers)

    def instruments(self, exchange=None):
        data = self.session.get(f"{self.root_url}/instruments",headers=self.headers).text.split("\n")
        Exchange = []
        for i in data[1:-1]:
            row = i.split(",")
            if exchange is None or exchange == row[11]:
                Exchange.append({'instrument_token': int(row[0]), 'exchange_token': row[1], 'tradingsymbol': row[2],
                                 'name': row[3][1:-1], 'last_price': float(row[4]),
                                 'expiry': dateutil.parser.parse(row[5]).date() if row[5] != "" else None,
                                 'strike': float(row[6]), 'tick_size': float(row[7]), 'lot_size': int(row[8]),
                                 'instrument_type': row[9], 'segment': row[10],
                                 'exchange': row[11]})
        return Exchange        
