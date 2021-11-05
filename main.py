import configparser
import time
import re
import datetime
import logging

import requests


logging.basicConfig(filename='info.log', filemode='w', level=logging.INFO)

config = configparser.ConfigParser()
config.read('config.conf')
login = config['user_info']['login']
password = config['user_info']['password']

lessons = dict(config.items('lessons'))
print(lessons)

now = datetime.datetime.now()

first = now.replace(hour=22, minute=20, second=0, microsecond=0)

second = now.replace(hour=22, minute=40, second=0, microsecond=0)

third = now.replace(hour=23, minute=0, second=0, microsecond=0)

fourth = now.replace(hour=23, minute=20, second=0, microsecond=0)

end = now.replace(hour=23, minute=40, second=0, microsecond=0)

login_url = 'https://ndl-vitv.khpi.edu.ua/login/index.php?'

user_values = {'username': login, 'password': password}
test_url = 'https://ndl-vitv.khpi.edu.ua/my/'

with requests.Session() as session:
    r_1 = session.get(url=login_url)
    pattern_auth = '<input type="hidden" name="logintoken" value="\w{32}">'
    token = re.findall(pattern_auth, r_1.text)
    token = re.findall("\w{32}", token[0])[0]
    payload = {'anchor': '', 'logintoken': token, 'username': login, 'password': password, 'rememberusername': 1}
    r_2 = session.post(url=login_url, data=payload)
    for i in r_2.text.splitlines():
        if "<title>" in i:
            print(i[15:-8:])
            break
    counter = 0
    for i in r_2.text.splitlines():
        if "loginerrors" in i or (0 < counter <= 3):
            counter += 1
            print(i)

    while now < end:
        now = datetime.datetime.now()

        if first < now < second:
            session.get(lessons['first'])
            logging.info(f'first:  {lessons["first"]} - {now}')
        elif second < now < third:
            session.get(lessons['second'])
            logging.info(f'second:  {lessons["second"]} - {now}')
        elif third < now < fourth:
            session.get(lessons['third'])
            logging.info(f'third:  {lessons["third"]} - {now}')
        else:
            session.get(lessons['fourth'])
            logging.info(f'fourth:  {lessons["fourth"]} - {now}')
        time.sleep(240)
        now = datetime.datetime.now()
