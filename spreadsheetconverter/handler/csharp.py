# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import json
from .base import BaseHandler
from .valueformatter.string import ValueFormatter as StringValueFormatter


class Handler(BaseHandler):

    def _make_csharp(self):
        members = []
        inits = []
        properties = []

        for i, field in enumerate(self._config['fields']):
            name = field['column']
            type_ = field['type']
            if type_ != 'foreignkey':
                member_name = name

                csharp_type = {
                    'int': 'int',
                    'char': 'string',
                    'string': 'string',
                    'float': 'float',
                    'datetime': 'DateTime',
                }[type_]
                member = 'public {0} {1};'.format(csharp_type, member_name)
                members.append(member)
            else:
                member_name = '_' + name
                property_name = name
                new_type = field['relation']['from'].rules['handler']['name']

                member = 'public {0} {1};'.format('int', member_name)
                members.append(member)

                prop = "public {new_type} {property_name} {{ get {{ return MasterData.{new_type}[this.{member_name}]; }} }}".format(
                    property_name=property_name,
                    new_type=new_type,
                    member_name=member_name)
                properties.append(prop)

            cast = {
                'int': '(int)(long){0}',
                'char': '(string){0}',
                'string': '(string){0}',
                'float': '(float)(double){0}',
                'datetime': 'DateTime.Parse((string){0})',
                'foreignkey': '(int)(long){0}',
            }[type_]
            init = """obj.{0} = {1};""".format(member_name, cast.format("row[{0}]".format(i)))
            inits.append(init)

        return """/*
 * このコードは自動生成です。
 * 手動で編集せず、別ファイルにpartial classを定義して拡張してください。
 */
using System;
using System.Collections.Generic;

namespace MasterDataTable
{{
    public partial class {0}
    {{
        {1}

        public static {0} ParseList(List<object> row)
        {{
            var obj = new {0}();
            {2}
            return obj;
        }}

        {3}
    }}
}}
""".format(
            self._config['name'],
            ("\n" + " " * 8).join(members),
            ("\n" + " " * 12).join(inits),
            ("\n" + " " * 8).join(properties))

    def save(self, data):
        with open(self._config['csharp'], 'w') as f:
            f.write(self._make_csharp())

        with open(self._config['json'], 'w') as f:
            keys = [field['column'] for field in self._config['fields']]
            converted_data = [[entity[key] for key in keys] for entity in data]
            indent = self._config.get('indent')
            sort_keys = self._config.get('sort_keys', False)
            f.write(json.dumps(converted_data, indent=indent, sort_keys=sort_keys))

    def get_value_formatter(self, setting):
        if setting['type'] == 'datetime':
            return StringValueFormatter(setting)

        return super(Handler, self).get_value_formatter(setting)
