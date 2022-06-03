from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import smtplib
from email import message
import datetime
import time





def login(driver,n):
    driver_log = ""
    flag = 0
    for _ in range(3):
        try:
            WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located)
            id_box = driver.find_element(By.XPATH,"/html/body/form/div/input[1]")
            id_box.send_keys("USERID")
            pw_box = driver.find_element(By.XPATH,"/html/body/form/div/input[2]")
            pw_box.send_keys("PASSWORD")
            pw_box.submit()
        except Exception as e:
            dt_now =datetime.datetime.now()
            driver_log = driver_log + str(dt_now) + "   driver_"  + str(n) +  " LOGIN ERROR\n"
            return driver_log,flag
        else:
            WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located)
            try:
                user_name = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH,"/html/body/div[2]/div[1]/div[2]")))
            except Exception as e:
                dt_now = datetime.datetime.now()
                driver_log = driver_log + str(dt_now) + "   driver_" + str(n) + " 503 ERROR(login)\n"
                return driver_log, flag
            else:
                if user_name.text != "高専太郎 様":
                    dt_now = datetime.datetime.now()
                    driver_log = driver_log + str(dt_now) + "   driver_" + str(n) + " 503 ERROR(login)\n"
                    return driver_log, flag
                dt_now = datetime.datetime.now()
                driver_log = driver_log + str(dt_now) + "   driver_" + str(n) +  " LOGIN SUCCESSFULLY\n"
                flag = n
                break
    return driver_log,flag   

def wait_updating(driver,n):
    #キャンセル予約ページへ
    driver_log = ""
    dt_now = datetime.datetime.now()
    cancel_bm = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH,"/html/body/div[3]/form[3]/input[1]")))
    cancel_bm.click()
    flag = 0
    #キャンセル待ち予約ページ
    for _ in range(20):
        try:
            #ページの日付を取得
            WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located)
            #wdate = WebDriverWait(driver,3).until(EC.visibility_of_element_located((By.XPATH,"/html/body/div[2]/ul/li[2]")))
            wdate = driver.find_element(By.XPATH,"/html/body/div[2]/ul/li[2]")
        except Exception as e:
            #取得に失敗したら再読み込み
            dt_now = datetime.datetime.now()
            driver_log = driver_log + str(dt_now) + "   driver_" + str(n) + " PROBABLY 503 ERROR(get_date)\n"
            driver.refresh()
            continue
        else:
            #日付があっていればループから抜ける
            if  dt_now.day == int(wdate.text[3:5]):
                flag = n
                dt_now = datetime.datetime.now()
                driver_log = driver_log + str(dt_now) + "   driver_" + str(n) + " FOUND TODAY'S PAGE!!\n"
                break
            #日付があっていなければ再読み込み
            else:
                for _ in range(10):
                    try:
                        driver.refresh()
                    #再読み込みに失敗したらドライバを変更する。
                    except Exception as e:
                        dt_now = datetime.datetime.now()
                        driver_log = driver_log + str(dt_now) + "   driver" + str(n) + " PROBABLY 503 ERROR(reload)\n"
                        flag = 0
                        return driver_log, flag
                    else:
                        break
                continue
    return driver_log,flag

def push_bm(driver,n):
    i = 2
    flag = n
    driver_log = ""
    t = 0
    while i < 5:
        try:
            cancel_bm = driver.find_element(By.XPATH,"/html/body/div[2]/form/div[1]/table/tbody/tr["+str(i)+"]/td[2]/label")
            driver.execute_script("arguments[0].click();",cancel_bm)
        except Exception as e:
            dt_now = datetime.datetime.now()
            driver_log = driver_log + str(dt_now) + "   driver_" + str(n) +  " BTN" + str(i) + " CLICK ERROR\n"
            if i == 4 and t == 0:
                flag = 0
                return driver_log,flag
            i += 1
            continue
        else:
            dt_now = datetime.datetime.now()
            driver_log = driver_log + str(dt_now) + "   driver_" + str(n) +  " BTN" +str(i) + " CLICKED!!\n"
            t = 1
            i += 1
            continue
    return driver_log,flag
#更新ボタンを押す
def submit(driver,n):
    flag = n
    driver_log =""
    for _ in range(3):
        try:
            #更新ボタンを押す
            submit_bm = driver.find_element(By.XPATH,"/html/body/div[2]/form/input[1]")
            driver.execute_script("arguments[0].click();",submit_bm)
        except Exception as e:
            #失敗すればもう一度
            flag = 0
            dt_now = datetime.datetime.now()
            driver_log = driver_log + str(dt_now) + "   driver_" + str(n) + " PUSH SUBMIT BTN ERROR\n"
            driver.refresh()
            continue
        else:
            #成功したらループを抜ける
            dt_now = datetime.datetime.now()
            driver_log = driver_log + str(dt_now) + "   driver_" + str(n) + " PUSHED SUBMIT BTN\n"
            break
    for _ in range(5):
        try:
            #提出が成功したかの確認
            WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located)
            #wdate = WebDriverWait(driver,3).until(EC.visibility_of_element_located((By.XPATH,"/html/body/div[2]/ul/li[2]")))
            wdate = driver.find_element(By.XPATH,"/html/body/div[2]/ul/li[2]")
        except Exception as e:
            #失敗すればもう一度
            flag = 0
            dt_now = datetime.datetime.now()
            driver_log = driver_log + str(dt_now) + "   driver_" + str(n) + " 503 ERROR(submit)\n"
            driver.back()
            WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located)
            submit_bm = driver.find_element(By.XPATH,"/html/body/div[2]/form/input[1]")
            driver.execute_script("arguments[0].click();",submit_bm)
            continue
        else:
            #成功すればループから抜ける
            flag = n
            dt_now = datetime.datetime.now()
            driver_log = driver_log + str(dt_now) + "   driver_" + str(n) + " COMPLETED PROCESSING!!\n"
            return driver_log, flag
    return driver_log,flag
    

