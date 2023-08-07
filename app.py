import unittest

from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time



fichas = input("cuantas fichas cargo: ")
jugador = input("escribe aqui el usuario: ")
id = input("escribe aqui el id: ")

options = webdriver.ChromeOptions()
chrome_driver = webdriver.Chrome(options=options)

chrome_driver.get("https://agentes.ganaencasa.co/account/login")

time.sleep(8)

element = chrome_driver.find_element("name", "userNameOrEmailAddress")
element.send_keys("Francoo")

element = chrome_driver.find_element("name", "password")
element.send_keys("Gokussj99")

chrome_driver.find_element('xpath', '//*[@id="kt_login"]/div/div[2]/div[2]/ng-component/div/form/div[3]/button').click()

time.sleep(2)

chrome_driver.get("https://agentes.ganaencasa.co/app/admin/usersManage/0")

playerid = elements_with_id = chrome_driver.find_elements('name', 'playerId')

print(playerid)


time.sleep(5)
buscador = chrome_driver.find_element('name', 'filterText')
busqueda = jugador
time.sleep(1)
buscador.send_keys(busqueda)

time.sleep(5)
chrome_driver.find_element('xpath', '//*[@id="btn_search"]').click()

time.sleep(5)
dinero_element = chrome_driver.find_element('xpath', f'//*[@id="itemBlc__{jugador}"]/div')
dinero_text = dinero_element.get_attribute("textContent").replace(",", ".")
print(dinero_text)

if dinero_text == "0.00":
    dinero_text = int(0)

time.sleep(2)
chrome_driver.find_element('xpath', f'//*[@id="item__{jugador}__1__10034057__{dinero_text}__{id}__ARS"]').click()

time.sleep(5)

element = chrome_driver.find_element("name", "monto")
element.send_keys(fichas)
time.sleep(5)
chrome_driver.find_element('xpath', '/html/body/app-root/ng-component/div/default-layout/div/div[2]/div/div[2]/div[2]/div[1]/app-users-manage/div/deposit-modal/div/div/div/form/div[3]/button[2]').click()
time.sleep(1)
chrome_driver.find_element('xpath', '/html/body/div/div/div[3]/button[1]').click()


time.sleep(10)
 






