# -*- coding: utf-8 -*-
"""Process Data"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from unidecode import unidecode

class Process():
    """
    Process Data
    """

    def __init__(self):

        self.process = []


    def get_process_json(self, driver):
        """
        Gets process json.
        """
        self.process.append(self.__get_process_class(driver))
        self.process.append(self.__get_process_area(driver))
        self.process.append(self.__get_process_subject(driver))
        self.process.append(self.__get_process_distribuition_date(driver))
        self.process.append(self.__get_process_judge(driver))
        self.process.append(self.__get_process_share_value(driver))
        self.process.append(self.__get_process_parts(driver))
        self.process.append(self.__get_process_drives(driver))

        return self.process

    def __get_process_class(self, driver):
        """
        Gets process's class.
        """
        return {'Classe': unidecode(driver.execute_script("return $('.labelClass:contains(\"Classe\")').closest('tr').find('span').eq(0).text()").replace('\n', '').replace('\t', '').strip())}

    def __get_process_area(self, driver):
        """
        Gets process's area.
        """
        return {'Area': unidecode(driver.execute_script("return $('.labelClass:contains(\"Área\")').closest('td').text()").strip()[len('Área:'):])}

    def __get_process_subject(self, driver):
        """
        Gets process's subject.
        """
        return {'Assunto': unidecode(driver.execute_script("return $('.labelClass:contains(\"Assunto\")').closest('tr').find('span').text()"))}

    def __get_process_distribuition_date(self, driver):
        """
        Gets process's distribuition date.
        """
        date = driver.execute_script("return $('.labelClass:contains(\"Distribuição\")').closest('tr').find('span').text()")
        date = (date, None)[date == '']
        if date is None: return {'Data de distribuicao': ""}
        return {'Data de distribuicao': unidecode(date)}

    def __get_process_judge(self, driver):
        """
        Gets process's judge.
        """
        judge = driver.execute_script("return $('.labelClass:contains(\"Juiz\")').closest('tr').find('span').text()")
        judge = (judge, None)[judge == '']
        if judge is None: return {'Juiz': ""}
        return {'Juiz': unidecode(judge)}

    def __get_process_share_value(self, driver):
        """
        Gets process's share value.
        """
        share_value = driver.execute_script("return $('.labelClass:contains(\"Valor da ação\")').closest('tr').find('span').text()").replace(" ", "")
        share_value = (share_value, None)[share_value == '']
        if share_value is None: return {"Valor da acao" : ""}
        return {"Valor da acao" : unidecode(share_value)}

    def __get_process_parts(self, driver):
        """
        Gets process's parts.
        """
        process_parts = []
        table_principais = driver.find_element_by_id('tablePartesPrincipais')
        if len(driver.find_elements_by_id('tableTodasPartes')) == 1:
            table_todos = driver.find_element_by_id('tableTodasPartes')
        else:
            table_todos = None

        if table_todos is not None:
            principais_name = [i.text.split('\n')[0] for i in table_principais.find_elements_by_css_selector('[align="left"]')]
            driver.find_element_by_id('linkpartes').click()

            for i in table_todos.find_elements_by_class_name('fundoClaro'):
                parte_type = i.find_element_by_css_selector('[align="right"]').text[:-2]

                left_text = i.find_element_by_css_selector('[align="left"]').text
                parte_name = left_text.split('\n')[0]
                left_text = left_text.split('\n')[1:]

                part = [(0, 1)[parte_name in principais_name], parte_type, parte_name.title()]
                part = unidecode(part[1]) + " : " + unidecode(part[2])
                sub_part = []
                for i in left_text:
                    justiciario_type, justiciario_name = i.split(': ')
                    sub_part.append({unidecode(justiciario_type): unidecode(justiciario_name.strip().title())})
                process_parts.append({part:sub_part})
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
        return {'Partes do processo' : process_parts}

    def __get_process_drives(self, driver):
        """
        Gets process's drives.
        """
        driver.find_element_by_id('linkmovimentacoes').click()
        movs = []
        drives = driver.find_element_by_id('tabelaTodasMovimentacoes').find_elements_by_tag_name('tr')
        for i in drives:
            data, description = [i.find_elements_by_tag_name('td')[0].text, i.find_elements_by_tag_name('td')[2].text]
            data = unidecode(data)
            description = unidecode(description)
            movs.append({data: description})
        return {"Lista das movimentações" :movs}
