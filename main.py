from fastapi import FastAPI
from bs4 import BeautifulSoup 
from fastapi.middleware.cors import CORSMiddleware
import pyuser_agent
import requests

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_number(td):
    x = str(td)
    x = x.split('\n')[1].strip(' ')
    x = x.split('\r')[0]
    x = x.strip(' ')
    x = x.strip('%')
    return x

def get_data():
    user = pyuser_agent.UA()
    headers = {'user-Agent': user.random}
    session = requests.Session()
    request = session.get(url='https://tradingeconomics.com/stocks', timeout=30, headers=headers)
    soup = BeautifulSoup(request.text, 'html.parser')
    tbodies = soup.find_all('tbody')
    Europe = tbodies[1].find_all('td')
    Americas = tbodies[2].find_all('td')
    Asia = tbodies[3].find_all('td')
    Australia = tbodies[4].find_all('td')
    Africa = tbodies[5].find_all('td')

    payload = {}

    europes = [('UK', 5), ('Germany', 15), ('France', 25), ('Italy', 35), ('Spain', 45), ('Russia', 55),
            ('Turkey', 75), ('Sweden', 95), ('Poland', 105), ('Norway', 125), ('Austria', 135), ('Denmark', 145),
            ('Finland', 155)]
    for europe in europes:
        payload[europe[0]] = get_number(Europe[europe[1]])
        
    americas = [('USA', 15), ('Ecuador', 35), ('Canada', 45), ('Brazil', 55), ('Mexico', 65), ('Peru', 75),
            ('Argentina', 85), ('Venezuela', 95), ('Colombia', 105), ('Chile', 115)]
    for america in americas:
        payload[america[0]] = get_number(Americas[america[1]])
        
    asias = [('Japan', 5), ('China', 25), ('India', 55), ('Bangladesh', 65), ('Indonesia', 75), ('Saudi Arabia', 85),
            ('Taiwan', 95), ('Thailand', 115), ('Malaysia', 125), ('Philippines', 165), ('Pakistan', 175),
            ('Kazakhstan', 185), ('Vietnam', 215)]
    for asia in asias:
        payload[asia[0]] = get_number(Asia[asia[1]])
        
    australias = [('Australia', 5), ('New Zealand', 35)]
    for australia in australias:
        payload[australia[0]] = get_number(Australia[australia[1]])
        
    africas = [('Nigeria', 5), ('South Africa', 15), ('Egypt', 35), ('Morocco', 45), ('Kenya', 65), ('Tanzania', 75),
            ('Tunisia', 85), ('Ghana', 95), ('Mauritius', 105), ('Uganda', 115), ('Namibia', 125), ('Botswana', 135),
            ('Zimbabwe', 145)]
    for africa in africas:
        payload[africa[0]] = get_number(Africa[africa[1]])

    return payload



@app.get('/')
def make_map_data():
    data = get_data()
    return data

