# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import sys
import os


sys.path.append(os.path.abspath('..'))
from spreadsheetconverter import Converter, YamlConfig


if __name__ == '__main__':
    converter = Converter(YamlConfig('cs_user.yaml'))
    converter.run()
