import configparser
import time
import re
import datetime
import logging
import requests
import argparse

login_url = 'https://ndl-vitv.khpi.edu.ua/login/index.php?'


def work_with_cmd_prompt() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Moodle parser')
    parser.add_argument('-p', "--password", type=str, help="Password flag")
    parser.add_argument('-l', "--login", type=str, help="Login flag")
    parser.add_argument('-n', "--no-logs", action='store_true', help="Show logs in commands line")
    args = parser.parse_args()
    return args


def get_login_password(args: argparse.Namespace) -> (str, str):
    if args.login is None:
        try:
            config = configparser.ConfigParser()
            config.read('config.conf')
            login = config['user_info']['login']
            password = config['user_info']['password']
            return login, password
        except:
            raise Exception("Check config or use cmd arguments")
    elif args.login is not None and args.password is not None:
        return args.login, args.password
    else:
        raise Exception("login and password not found")


if __name__ == "__main__":

    logging.basicConfig(filename='info.log', filemode='w', level=logging.INFO)

    args = work_with_cmd_prompt()
    login, password = get_login_password(args)
    no_logs_flag: bool = True if args.no_logs else False

    now = datetime.datetime.now()

    with open("links.txt") as fp:
        links_list = fp.readlines()

    with requests.Session() as session:
        r_1 = session.get(url=login_url)
        pattern_auth = '<input type="hidden" name="logintoken" value="\w{32}">'
        token = re.findall(pattern_auth, r_1.text)
        token = re.findall("\w{32}", token[0])[0]
        payload = {'anchor': '', 'logintoken': token, 'username': login, 'password': password, 'rememberusername': 1}
        r_2 = session.post(url=login_url, data=payload)
        counter = 0
        log_err = False
        for i in r_2.text.splitlines():
            if "loginerrors" in i or (0 < counter <= 3):
                counter += 1
                print(i)
                log_err = True
            if "page-my-index" in i:
                print('Successfully log in')
        if log_err:
            print("ERROR! Cannot log in!")
            assert ()

        while True:
            now = datetime.datetime.now()
            begin = now.replace(hour=9, minute=0, second=0, microsecond=0)
            end = now.replace(hour=15, minute=40, second=0, microsecond=0)
            if begin < now < end:
                for link in links_list:
                    session.get(link)
                    logging.info(f'{link} - {now}')
                    if not no_logs_flag:
                        print(f'{link} - {now}')
                    time.sleep(10)
            else:
                session.get("https://ndl-vitv.khpi.edu.ua/my/")
                logging.info(f'https://ndl-vitv.khpi.edu.ua/my/ - {now}')
                if not no_logs_flag:
                    print(f'https://ndl-vitv.khpi.edu.ua/my/ - {now}')
            time.sleep(240)