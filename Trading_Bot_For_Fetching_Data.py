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
