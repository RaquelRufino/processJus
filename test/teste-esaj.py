# -*- coding: utf-8 -*-

import unittest
import json
from selenium import webdriver
import sys
sys.path.append("..")
from crawlers.esaj import search_process

class SearchText(unittest.TestCase):

    def test_search_process01(self):
        """
        Test at the Court of Justice of São Paulo where you have a lawsuit in 1st and 2nd degree
        """
        response = {
        "number": "1002298-86.2015.8.26.0271",
        "state" : "sp"}
        self.assertEqual(3, len(search_process(json.dumps(response))))

    def test_search_process02(self):
        """
        Test in the Court of Justice of Mato Grosso do Sul where there is only one process
        """
        response = {
        "number": "0821901-51.2018.8.12.0001",
        "state" : "ms"}
        self.assertEqual(1, len(search_process(json.dumps(response))))

    def test_search_process03(self):
        """
        Test in the Court of Justice of São Paulo in which the process is in secrecy of justice
        """
        response = {
        "number": "0000000-00.0000.8.26.0000",
        "state" : "sp"}
        self.assertEqual("Caso Privado", search_process(json.dumps(response)))

    def test_search_process04(self):
        """
        Test in the Court of Justice of São Paulo in which the process is in secrecy of justice
        """
        response = {
        "number": "0015338-39.2012.8.26.0278",
        "state" : "sp"}
        self.assertEqual("Caso Privado", search_process(json.dumps(response)))

    def test_search_process05(self):
        """
        Test in the Court of Justice of São Paulo where there is only one process
        """
        response = {
        "number": "0010599-28.2019.8.26.0100",
        "state" : "sp"}
        self.assertEqual(1, len(search_process(json.dumps(response))))

    def test_search_process06(self):
        """
        Test in the Court of Justice of São Paulo where there is only one process
        """
        response = {
        "number": "0024825-72.2018.8.26.0100",
        "state" : "sp"}
        self.assertEqual(1, len(search_process(json.dumps(response))))

    def test_search_process07(self):
        """
        Test in the Court of Justice of São Paulo where there is only one process
        """
        response = {
        "number": "0010599-28.2019.8.26.0100",
        "state" : "sp"}
        self.assertEqual(1, len(search_process(json.dumps(response))))

    def test_search_process08(self):
        """
        Test in the Court of Justice of Mato Grosso do Sul 
        """
        response = {
        "number": "0000083-75.2011.8.12.0016",
        "state" : "ms"}
        self.assertEqual(2, len(search_process(json.dumps(response))))

    def test_search_process09(self):
        """
        Test in the Court of Justice of Mato Grosso do Sul
        """
        response = {
        "number": "0001092-83.2009.8.12.0035",
        "state" : "ms"}
        self.assertEqual(2, len(search_process(json.dumps(response))))

    def test_search_process10(self):
        """
        Test in the Court of Justice of Mato Grosso do Sul
        """
        response = {
        "number": "0001092-83.2009.8.12.0035",
        "state" : "ms"}
        self.assertEqual(2, len(search_process(json.dumps(response)))) 

    def test_search_process11(self):
        """
        Test in the Court of Justice of São Paulo that the process does not exist
        """
        response: {    
                "number": "1000000-00.0000.8.26.0000",
                "state" : "sp"}
        self.assertEqual("Nao foi possivel executar essa operacao.", search_process(json.dumps(response)))

if __name__ == '__main__':
    unittest.main()
