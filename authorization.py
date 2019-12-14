from selenium import webdriver
from time import sleep
import requests
import json
from web import config
info = config.config
if info["yourserver"] == "开发服" :
    login_home = "********************"
elif info["yourserver"] == "预发布服":
    login_home = "********************"
else:
    login_home = "********************"

authorization = ""
if info["platform"] == "**系统":
    opt = webdriver.ChromeOptions()
    opt.headless = True
    browser = webdriver.Chrome(options=opt)
    browser.get(login_home)
    sleep(2)
    login_name = browser.find_element_by_xpath('//*[@id="app"]/div/div/div[3]/div/form/div[1]/div/div/input')
    login_pass = browser.find_element_by_xpath('//*[@id="app"]/div/div/div[3]/div/form/div[2]/div/div/input')
    login_name.clear()
    login_name.send_keys(info["name"])
    login_pass.clear()
    login_pass.send_keys(info["password"])
    browser.find_elements_by_class_name("***-button")[0].click()
    sleep(2)
    authorization = "**** "+ str(browser.get_cookies()[2]["value"])

# if info["platform"] == "客户端":
#     s = requests.Session()
#     url = '********************'
#     params = {"password":"********************","phone":"********************"}
    
#     data = json.dumps(params)
#     headers = {
#         'Content-Type': "application/x-www-form-urlencoded;charset=UTF-8",
#     }
#     r = s.post(url,data=data,headers=headers)
#     print(r.status_code)
#     print(r.url)
#     print(r.json())

