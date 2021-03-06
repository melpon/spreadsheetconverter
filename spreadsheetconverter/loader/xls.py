# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import xlrd
from xlrd.xldate import xldate_as_datetime

from .base import BaseLoader, BaseBook, BaseSheet
from .valueconverter.datetime import ValueConverter as BaseDatetimeConverter
from .valueconverter.date import ValueConverter as BaseDateConverter


class XlsDatetimeValueConverter(BaseDatetimeConverter):
    def __init__(self, settings, date_mode):
        super(XlsDatetimeValueConverter, self).__init__(settings)
        self.date_mode = date_mode

    def to_python(self, value):
        if isinstance(value, float):
            return xlrd.xldate.xldate_as_datetime(value, self.date_mode)

        return super(XlsDatetimeValueConverter, self).to_python(value)


class XlsDateValueConverter(BaseDateConverter):
    def __init__(self, settings, date_mode):
        super(XlsDateValueConverter, self).__init__(settings)
        self.date_mode = date_mode

    def to_python(self, value):
        if isinstance(value, float):
            _datetime = xlrd.xldate.xldate_as_datetime(value, self.date_mode)
            return _datetime.date()

        return super(XlsDateValueConverter, self).to_python(value)


class Loader(BaseLoader):
    def __init__(self, params):
        super(Loader, self).__init__(params)
        self._book = Book(self._params.path[1:])
        self._sheet = self._book.get_sheet(self._params.fragment)

    @property
    def sheet(self):
        return self._sheet

    def get_book(self):
        return self._book

    def get_sheet(self, name):
        return self._book.get_sheet(name)

    def get_value_converter(self, setting):
        if setting['type'] == 'datetime':
            return XlsDatetimeValueConverter(setting, self._book.datemode)
        if setting['type'] == 'date':
            return XlsDateValueConverter(setting, self._book.datemode)

        return super(Loader, self).get_value_converter(setting)


class Book(BaseBook):
    def __init__(self, file_path):
        super(Book, self).__init__()
        self._file_path = file_path
        self._workbook = xlrd.open_workbook(self._file_path)

    @property
    def datemode(self):
        return self._workbook.datemode

    @property
    def sheets(self):
        for sheet in self._workbook.sheets():
            yield Sheet(sheet)

    def get_sheet(self, name):
        wb = xlrd.open_workbook(self._file_path)
        for sheet in wb.sheets():
            if sheet.name == name:
                return Sheet(sheet)

        raise Exception()


class Sheet(BaseSheet):
    def __init__(self, sheet):
        super(Sheet, self).__init__()
        self.sheet = sheet

    @property
    def rows(self):
        for row in range(self.sheet.nrows):
            yield [self.sheet.cell(row, col).value
                   for col in range(self.sheet.ncols)]
