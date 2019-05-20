# -*- coding: utf-8 -*-
"""Trace a lawsuit"""

import scrapy
import json
from selenium import webdriver
from processJus.items import ProcessjusItem
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from xml.etree import ElementTree
class ProcessSpider(scrapy.Spider):
    """Crawler of Process"""

    name = 'process'
    allowed_domains = []
    #allowed_domains = ['']
    start_urls = []
    def __init__(self, *a, **kw):
        super(ProcessSpider, self).__init__(*a, **kw)
        with open('seeds/tj.json') as json_file:
                data = json.load(json_file)
        self.allowed_domains = list(data.values())
        self.start_urls = ['https://esaj.tjsp.jus.br/cpopg/open.do']

    # def start_requests(self):
    #     url = 'localhost:8082'
    #     headers = {'Content-type': 'application/json'}
    #     params = {
    #     'number': 'value1',
    #     }
    #     response = webdriver.request('POST', url, paramss)
    #     yield scrapy.Request('localhost:8082',
    #                         method="POST",
    #                         body=request_body,
    #                         headers={'Content-Type': 'application/json; charset=UTF-8'}, )

    def parse(self, response):

        response = {
            "number": "1002298-86.2015.8.26.0271",
            "state" : "sp"}
        state = response["state"]
        with open('seeds/tj.json') as json_file:
            data = json.load(json_file)
        data = list(data[state])

        for url in data:
            print url
            #return self.search_information(str(url), response)

        #time.sleep(30)
        return self.search_process(str(data[0]), response)

    def search_process(self, url, response):
        #self.start_urls = url
        number_process = response["number"]
        chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        driver = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=chrome_options)
        
        driver.get(url)

        driver.find_element_by_id('numeroDigitoAnoUnificado').send_keys(number_process[:15])
        driver.find_element_by_id('foroNumeroUnificado').send_keys(number_process[21:])
        if url[25:30] == "cposg":
            submit_button = driver.find_element_by_id('botaoPesquisar')
        else:
            submit_button = driver.find_element_by_id('pbEnviar')
        submit_button.click()
        if self.__isNumberProcess(driver):

            if not(self.__isCaseSecrect(driver)):

                if self.__isPrivateRight(driver):
                    pass
                
                else:
                    pass


        return self.__get_process_data(driver)

    def __isPrivateRight(self, driver):
        """ Check if is Private Right """
        try:
            driver.find_element_by_xpath("//div[contains(text(),'Direito Privado')]")
            
            return True
        except:
            
            return False

    def __isNumberProcess(self, driver):
        """ Check if is Number Process """
        try:
            driver.find_element_by_xpath('//*[@id="mensagemRetorno"]/li')
            return False
        except NoSuchElementException:
            return True

    def __isCaseSecrect(self, driver):
        """ 
        Checks if it is a secret process of justice
        """
        try:
            driver.find_element_by_xpath('//*[@id="popupSenha"]/table/tbody/tr[5]/td[1]/b')
            return True
        except NoSuchElementException:
            return False

    def __get_process_data(self, driver):
        """
            Gets process's data.
        """

        elem = ProcessjusItem()
        phantom = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
        #url = driver.Url
        phantom.get('https://esaj.tjsp.jus.br/cposg/show.do?processo.codigo=RI0034YMS0000&conversationId=&paginaConsulta=1&localPesquisa.cdLocal=-1&cbPesquisa=NUMPROC&tipoNuProcesso=UNIFICADO&numeroDigitoAnoUnificado=1002298-86.2015&foroNumeroUnificado=0271&dePesquisaNuUnificado=1002298-86.2015.8.26.0271&dePesquisa=&uuidCaptcha=')
        elem['classe'] = self.get_process_class(driver)
        elem['area'] = self.get_process_area(driver)
        elem['subject'] = self.get_process_subject(driver)
        elem['distribuition_date'] = self.get_process_distribuition_date(driver)
        elem['judge'] = self.get_process_judge(driver)
        elem['share_value'] = self.get_process_share_value(driver)
        elem['parts'] = self.get_process_parts(driver)
        elem['drives'] = self.get_process_drives(driver)

        
        return elem


    @staticmethod
    def get_process_class(phantom):
        """
        Gets process's class.
        """
        return phantom.execute_script("return $('.labelClass:contains(\"Classe\")').closest('tr').find('span').eq(0).text()").replace('\n', '').replace('\t', '').replace(" ", "")


    @staticmethod
    def get_process_area(phantom):
        """
        Gets process's area.
        """
        return phantom.execute_script("return $('.labelClass:contains(\"Área\")').closest('td').text()").strip()[len('Área: '):]

    @staticmethod
    def get_process_subject(phantom):
        """
        Gets process's subject.
        """
        return phantom.execute_script("return $('.labelClass:contains(\"Assunto\")').closest('tr').find('span').text()")

    @staticmethod
    def get_process_distribuition_date(driver):
        """
        Gets process's distribuition date.
        """
        return driver.find_elements_by_xpath(
            '/html/body/div/table[4]/tbody/tr/td/div[1]/table[2]/tbody/tr[6]/td[2]/span')

    @staticmethod
    def get_process_judge(phantom):
        """
        Gets process's judge.
        """
        judge = phantom.execute_script("return $('.labelClass:contains(\"Juiz\")').closest('tr').find('span').text()")
        judge = (judge, None)[judge == '']
        return judge

    @staticmethod
    def get_process_share_value(phantom):
        """
        Gets process's share value.
        """
        share_value = phantom.execute_script("return $('.labelClass:contains(\"Valor da ação\")').closest('tr').find('span').text()").replace(" ", "")
        share_value = (share_value, None)[share_value == '']
        return share_value

    @staticmethod
    def get_process_parts(phantom):
        """
        Gets process's parts.
        """
        process_parts = []
        table_principais = phantom.find_element_by_id('tablePartesPrincipais')
        if len(phantom.find_elements_by_id('tableTodasPartes')) == 1:
            table_todos = phantom.find_element_by_id('tableTodasPartes')
        else:
            table_todos = None

        if table_todos is not None:
            principais_name = [i.text.split('\n')[0] for i in table_principais.find_elements_by_css_selector('[align="left"]')]
            phantom.find_element_by_id('linkpartes').click()

            for i in table_todos.find_elements_by_class_name('fundoClaro'):
                parte_type = i.find_element_by_css_selector('[align="right"]').text[:-2]

                left_text = i.find_element_by_css_selector('[align="left"]').text
                parte_name = left_text.split('\n')[0]
                left_text = left_text.split('\n')[1:]

                # todo: lidar com abreviações em parte_type tais como
                #   "Ministério Púb" -> "Mininsério Público"
                part = [(0, 1)[parte_name in principais_name], parte_type, parte_name.title()]
                sub_part = []
                for i in left_text:
                    justiciario_type, justiciario_name = i.split(': ')
                    # todo: unificar gêneros em justiciario_type, tais como
                    #   "advogada" -> "advogado"
                    #   "Devedora" -> "Devedor"
                    # também há sites que ficam com inicial maiúscula enquanto outros não
                    # e abreviações, tais como
                    #   "Ministério Púb" -> "Mininsério Público"
                    #   "Defensor P" -> Defensor Público
                    sub_part = [justiciario_type, justiciario_name.strip().title()]
                    part.extend(sub_part)
                process_parts.extend(part)
        else:
            for i in table_principais.find_elements_by_class_name('fundoClaro'):
                parte_type = i.find_element_by_css_selector('[align="right"]').text[:-2]

                left_text = i.find_element_by_css_selector('[align="left"]').text
                parte_name = left_text.split('\n')[0]
                left_text = left_text.split('\n')[1:]

                reu_preso = 0
                if parte_name[-1 * len(' Réu Preso'):] == ' Réu Preso':
                    parte_name = parte_name[:len(parte_name) - len(' Réu Preso')]
                    reu_preso = 1
                part = [1, parte_type, parte_name.title(), reu_preso]
                sub_part = []
                
                for i in left_text:
                    justiciario_type, justiciario_name = i.split(': ')
                    sub_part = [justiciario_type, justiciario_name.strip().title()]
                    part.extend(sub_part)
                process_parts.extend(part)
        return process_parts

    @staticmethod
    def get_process_drives(phantom):
        """
        Gets process's drives.
        """
        phantom.find_element_by_id('linkmovimentacoes').click()
        movs = []
        drives = phantom.find_element_by_id('tabelaTodasMovimentacoes').find_elements_by_tag_name('tr')
        for i in drives:
            data, description = [i.find_elements_by_tag_name('td')[0].text, i.find_elements_by_tag_name('td')[2].text]
            movs.extend([data,description])
            # todo: documento_url = ... pegar o texto do documento, se disponível 
        return movs

    # def parse_error(self, failure):
    #     """
    #     Error message.
    #     """
    #     logging.error('It was not possible: {}'.format(failure.url))
 