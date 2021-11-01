import datetime
import time
import gc
import requests
import json
from bs4 import BeautifulSoup

coutofparser = 99
no_visits = True

HEADERs = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 YaBrowser/21.5.3.742 Yowser/2.5 Safari/537.36',
    'accept': '*/*'}

def get_html(url, params=None):
    f = open('cfg', 'r')
    strings = f.read()
    splitss = strings.split("\n")
    global coutofparser
    #print(coutofparser)
    s = requests.Session()
    #print(splitss[coutofparser].split(" ")[1])
    r = s.get(url, \
              cookies={
                  'session_id': splitss[coutofparser].split(" ")[2],  #'1952AD09-578E-FCDB-62BC-C71C86E74CBC', splitss[coutofparser].split(" ")[2]
                  'secret': splitss[coutofparser].split(" ")[3]     #'EEC5222B-AEFE-96B3-9125-1928512E7C5B' splitss[coutofparser].split(" ")[3]
                  },
              headers=HEADERs
              )
    return r

def get_html_ip(url, params=None):
    s = requests.Session()
    r = s.get(url,
              headers=HEADERs
              )
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    classes = soup.find_all("div", class_="left")
    now = datetime.datetime.now()
    #f = open("file.html",'w',encoding = 'utf-8')
    #f.write(html)
    #f.close()
    global no_visits
    if (len(classes) == 0):
        if (no_visits == True):
            print(str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + " No visits")
            no_visits = False
        else:
            print("visits false")
        time.sleep(20)
        no_visits = False
        gc.collect()
        return
    typeoflink = str(classes[1]).split()[8]
    link = classes[0].findChildren()[1].attrs.get("href")
    if (typeoflink == 'страницы'):
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


def get_content_username(html):
    soup = BeautifulSoup(html, 'html.parser')
    classes = soup.find("span", class_="username")
    print("username on site " + classes.contents[0])


def parse():
    url = 'https://socpublic.com/account/visit.html'
    html = get_html(url)
    get_content(html.text)
    gc.collect()


def getip():
    html = get_html_ip("https://ipwhois.app/json/")
    ip_json = json.loads(html.text)
    print("asn: "+str(ip_json['asn']))
    print('ip: '+ip_json['ip'])
    f = open('cfg', 'r')
    strings = f.read()
    cfg_file = strings.split("\n")
    for s in cfg_file:
        file_line = s.split(" ")
        print(file_line[0]+" "+str(ip_json['asn']))
        if (file_line[0] in str(ip_json['asn'])):
            global coutofparser
            coutofparser = cfg_file.index(s)
            print("Logging as " + file_line[1])
            break
    html2 = get_html('https://socpublic.com/account/visit.html')
    get_content_username(html2.text)


def main():
    getip()
    while True:
        parse()
        gc.collect()


def maintest():
    global coutofparser
    while True:
        for x in range(1, 3):
                coutofparser = x
                parse()
                gc.collect()

print("")
main()
#maintest()
