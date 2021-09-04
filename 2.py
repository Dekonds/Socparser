import datetime
import time
import gc
import requests
from bs4 import BeautifulSoup


HEADERs = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4297.0 Safari/537.36',
    'accept': '*/*'}


def get_html(url, params=None):
    s = requests.Session()
    # print(url)
    r = s.get(url, \
              cookies={
                    'session_id': '8FBABDE6-234F-1F13-FB17-053A557F4BCC', \
                    'user_data': 'a%3A0%3A%7B%7D', \
                    'secret': '8595BB40-D44C-BE89-3A53-2FCE2D95184F'},
            headers=HEADERs
              )
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    classes = soup.find_all("div", class_="left")
    now = datetime.datetime.now()
    if (len(classes) == 0):
        print(str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + " No visits "+"Memory  " )
        time.sleep(300)
        gc.collect()
        #parse()
        return
    typeoflink = str(classes[1]).split()[8]
    link = classes[0].findChildren()[1].attrs.get("href")

    if (typeoflink == 'страницы'):
        print(str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + " " + link + " direct")
        time.sleep(10)
    else:
        print(str(now.hour)+ ":" + str(now.minute) + ":" + str(now.second) + " " + link + " " + typeoflink)
        time.sleep(int(typeoflink) + 10)
    get_html(link + "&act=redirect")
    #print("Memory " + str(memory_usage()))
    gc.collect()
    #parse()
    # f = open('parse.html', 'w', encoding='utf-8')


def parse():
    url = 'https://socpublic.com/account/visit.html'
    html = get_html(url)
    get_content(html.text)


def getip():
    html = get_html("https://ipwhois.app/json/")
    print(html.text.split('"')[3])


def main():
    getip()
    while 10 > 1:
        parse()
        gc.collect()

print("")

main()

