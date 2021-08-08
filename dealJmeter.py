#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari

import os
import time
import xml.dom.minidom
from config import getJMeter


class JMeter:
    def __init__(self, current_test_case):
        path = getJMeter('path')
        self.raw_name = os.path.join(path, getJMeter('rawName'))
        self.output_name = os.path.join(path, getJMeter('outputName'))

        self.jtl_path = os.path.join(path, getJMeter('jtlPath'))
        self.html_path = os.path.join(path, getJMeter('htmlPath'))

        self.current_test_case = current_test_case

    def dealJMeter(self):
        dom_tree = xml.dom.minidom.parse(self.raw_name)
        root_node = dom_tree.documentElement

        all_test_cases = root_node.getElementsByTagName('TransactionController')

        for test_case in all_test_cases:
            test_name = test_case.getAttribute('testname')
            if test_name == self.current_test_case:
                test_case.setAttribute('enabled', 'false')
                bool_props = test_case.getElementsByTagName('boolProp')
                for bool_prop in bool_props:
                    if bool_prop.getAttribute('name') == 'TransactionController.parent':
                        bool_prop.childNodes[0].data = 'false'

            else:
                test_case.setAttribute('enabled', 'false')
                bool_props = test_case.getElementsByTagName('boolProp')
                for bool_prop in bool_props:
                    if bool_prop.getAttribute('name') == 'TransactionController.parent':
                        bool_prop.childNodes[0].data = 'false'

            with open(self.output_name, 'w', encoding='utf-8') as f:
                root_node.writexml(f)

    def runJMeter(self):
        current_time = str(int(time.time()))
        jtl_name = os.path.join(self.jtl_path, current_time + '.jtl')
        html_path = os.path.join(self.html_path, current_time)

        if not os.path.exists(html_path):
            os.mkdir(html_path)

        _  = os.popen('nohup jmeter ')

        return html_path

    def deal_html(self, html_path):
        pass