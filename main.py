from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Abre o Chrome WebDriver
driver = webdriver.Chrome()
driver.maximize_window()

# Abre o WhatsApp Web
driver.get("https://web.whatsapp.com/")
input("Escaneie o código QR do WhatsApp e pressione Enter")

# Carregua os contatos e mensagens a partir da planilha do Excel
planilha = pd.read_excel('data\contatos.xlsx')

# Loop através dos contatos e mensagens
for index, row in planilha.iterrows():
    contato = row['Contato']
    imagem = row['Imagem']

    # Aguarde até que o campo de pesquisa seja visível
    search_box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
    )
    search_box.clear()
    search_box.send_keys(contato)
    time.sleep(2)

    # Selecione o contato
    contato_element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, f'//span[@title="{contato}"]'))
    )
    contato_element.click()
    time.sleep(2)

    # Envie a imagem
    attachment_icon = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@title="Anexar"]'))
    )
    attachment_icon.click()
    image_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]'))
    )
    image_input.send_keys(imagem)
    time.sleep(2)
    send_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//span[@data-icon="send"]'))
    )
    send_button.click()
    time.sleep(2)

# Feche o navegador
driver.quit()