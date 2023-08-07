import time
from flask import Flask, render_template, request
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import mercadopago
import pandas as pd
import math

app = Flask(__name__)
app.static_folder = 'static'

jugador = None
fichas = None

def buscar_jugador(jugador):
    ruta_archivo_excel = 'libro1.xlsx'
    data_frame = pd.read_excel(ruta_archivo_excel)
    return jugador not in data_frame['jugador'].values  

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST', 'GET'])
def submit():   
    data = request.form.to_dict()
    
    global jugador
    jugador = data.get("jugador")
    global fichas
    fichas = data.get("fichas")
    
    def contiene_letras(fichas):
        if isinstance(fichas, str):
            return any(caracter.isalpha() for caracter in fichas)
        else:
            return False
    
    def es_numero_decimal(fichas):
        try:
            float_numero = float(fichas)
            if '.' in fichas or ',' in fichas:
                return True  # Tiene decimales, es un número decimal.
            else:
                return False
        except ValueError:
            return False
        
    if es_numero_decimal(fichas):
        return render_template('index.html', mensaje="No puedes ingresar numeros decimales")
    elif contiene_letras(fichas):
        return render_template('index.html', mensaje="Solo puedes ingresar numeros")
    else:  
        fichas_l = int(fichas)
    
    if buscar_jugador(jugador):
        return render_template('index.html', mensaje="El jugador no se encuentra registrado")
    elif fichas_l < int(500):
        return render_template('index.html', mensaje="El monto a cargar debe ser superior a $500")
    else:
        sdk = mercadopago.SDK("TEST-8601078490113141-072113-38464d5924c067498ab5f98875301f3c-516031336")

        preference_data = {
                "items": [
                {
                    "title": "FICHAS",
                    "quantity": 1,
                    "unit_price": int(fichas),
                }
            ],
                "back_urls": {
                    "success": "http://127.0.0.1:5000/listo",
                    "failure": "#",
                    "pending": "#",
            },
                "default_payment_method_id": 'debin_transfer',
                "auto_return": "approved",   
        }
        
        preference_response = sdk.preference().create(preference_data)
        preference_id = preference_response["response"]["id"]
        
    return render_template('result.html', jugador=jugador, pref=preference_id)

@app.route('/listo', methods=['POST', 'GET'])
def listo():
    return render_template('listo.html')

@app.route('/otro', methods=['POST', 'GET'])
def otro():
    
    ruta_archivo_excel = 'libro1.xlsx'
    data_frame = pd.read_excel(ruta_archivo_excel)
    jugador_buscado = jugador
    id = data_frame.loc[data_frame['jugador'] == jugador_buscado, 'id'].iloc[0]
    
    options = webdriver.ChromeOptions()
    chrome_driver = webdriver.Chrome(options=options)

    chrome_driver.get("https://agentes.ganaencasa.co/account/login")
    time.sleep(4)

    element = chrome_driver.find_element("name", "userNameOrEmailAddress")
    element.send_keys("Francoo")

    element = chrome_driver.find_element("name", "password")
    element.send_keys("Gokussj99")

    chrome_driver.find_element('xpath', '//*[@id="kt_login"]/div/div[2]/div[2]/ng-component/div/form/div[3]/button').click()

    time.sleep(2)

    chrome_driver.get("https://agentes.ganaencasa.co/app/admin/usersManage/0")

    time.sleep(3)
    buscador = chrome_driver.find_element('name', 'filterText')
    busqueda = jugador
    time.sleep(1)
    buscador.send_keys(busqueda)

    time.sleep(3)
    chrome_driver.find_element('xpath', '//*[@id="btn_search"]').click()
    
    time.sleep(2)
    dinero_element = chrome_driver.find_element('xpath', f'//*[@id="itemBlc__{jugador}"]/div')
    dinero_text = dinero_element.get_attribute("textContent").replace(",", ".")
    dinero_text = float(dinero_text)
    segundo_decimal = int(dinero_text * 10) % 10
    primer_decimal = int((dinero_text * 10) % 10)
    print(dinero_text)
    
    if primer_decimal == 0:
        dinero_text = int(dinero_text)
        print(dinero_text)
    elif segundo_decimal == 0:
        dinero_text = round(dinero_text, 1)
        print(dinero_text)
    else:
        dinero_text = math.floor(dinero_text * 100) / 100
        print(dinero_text)
    
    dinero_text = str(dinero_text)

    if dinero_text == "0.00" or dinero_text == "0.0":
        dinero_text = int(0)

    time.sleep(2)
    chrome_driver.find_element('xpath', f'//*[@id="item__{jugador}__1__10034057__{dinero_text}__{id}__ARS"]').click()

    time.sleep(3)
    

    element = chrome_driver.find_element("name", "monto")
    element.send_keys(fichas)
    time.sleep(3)
    chrome_driver.find_element('xpath', '/html/body/app-root/ng-component/div/default-layout/div/div[2]/div/div[2]/div[2]/div[1]/app-users-manage/div/deposit-modal/div/div/div/form/div[3]/button[2]').click()
    time.sleep(1)
    chrome_driver.find_element('xpath', '/html/body/div/div/div[3]/button[1]').click()


    time.sleep(2)
    
    chrome_driver.quit()
    
    return render_template('otro.html')

if __name__ == '__main__':
    app.run(debug=True)