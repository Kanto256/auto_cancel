import requests
import time
import datetime
import re
import smtplib
from email import message
payload = {
    "ID": "*******",
    "Pass": "******",
    "APPNAME": "NK-YOYAKU",
    "PRGNAME": "chkresult",
    "ARGUMENTS": "ID,Pass",
    "SP": "1"
  }
html_num = 0
log = ""
login_url = "http://203.152.207.3/Scripts/MGrqispi015.dll?APPNAME=NK-YOYAKU&PRGNAME=sslogin"
#login the page
for _ in range(3):
    r = requests.post(login_url,data = payload)
    r.encoding = r.apparent_encoding
    print(r.text)
    with open(str(html_num) + ".html",mode = 'w') as f:
        f.write(r.text)
    html_num += 1
    if type(re.search(r'<input value="([0-9]+)" type="hidden" name="CTXT',r.text).groups()[0]) == str:
        dt_now = datetime.datetime.now()
        log = log + str(dt_now) + " login successfully\n"
        break
    else:
        dt_now = datetime.datetime.now()
        log = log + str(dt_now) + " login error\n"

CTXT =  re.search(r'<input value="([0-9]+)" type="hidden" name="CTXT',r.text).groups()[0]
DATE =  re.search(r'<input value="([0-9]+)" type="hidden" name="DATE',r.text).groups()[0]
#wait for time is coming
while 1:
    dt_now = datetime.datetime.now()
    if dt_now.minute *  60 + dt_now.second > 135 and dt_now.minute != 59:
        break
    time.sleep(1)

home_url = "http://203.152.207.3/Scripts/mgrqispi015.dll"

payload = {
    "APPNAME": "NK-YOYAKU",
    "PRGNAME": "waitinglist",
    "CTXT": CTXT,
    "DATE": DATE
  }

#wait for waiting list updated
for _ in range(30):
    for _ in range(10):
        r = requests.post(home_url,data = payload)
        r.encoding = r.apparent_encoding
        print(r.text)
        with open(str(html_num) + ".html",mode = 'w') as f:
            f.write(r.text)
        html_num += 1
        if type(re.search(r'3月([0-9]+)日',r.text).groups()[0]) == str:
            break
        else:
            dt_now = datetime.datetime.now()
            log = log + str(dt_now) + " 503 errror (access waiting list)\n"
            continue
    day =  re.search(r'3月([0-9]+)日',r.text).groups()[0]
    if day == str(dt_now.day):
        dt_now = datetime.datetime.now()
        log = log + str(dt_now) + " found today's page\n"
        break
    else:
        print(" page updated yet\n")

#apply for waiting list
payload = {
    "WL02" : "1",
    "WL03" : "1",
    "WL04" : "1",
    "APPNAME": "NK-YOYAKU",
    "PRGNAME": "waitinglist",
    "CTXT": CTXT,
    "DATE": str(int(DATE)+1),
    "TARDATE": str(int(DATE)+1)
  }

for _ in range(3):
    r = requests.post(home_url,data = payload)
    r.encoding = r.apparent_encoding
    print(r.text)
    with open(str(html_num) + ".html",mode = 'w') as f:
        f.write(r.text)
    html_num += 1
    if re.search(r'3月([0-9]+)日',r.text).groups()[0] == str(dt_now.day):
        dt_now = datetime.datetime.now()
        log = log + str(dt_now) + " apply to waiting list succcessfully\n"
        break
    else:
        dt_now = datetime.datetime.now()
        log = log + str(dt_now) + " 503 errror (apply to waiting list)\n"

print(log)

host = 'smtp.gmail.com'
port = 587
f_email = '**********@gmail.com'
t_email = '********@sample.com'
password = '*********'

msg = message.EmailMessage()


msg.set_content(log)
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
        log = log + str(dt_now) + "   MAIL SEVER: LOGIN ERROR\n"
        sever.ehlo()
        sever.starttls()
        sever.ehlo()
    else:
        dt_now = datetime.datetime.now()
        log = log + str(dt_now) + "   MAIL SEVER: LOGIN SUCCESSFLLUY\n"
        break

for _ in range(3):
    try:
        sever.send_message(msg)
    except Exception as e:
        dt_now = datetime.datetime.now()
        log = log + str(dt_now) + "   MAIL SEVER: SENDING MSG ERROR\n"
        sever.ehlo()
        sever.starttls()
        sever.ehlo()
        sever.login(f_email,password)
    else:
        dt_now = datetime.datetime.now()
        log = log + str(dt_now) + "   MAIL SEVER: SEND EMAIL\n"
        break
sever.quit()
time.sleep(5000)
with open('driver_log.txt',mode = 'w') as f:
    f.write(log)






