import asyncio
import datetime
import random
import time
import gc
import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import multiprocessing

#hui
no_visits = True
HEADERs = {
    'user-agent': 'Mozilla/5.1 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 YaBrowser/21.5.3.742 Yowser/2.5 Safari/537.36',
    'accept': '*/*'}

with open('data.json') as jsonFile:
    data = json.load(jsonFile)['users']



def get_content(UserNumber):
    now = datetime.datetime.now()
    global no_visits
    html = requests.Session().get('http://socpublic.com/account/visit.html', cookies={'session_id': data[UserNumber]['cookie']}, headers=HEADERs,
                               proxies={'http:': data[UserNumber]['proxy']}).text
    soup = BeautifulSoup(html, 'html.parser')
    classes = soup.find_all("div", class_="left")
    name = soup.find('span', class_='username')
    if name is None:
        print('Not Logget'+data[UserNumber]['name'])
        return 0
    if len(classes) == 0:
        #print(f"{0} {1}".format(user_number,len(classes)))
        if no_visits:
            #print(str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + " No visits "+name.text)
            print("{0}:{1}:{2} No visits {3}".format(now.hour,now.minute,now.second,name.text))
            no_visits = False
        time.sleep(2)
        no_visits = False
        gc.collect()
        return
    typeoflink = str(classes[1]).split()[8]
    link = classes[0].findChildren()[1].attrs.get("href")
    if typeoflink == 'страницы':
        print(str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + " " + link + " direct " +name.text)
        requests.Session().get( link+'&act=redirect', cookies={'session_id': data[UserNumber]['cookie']},
                               headers=HEADERs,
                               proxies={'http:': data[UserNumber]['proxy']})
        time.sleep(2)
    else:
        print(str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + " " + link + " " + typeoflink+ " "+name.text)
        requests.Session().get(link+'&act=redirect', cookies={'session_id': data[UserNumber]['cookie']},
                               headers=HEADERs,
                               proxies={'http:': data[UserNumber]['proxy']})
        time.sleep(int(typeoflink) + 10)
    no_visits = True


def parse(user_number):
    while True:
        var = get_content(user_number)
        gc.collect()
        if var == 0:
            print('Exitins cycle'+str(user_number))
            break


def get_ip(user_number):
    print(data[user_number]['proxy'])
    response = requests.get('http://api.ipify.org', proxies={'http': data[user_number]['proxy']})  # узнать ip
    print(response.text)


def selenium_browser(user_bumber):
    # список адресов DNS серверов
    dns_servers = ['8.8.8.8', '8.8.4.4']

    # преобразование списка в строку для настройки Firefox-опций
    dns_str = ','.join(dns_servers)

    # инициализация Firefox-опций
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.set_preference('network.dns.forceResolve', True)
    firefox_options.set_preference('network.dns.disablePrefetch', True)
    firefox_options.set_preference('network.dns.disableIPv6', True)
    firefox_options.set_preference('network.dnsCacheEntries', 20)
    firefox_options.set_preference('network.dnsCacheExpiration', 300)
    firefox_options.set_preference('network.dnsCacheExpirationGracePeriod', 3600)
    firefox_options.set_preference('network.dns.localDomains', '')
    firefox_options.set_preference('network.dns.server', dns_str)

    driver = webdriver.Firefox(options=firefox_options)


    proxy = Proxy({
        'proxyType': ProxyType.MANUAL,
        'httpProxy': '185.15.172.212:3128',
        'sslProxy': '185.15.172.212:3128',
    })
    firefox_options = webdriver.FirefoxOptions()
    proxy.add_to_capabilities(firefox_options.to_capabilities())
    webdriver.Firefox(options=firefox_options)


def auto_task(taskid, response_text):
    requests.session().post('http://socpublic.com/task.ajax?act=task_start', cookies={'session_id': data[0]['cookie']},
                            data={'id': taskid})
    time.sleep(1)
    requests.Session().post(f'http://socpublic.com/account/task_view.html?id={taskid}&act=report',
                            cookies={'session_id': data[0]['cookie']},
                            data={'text': f'{response_text}', 'report': '1'})



#http://socpublic.com/task.ajax?act=task_start
#print(html.text)
#selenium_browser(1)

if __name__ == '__main__':
    for i in range(2):
        multiprocessing.Process(target=parse, args=(i,)).start()
        time.sleep(1)
