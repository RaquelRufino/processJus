# -*- coding: utf-8 -*-
"""Trace a lawsuit"""
import sys
sys.path.append("..")
import json
from selenium import webdriver
from crawlers.process import Process
from unidecode import unidecode
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time

def search_process(response):
    all_process = []
    response = {
        "number": "0001092-83.2009.8.12.0035",
        "state" : "ms"}
    state = response["state"]

    with open('../seeds/tj.json') as json_file:
        data = json.load(json_file)

    urls = data[state]

    number_process = response["number"]
    process = Process()
    driver = __getDriver()
    for url in urls:

        driver.get(url)
        driver.find_element_by_id('numeroDigitoAnoUnificado').send_keys(number_process[:15])
        driver.find_element_by_id('foroNumeroUnificado').send_keys(number_process[21:])
       
        if url[25:30] == "cposg":
            submit_button = driver.find_element_by_id('botaoPesquisar')
        else:
            submit_button = driver.find_element_by_id('pbEnviar')
        submit_button.click()
        if __isNumberProcess(driver):
            if not(__isCaseSecrect(driver)):          
                if not(__isPrivateRight(driver)):
                    href_list = []
                    while True:
                        href_list.extend([i.find_element_by_tag_name('a').get_attribute('href') for i in driver.find_elements_by_class_name('nuProcesso')])
                        next_page = __get_element_next_page(driver)
                        if next_page is not None:
                            next_page.click()
                        else: break
                    # if len(href_list) == 0:
                    #     print ("Nao tem processo")
                    for url in href_list:
                        driver.get('about:blank')
                        while driver.current_url == 'about:blank':
                            driver.get(url)
                            all_process.append({"Processo": Process.get_process_json(process, driver)})

     
                else:
                    all_process.append({"Processo": Process.get_process_json(process, driver)})
            else:
                return all_process

        # else:
        #     print ("Não foi possível executar esta operação.")
    driver.quit()
    return all_process

def __isPrivateRight(driver):
    """ Check if is Private Right """
    return driver.find_elements_by_class_name('nuProcesso') == []

def __isNumberProcess(driver):
    """ Check if is Number Process """
    return driver.find_elements_by_class_name('tabelaMensagem') == []

def __isCaseSecrect(driver):
    """ 
    Checks if it is a secret process of justice
    """
    return driver.find_elements_by_class_name('modalTitulo') != []

def __getDriver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    return webdriver.Chrome('/usr/bin/chromedriver', chrome_options=chrome_options)

def __get_element_next_page(driver):
    element_next_page = driver.execute_script("return $('a:contains(\">\")').eq(0)")
    if len(element_next_page) > 0:
        return element_next_page[0]
    else:
        return None

if __name__ == "__main__" :

    search_process(None)

