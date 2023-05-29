import datetime
import time
import gc
import requests
import json
from bs4 import BeautifulSoup

no_visits = True

HEADERs = {'user-agent': 'Mozilla/5.1 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 YaBrowser/21.5.3.742 Yowser/2.5 Safari/537.36','accept': '*/*'}
proxys = {
  'http':'89.223.121.208:3128'
}

def get_html(url):
    jsonData = ""
    with open('data.json') as jsonFile:
        data = json.load(jsonFile)
        jsonData = data['users']
    s = requests.Session()
    #print(cookie_session)
    #print(jsonData[0]['cookie'])
    r = s.get(url, cookies={'session_id': jsonData[0]['cookie']},headers=HEADERs)#, proxies=proxys
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    classes = soup.find_all("div", class_="left")
    name = soup.find('span', class_='username')
    if type(name) == type(None):
        print('Not Logget')
        time.sleep(100)
        return
    now = datetime.datetime.now()
    global no_visits
    if len(classes) == 0:
        if no_visits == True:
            print(str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + " No visits")
            no_visits = False
        time.sleep(20)
        no_visits = False
        gc.collect()
        return
    typeoflink = str(classes[1]).split()[8]
    link = classes[0].findChildren()[1].attrs.get("href")
    if typeoflink == 'страницы':
        print(str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + " " + link + " direct")
        get_html(link + "&act=redirect")
        time.sleep(10)
    else:
        print(str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + " " + link + " " + typeoflink)
        get_html(link + "&act=redirect")
        time.sleep(int(typeoflink) + 10)
    no_visits = True
    gc.collect()
    parse()

def parse():
    url = 'http://socpublic.com/account/visit.html'
    html = get_html(url)
    get_content(html.text)
    gc.collect()




def main():
    while True:
        parse()
        gc.collect()



#session = requests.Session()
#session.proxies = {"http": "89.223.121.208:3128"}
#print("Страница запроса с IP:", session.get("http://ip.bablosoft.com/").text.strip())
main()
