from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import smtplib
from email import message
import datetime
import time
from auto_cancel_lib import login
from auto_cancel_lib import wait_updating
from auto_cancel_lib import push_bm
from auto_cancel_lib import submit

#Chrome Driverの設定
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--disable-extention') #拡張機能を無効化
options.add_argument('--proxy-sever="direct://"')#プロキシ経由しない
options.add_argument('--proxy-bypass-list=*')
options.add_argument('--start-maximized') #起動時にウィンドウを最大化

driver_1 = webdriver.Chrome(chrome_options = options) #上記の設定を挿入
driver_2 = webdriver.Chrome(chrome_options = options)
driver_3 = webdriver.Chrome(chrome_options = options)

driver_1.set_window_size('1828','935')
driver_2.set_window_size('1828','935')
driver_2.set_window_size('1828','935')

#ログインページへ
driver_1.get("http://203.152.207.3/Scripts/MGrqispi015.dll?APPNAME=NK-YOYAKU&PRGNAME=sslogin")
driver_2.get("http://203.152.207.3/Scripts/MGrqispi015.dll?APPNAME=NK-YOYAKU&PRGNAME=sslogin")
driver_3.get("http://203.152.207.3/Scripts/MGrqispi015.dll?APPNAME=NK-YOYAKU&PRGNAME=sslogin")

#エラー文の作成
driver_log = ""

#キャンセル待ちの実施を制御する。0なら続ける。
flag = 0
#driver_1をログインさせる
ms,flag = login(driver_1,1)
driver_log = driver_log + ms
dt_now = datetime.datetime.now()
driver_log = driver_log + str(dt_now) + "   wait for page updating...\n"
#ログインが失敗すればdriver_2をログインさせる
if flag == 0:
    driver_1.quit()
    ms,flag = login(driver_2,2)
    driver_log = driver_log + ms
#ログインが失敗すればdriver_3をログインさせる
if flag == 0:
    driver_2.quit()
    ms,flag = login(driver_3,3)
    driver_log = driver_log + ms
#6:00:45までまつ
while 1:
    dt_now = datetime.datetime.now()
    if dt_now.minute *  60 + dt_now.second > 75 and dt_now.minute != 59:
        break
    time.sleep(1)

dt_now = datetime.datetime.now()
driver_log = driver_log + str(dt_now) + "   START PROCESSING\n"


#driver_1を操作
if flag == 1:
    ms,flag = wait_updating(driver_1,1)
    driver_log = driver_log + ms
    if flag == 1:
        ms,flag = push_bm(driver_1,1)
        driver_log = driver_log + ms
    if flag == 1:
        ms,flag = submit(driver_1,1)
        driver_log = driver_log + ms

driver_1.quit()

#driver_2を操作(driver_1が失敗した場合)
if flag == 0:
    ms,flag = login(driver_2,2)
    driver_log = driver_log + ms
    if flag == 2:
        ms,flag = wait_updating(driver_2,2)
        driver_log = driver_log + ms
        if flag == 2:
            ms,flag = push_bm(driver_2,2)
            driver_log = driver_log + ms
        if flag == 2:
            ms,flag = submit(driver_2,2)
            driver_log = driver_log + ms
elif flag == 2:
    ms,flag = wait_updating(driver_2,2)
    driver_log = driver_log +ms
    if flag == 2:
        ms,flag = push_bm(driver_2,2)
        driver_log = driver_log + ms
    if flag == 2:
        ms,flag = submit(driver_2,2)
        driver_log = driver_log + ms



driver_2.quit()
#driver_3を操作(driver_1,2が失敗した場合)
if flag == 0:
    ms,flag = login(driver_3,3)
    driver_log = driver_log + ms
    if flag == 3:
        ms,flag = wait_updating(driver_3,3)
        driver_log = driver_log + ms
        if flag == 3:
            ms,flag = push_bm(driver_3,3)
            driver_log = driver_log + ms
        if flag == 3:
            ms,flag = submit(driver_3,3)
            driver_log = driver_log + ms
elif flag == 3:
    ms,flag = wait_updating(driver_3,3)
    driver_log = driver_log +ms
    if flag == 3:
        ms,flag = push_bm(driver_3,3)
        driver_log = driver_log + ms
    if flag == 3:
        ms,flag = submit(driver_3,3)
        driver_log = driver_log + ms

driver_3.quit()



host = 'smtp.gmail.com'
port = 587
f_email = 'nakatakennta4@gmail.com'
t_email = 'ic191237@edu.okinawa-ct.ac.jp'
password = 'a01s01k01'

msg = message.EmailMessage()


msg.set_content(driver_log)
msg['Subject'] = 'AUTO_CANCEL LOG'
msg['From'] = f_email
msg['To'] = t_email

sever = smtplib.SMTP(host,port)
sever.ehlo()
sever.starttls()
sever.ehlo()
for _ in range(3):
    try:
        sever.login(f_email,password)
    except Exception as e:
        dt_now = datetime.datetime.now()
        driver_log = driver_log + str(dt_now) + "   MAIL SEVER: LOGIN ERROR\n"
        sever.ehlo()
        sever.starttls()
        sever.ehlo()
    else:
        dt_now = datetime.datetime.now()
        driver_log = driver_log + str(dt_now) + "   MAIL SEVER: LOGIN SUCCESSFLLUY\n"
        break

for _ in range(3):
    try:
        sever.send_message(msg)
    except Exception as e:
        dt_now = datetime.datetime.now()
        driver_log = driver_log + str(dt_now) + "   MAIL SEVER: SENDING MSG ERROR\n"
        sever.ehlo()
        sever.starttls()
        sever.ehlo()
        sever.login(f_email,password)
    else:
        dt_now = datetime.datetime.now()
        driver_log = driver_log + str(dt_now) + "   MAIL SEVER: SEND EMAIL\n"
        break
sever.quit()

#ログファイルへの書き込み
with open('driver_log.txt',mode = 'w') as f:
    f.write(driver_log)