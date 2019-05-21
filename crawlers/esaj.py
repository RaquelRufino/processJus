# -*- coding: utf-8 -*-
"""Crawler at Court of Justice"""

import json
import sys
import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#sys.path.append("..")
from crawlers.process import Process


def search_process(response):
    """
    Search Process
    """
    all_process = []
    # response = {
    #     "number": "0001092-83.2009.8.12.0035",
    #     "state" : "ms"}
    response = json.loads(response)
    state = response["state"]

    with open('../seeds/tj.json') as json_file:
        data = json.load(json_file)

    urls = data[state]

    number_process = response["number"]
    process = Process()
    driver = __get_driver()
    for url in urls:
        driver.get(url)
        driver.find_element_by_id('numeroDigitoAnoUnificado').send_keys(number_process[:15])
        driver.find_element_by_id('foroNumeroUnificado').send_keys(number_process[21:])
        if url[25:30] == "cposg":
            submit_button = driver.find_element_by_id('botaoPesquisar')
        else:
            submit_button = driver.find_element_by_id('pbEnviar')
        submit_button.click()
        if __is_number_process(driver):
            if not(__is_case_secret(driver)):
                if not(__is_private_right(driver)):
                    href_list = []
                    while True:
                        href_list.extend(
                            [i.find_element_by_tag_name('a').get_attribute(
                                'href') for i in driver.find_elements_by_class_name(
                                    'nuProcesso')])
                        next_page = __get_element_next_page(driver)
                        if next_page is not None:
                            next_page.click()
                        else: break
                    for url in href_list:
                        driver.get('about:blank')
                        while driver.current_url == 'about:blank':
                            driver.get(url)
                            all_process.append(
                                {"Processo": Process.get_process_json(process, driver)})

                else:
                    all_process.append({"Processo": Process.get_process_json(process, driver)})
            else:
                driver.close()
                return "Caso Privado"
        else:
            if len(all_process):
                break
            else:
                driver.close()
                return "Nao foi possivel executar essa operacao."
    driver.close()
    return all_process

def __is_private_right(driver):
    """ Check if is Private Right """
    return driver.find_elements_by_class_name('nuProcesso') == []

def __is_number_process(driver):
    """ Check if is Number Process """
    return driver.find_elements_by_class_name('tabelaMensagem') == []

def __is_case_secret(driver):
    """
    Checks if it is a secret process of justice
    """
    return driver.find_elements_by_class_name('modalTitulo') != []

def __get_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    if platform.system() == 'Linux':
        chrome_driver_binary = "/usr/bin/chromedriver"
    else:
        chrome_driver_binary = "/usr/local/bin/chromedriver"
    driver = webdriver.Chrome(chrome_driver_binary, options=chrome_options)
    return driver

def __get_element_next_page(driver):
    element_next_page = driver.execute_script("return $('a:contains(\">\")').eq(0)")
    if len(element_next_page) > 0:
        return element_next_page[0]

    return None

if __name__ == "__main__":
    search_process(None)
