import rsa
import binascii
import requests
from requests.auth import HTTPBasicAuth
import json
import base64


def user_add(email, password):
    with open('pub_key.pem', mode='rb') as pub_file:
        keydata = pub_file.read()

    pub_key = rsa.PublicKey.load_pkcs1(keydata)
    message = email + ':' + password
    crypto = rsa.encrypt(message.encode(), pub_key)

    payload = {"data": binascii.hexlify(crypto).decode()}
    headers = {
        'content-type': 'application/json',
        'charset': 'utf-8',
    }

    res = requests.post('http://127.0.0.1:5000/api/v1.0/users/add', data=json.dumps(payload), headers=headers)

    print(res.text)

def get_token(email, password):
    with open('pub_key.pem', mode='rb') as pub_file:
        keydata = pub_file.read()

    pub_key = rsa.PublicKey.load_pkcs1(keydata)
    message = email + ':' + password

    res = requests.get('http://127.0.0.1:5000/api/v1.0/token',  auth=HTTPBasicAuth(email, password))

    print(res.text)
    print(res.headers)
    return json.loads(res.text)


def token_login(token):
    res = requests.get('http://127.0.0.1:5000/api/v1.0/token', auth=HTTPBasicAuth(token, ''))

    print(res.text)

def call_api(token):
    res = requests.get('http://127.0.0.1:5000/api/v1.0/users/login_test', auth=HTTPBasicAuth(token, ''))
    print(res.text)


def reset_password(token, password):
    with open('pub_key.pem', mode='rb') as pub_file:
        keydata = pub_file.read()

    pub_key = rsa.PublicKey.load_pkcs1(keydata)
    message = password
    crypto = rsa.encrypt(message.encode(), pub_key)

    payload = {"data": binascii.hexlify(crypto).decode()}
    headers = {
        'content-type': 'application/json',
        'charset': 'utf-8',
    }

    res = requests.post('http://127.0.0.1:5000/api/v1.0/users/reset_password', data=json.dumps(payload), headers=headers, auth=HTTPBasicAuth(token, ''))


def reset_username(token, username):
    with open('pub_key.pem', mode='rb') as pub_file:
        keydata = pub_file.read()

    pub_key = rsa.PublicKey.load_pkcs1(keydata)
    message = username
    crypto = rsa.encrypt(message.encode(), pub_key)

    payload = {"data": binascii.hexlify(crypto).decode()}
    headers = {
        'content-type': 'application/json',
        'charset': 'utf-8',
    }

    res = requests.post('http://127.0.0.1:5000/api/v1.0/users/reset_username', data=json.dumps(payload), headers=headers, auth=HTTPBasicAuth(token, ''))


if __name__ == '__main__':
    #res = get_token('test@bora.com', 'test')
    #user_add('test2@bora.com', 'test2')

    #token_login(res['token'])
    token = 'eyJpYXQiOjE0ODIyMjAwMjcsImV4cCI6MTQ4MjIyMzYyNywiYWxnIjoiSFMyNTYifQ.eyJpZCI6MTR9.qXiuf098l2Nz8Jp3PH6K0bDL8b60sLMb4GSGsIWSLRs'
    reset_username(token, 'jolsem')
    #reset_password(token, 'test')
    #call_api(token)

    '''
    pub_key, priv_key = rsa.newkeys(2048)
    f = open('pub_key.pem', 'w')
    f.write(pub_key.save_pkcs1(format='PEM').decode())
    f.close()

    f = open('priv_key.pem', 'w')
    f.write(priv_key.save_pkcs1(format='PEM').decode())
    f.close()
    '''
