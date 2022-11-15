from flask import Flask
import requests
import time

import execjs
from bs4 import BeautifulSoup
import re

app = Flask(__name__)


# 视图函数
@app.route('/')
def index():
    session = requests.session()
    username = "41723051"
    password = "swufe123"
    session = login(session, username, password)
    res = baobei(session)
    return r'<h1>Hello from swufe: %s </h1>' % res.text


@app.route('/login/')
def login(session, username, password):
    url = 'https://authserver.swufe.edu.cn/authserver/login'
    crypt = session.get("https://authserver.swufe.edu.cn/authserver/custom/js/encrypt.js").text
    encrypt = execjs.compile(crypt)
    authserver = requests.get(url)
    bs = BeautifulSoup(authserver.content, "html.parser")
    bs = bs.find('div', {'tabid': "01"})
    bs = bs.find_all('input', {'type': "hidden"})

    dist = {}
    for i in bs:
        try:
            dist[re.search('(?<=name=").*?(?=")', str(i)).group()] = re.search('(?<=value=").*?(?=")', str(i)).group()
        except:
            dist[re.search('(?<=id=").*?(?=")', str(i)).group()] = re.search('(?<=value=").*?(?=")', str(i)).group()
    enPassword = encrypt.call("encryptAES", password, dist["pwdDefaultEncryptSalt"])
    data = {
        "username": username,
        "password": enPassword,
        "lt": dist["lt"],
        "dllt": dist["dllt"],
        "execution": dist["execution"],
        "_eventId": dist["_eventId"],
        "rmShown": dist["rmShown"]
    }
    session.post(url, data=data, cookies=authserver.cookies)
    return session


@app.route('/baobei/')
def baobei(session):
    url = 'https://qxj.iswufe.info/QJ/XSBBList'
    info = session.get(url)
    bs = BeautifulSoup(info.content, "html.parser")
    bs1 = bs.find_all('div', {'class': "col-6 col-md-3"})
    bs2 = bs.find_all('label', {'id': "fdyid"})
    dist = {}
    for i in bs1:
        key = re.search('(?<=id=").*?(?=")', str(i)).group()
        if key in dist.keys():
            continue
        dist[key] = re.search('(?<=">).*?(?=</span>)', str(i)).group()
    now = time.strftime("%H:%M", time.localtime(int(time.time()) - 3 * 60))
    end = time.strftime("%H:%M", time.localtime(int(time.time()) + 30 * 60))
    dist['qjlx'] = "5"
    dist['qjkssj'] = now
    dist['qjjssj'] = end
    dist['qjyy'] = "吃饭"
    dist['mdd'] = "东门"
    dist['qjxc'] = "步行"
    dist['upTemp'] = ""
    dist[re.search('(?<=id=").*?(?=")', str(bs2[0])).group()] = re.search('(?<=">).*?(?=</label>)', str(bs2[0])).group()
    dist['bbfw'] = "1"
    url = 'https://qxj.iswufe.info/QJ/InsertStuBB'
    baobei_res = session.post(url, data=dist, cookies=info.cookies)
    return baobei_res


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
