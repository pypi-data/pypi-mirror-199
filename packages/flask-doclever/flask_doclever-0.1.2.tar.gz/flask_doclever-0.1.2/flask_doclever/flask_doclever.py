# -*- coding: utf-8 -*-

__author__ = 'liuxu'

import time
import functools
import inspect
import re
from flask_restful import fields, Resource
from flask import request
import uuid
import requests
import json


DOCTYPE_STR = 0
DOCTYPE_NUM = 1
DOCTYPE_BOOL = 2
DOCTYPE_LIST = 3
DOCTYPE_DICT = 4

'''
    1. Doclever新建项目，在项目下建default分组
'''

SOURCE = None
DOCLEVER = None


class Interfaces(Resource):
    def __init__(self):
        super(Interfaces, self).__init__()

    # 新增接口
    def post(self, **kwargs):
        info = []
        interfaces = DOCLEVER.get_interfaces()

        for url, route in SOURCE.route.items():
            methods = set()
            if hasattr(route['resource'], 'get'):
                methods.add('GET')
            if hasattr(route['resource'], 'post'):
                methods.add('POST')
            if hasattr(route['resource'], 'put'):
                methods.add('PUT')
            if hasattr(route['resource'], 'delete'):
                methods.add('DELETE')

            # 排除文档中是否已存接口
            exist_methods = {
                interface['interface_method']
                for interface in interfaces.values()
                if interface['interface_url'] == url}
            methods = methods - exist_methods
            if methods:
                src_interfaces = SOURCE.parse_resource(
                    resource=route['resource'],
                    url=route['url'])

                for src_interface in src_interfaces:
                    if src_interface['method'] in methods:
                        # 生成doclever文档
                        doc_interface = DOCLEVER.create_interface(data=src_interface)
                        info.append({
                            'method': doc_interface['data']['method'],
                            'url': doc_interface['data']['url']})

        return {'code': 'OK', 'msg': '正确', 'count': len(info), 'info': info}


class Interface(Resource):
    def __init__(self):
        super(Interface, self).__init__()

    # 更新指定接口
    def get(self, id, **kwargs):
        interfaces = DOCLEVER.get_interfaces()

        for interface in interfaces.values():
            if interface['interface_id'] == id:
                old_interface = DOCLEVER.get_interface(
                    interface_id=interface['interface_id'],
                    group_id=interface['group_id'])
                break
        else:
            return {'code': 'ERROR', 'msg': '错误的ID值'}

        route = SOURCE.route.get(old_interface['url'])
        if not route:
            return {'code': 'ERROR', 'msg': '该接口在代码中不存在'}

        # 解析代码
        src_interfaces = SOURCE.parse_resource(
            resource=route['resource'],
            url=route['url'])

        for src_interface in src_interfaces:
            if src_interface['method'] == interface['interface_method']:
                # 合并新旧接口
                doc_interface = SOURCE.merge_interface(
                    new_interface=src_interface,
                    old_interface=old_interface)

                # 保存接口
                DOCLEVER.create_interface(
                    data=doc_interface,
                    group_id=old_interface['group'],
                    id=old_interface['_id'])

        return {'code': 'OK', 'msg': '正确'}


class CodeGenerate(Resource):
    def __init__(self):
        super(CodeGenerate, self).__init__()

    # 代码生成
    def post(self, **kwargs):
        lines = request.data.decode().splitlines()
        field_list = []
        name = None
        for line in lines:
            if not name:
                name = re.search(r'# (.*)', line).group(1)
                continue

            if 'class' in line:
                table_name = re.search(r'class\s+(\w+)', line).group(1)
                base_name = re.search(r'class Tbl(\w+)', line).group(1)
            if '#' in line:
                field = {'comment': re.search(r'# (.*)', line).group(1), 'type': None}
                field_list.append(field)
            if 'DB.Column' in line:
                field['var_name'] = re.search(r'(\w+)\s*=', line).group(1)
                if 'DB.String' in line:
                    field['type'] = 'string'
                elif 'DB.Integer' in line:
                    field['type'] = 'integer'
                elif 'DB.JSON' in line:
                    field['type'] = 'json'
                elif 'DB.Numeric' in line:
                    field['type'] = 'numeric'
                elif 'DB.DateTime' in line:
                    field['type'] = 'datetime'
                elif 'DB.Date' in line:
                    field['type'] = 'date'
                elif 'DB.Float' in line:
                    field['type'] = 'float'
                elif 'DB.BigInteger' in line:
                    field['type'] = 'integer'
                elif 'DB.SmallInteger' in line:
                    field['type'] = 'integer'
                elif 'DB.Text' in line:
                    field['type'] = 'string'
                elif 'DB.Boolean' in line:
                    field['type'] = 'bool'
                elif 'DB.Text' in line:
                    field['type'] = 'string'
            if 'descriptor.DataDictionary' in line:
                field['var_name'] = re.search(r'(\w+)\s*=', line).group(1)
                field['type'] = 'datadictionary'
            if 'ReferenceColumn' in line:
                field['var_name'] = re.search(r'(\w+)\s*=', line).group(1)
                field['type'] = 'referencecolumn'
            if 'DB.relationship' in line:
                field['var_name'] = re.search(r'(\w+)\s*=', line).group(1)
                field['type'] = 'relationship'

        request_parse = ''
        for field in field_list:
            attach = ""
            if field['type'] == 'string':
                pass
            elif field['type'] == 'integer':
                attach = ", type=request.Type.positive"
            elif field['type'] == 'json':
                attach = ", action='append', type=request.Type.json(schema.Json.SEQ)"
            elif field['type'] == 'numeric':
                attach = ", type=request.Type.money"
            elif field['type'] == 'datetime':
                attach = ", type=request.Type.datetime"
            elif field['type'] == 'date':
                attach = ", type=request.Type.date"
            elif field['type'] == 'float':
                attach = ", type=float"
            elif field['type'] == 'datadictionary':
                continue
            elif field['type'] == 'referencecolumn':
                attach = ", type=request.Type.positive"
            elif field['type'] == 'relationship':
                continue

            request_parse += """
    # {}
    req.add_body('{}'{})""".format(field['comment'], field['var_name'], attach)

        response_parse = '    '+base_name.upper()+' = {'
        for field in field_list:
            attach = ""
            if field['type'] == 'string':
                attach = "fields.String"
            elif field['type'] == 'integer':
                attach = "fields.Integer"
            elif field['type'] == 'json':
                attach = "fields.List(fields.String)"
            elif field['type'] == 'numeric':
                attach = "fields.Price(decimals=2)"
            elif field['type'] == 'datadictionary':
                attach = "fields.String"
            elif field['type'] == 'referencecolumn':
                attach = "fields.Integer"
            elif field['type'] == 'relationship':
                attach = r"fields.List(fields.Nested({}))"
            elif field['type'] == 'datetime':
                attach = "DateTime"
            elif field['type'] == 'date':
                attach = "Date"
            elif field['type'] == 'float':
                attach = "fields.Float"

            response_parse += """
        # {}
        '{}': {},""".format(field['comment'], field['var_name'], attach)

        response_parse += '\n    }'

        ret = (
"""
# -*- coding: utf-8 -*-

from project import APP
from project.common import resource
from project.common import request
from project.common import response
from project.common import decorator
from project.common import datadictionary as dd
from project.database.models import {table_name}


__author__ = "liuxu"
# {name}管理


@APP.api.resource('/{base_name_low}s')
class {base_name}s(resource.Resource):
    req = request.RequestParser()
{request_parse}

    def __init__(self):
        super({base_name}s, self).__init__()

    # 增加{name}信息
    def post(self, **kwargs):
        req_args = self.req.parse_args()

        {base_name_low} = {table_name}.create(**req_args)

        return response.get_value({base_name_low}, response.Fields.{base_name_up})

    # 取得{name}列表
    @decorator.get_page
    def get(self, **kwargs):
        query = {table_name}.query

        {base_name_low}s = (
            query
            .paginate(**kwargs['page']))

        return response.get_value({base_name_low}s, response.Fields.{base_name_up})


@APP.api.resource('/{base_name_low}s/< int:id>')
class {base_name}(resource.Resource):
    req = request.RequestParser()
{request_parse}

    def __init__(self):
        super({base_name}, self).__init__()

    # 修改{name}信息
    def put(self, id, **kwargs):
        req_args = self.req.parse_args()

        {base_name_low} = {table_name}.get(id)
        {base_name_low}.update(**req_args)

        return response.get_value({base_name_low}, response.Fields.{base_name_up})

    # 取得{name}信息
    def get(self, id, **kwargs):
        banner = {table_name}.get(id)

        return response.get_value({base_name_low}, response.Fields.{base_name_up})

\n""".format(name=name,
             table_name=table_name,
             base_name=base_name,
             base_name_low=base_name.lower(),
             base_name_up=base_name.upper(),
             request_parse=request_parse))

        return ret + response_parse


def init(app, fields):
    try:
        global SOURCE
        global DOCLEVER

        SOURCE = Source(app=app, fields=fields)
        DOCLEVER = DOClever(app=app)

        doc = DOClever(app=app)
        app.api.add_resource = Source.collect_route(app.api.add_resource)
        app.api.add_resource(Interfaces, '/v1/interfaces')
        app.api.add_resource(Interface, '/v1/interfaces/<string:id>')
        app.api.add_resource(CodeGenerate, '/v1/code/generate')

        # 创建interface的接口文档
        group = doc.create_group('#文档接口')

        # 新增接口
        data = {
            'name': '新增接口',
            'url': '/v1/interfaces',
            'method': 'POST',
            'remark': '新增在doclever中不存在的接口',
            'finish': '0',
            'param': [{
                'before': {
                    'mode': 0,
                    'code': ''
                },
                'after': {
                    'mode': 0,
                    'code': ''
                },
                'name': 'default',
                'id': str(uuid.uuid1()),
                'remark': '',
                'header': [{
                    'name': 'Content-Type',
                    'value': 'application/json',
                    'remark': ''
                }],
                'queryParam': [],
                'bodyParam': [],
                'bodyInfo': {
                    'type': 0,
                    'rawType': 0,
                    'rawTextRemark': '',
                    'rawFileRemark': '',
                    'rawText': ''
                },
                'outParam': [{
                    'name': 'code',
                    'type': 0,
                    'remark': '返回码',
                    'must': 1,
                    'mock': ''
                }, {
                    'name': 'msg',
                    'type': 0,
                    'remark': '返回消息',
                    'must': 1,
                    'mock': ''
                }],
                'outInfo': {
                    'type': 0,
                    'rawRemark': '',
                    'rawMock': '',
                    'jsonType': 0
                },
                'restParam': []
            }]
        }

        interfaces = doc.get_interfaces()
        if not interfaces.get((data['url'], data['method'])):
            doc.create_interface(data=data, group_id=group['group_id'])

        # 代码生成接口
        data = {
            'name': '代码生成',
            'url': '/v1/code/generate',
            'method': 'POST',
            'remark': '根据ORM定义生成代码模板',
            'finish': '0',
            'param': [{
                'before': {
                    'mode': 0,
                    'code': ''
                },
                'after': {
                    'mode': 0,
                    'code': ''
                },
                'name': 'default',
                'id': str(uuid.uuid1()),
                'remark': '',
                'header': [],
                'queryParam': [],
                'bodyParam': [],
                'bodyInfo': {
                    'type': 1,
                    'rawType': 0,
                    'rawTextRemark': '',
                    'rawFileRemark': '',
                    'rawText': ''
                },
                'outParam': [],
                'outInfo': {
                    'type': 1,
                    'rawRemark': '',
                    'rawMock': '',
                    'jsonType': 0
                },
                'restParam': []
            }]
        }

        if not interfaces.get((data['url'], data['method'])):
            doc.create_interface(data=data, group_id=group['group_id'])

    except Exception as inst:
        if not all([
                   app.config.get('DOCLEVER_HOST'),
                   app.config.get('DOCLEVER_LOGIN'),
                   app.config.get('DOCLEVER_PASSWORD'),
                   app.config.get('PROJECT_NAME')]):
            print('flask_doclever error: please check app config exist('
                  'DOCLEVER_HOST, DOCLEVER_LOGIN, DOCLEVER_PASSWORD, PROJECT_NAME)')
        else:
            print('flask_doclever error: {}'.format(str(inst)))
            print(('please check: DOCLEVER_HOST({}), DOCLEVER_LOGIN({}), '
                   'DOCLEVER_PASSWORD({}), PROJECT_NAME({})'
                   .format(app.config.get('DOCLEVER_HOST'),
                           app.config.get('DOCLEVER_LOGIN'),
                           app.config.get('DOCLEVER_PASSWORD'),
                           app.config.get('PROJECT_NAME'))))


class DOClever(object):
    # route
    route = {}

    def __init__(self, *, app):
        super(DOClever, self).__init__()

        self.host = app.config['DOCLEVER_HOST']
        self.session = requests.session()

        # 登陆doclever
        data = {
            'name': app.config['DOCLEVER_LOGIN'],
            'password': app.config['DOCLEVER_PASSWORD']}
        r = self.session.post(url='{host}/user/login'.format(host=self.host), data=data)

        if r.status_code == 200:
            # 用户ID
            self.user_id = r.json()['data']['_id']

        # 项目ID
        project = self.create_project(app.config['PROJECT_NAME'])
        self.project_id = project['project_id']

    # 取得指定项目名称的项目信息
    def get_project(self, *, name):
        url = (
            '{host}/project/list?sbdoctimestamps={ts}'
            .format(
                host=self.host,
                ts=int(time.time())))

        r = self.session.get(url=url)
        if r.status_code == 200:
            project = {}
            data = r.json()['data']['project']['create']
            for project in data:
                if project['name'] == name:
                    return {
                        'project_name': project['name'],
                        'project_id': project['_id'],
                    }

            return None
        else:
            return r.status_code

    # 取得全部分组列表
    def get_groups(self):
        url = (
            '{host}/project/interface?id={project_id}&sort=0&sbdoctimestamps={ts}'
            .format(
                host=self.host,
                project_id=self.project_id,
                ts=int(time.time())))

        r = self.session.get(url=url)
        if r.status_code == 200:
            groups = {
                group['name']: group['_id']
                for group in r.json()['data']['data']
            }
            return groups
        else:
            return r.status_code

    # 取得全部接口列表
    def get_interfaces(self):
        def parse_interfaces(data, interfaces):
            for group in data:
                for interface in group['data']:
                    if interface.get('parent'):
                        parse_interfaces([interface], interfaces)
                    else:
                        interfaces[(interface['url'], interface['method'])] = {
                            'group_id': group['_id'],
                            'group_name': group['name'],
                            'interface_id': interface['_id'],
                            'interface_name': interface['name'],
                            'interface_url': interface['url'],
                            'interface_method': interface['method']}

        url = (
            '{host}/project/interface?id={project_id}&sort=0&sbdoctimestamps={ts}'
            .format(
                host=self.host,
                project_id=self.project_id,
                ts=int(time.time())))

        r = self.session.get(url=url)
        if r.status_code == 200:
            interfaces = {}
            data = r.json()['data']['data']
            parse_interfaces(data, interfaces)
            return interfaces
        else:
            return r.status_code

    # 取得指定ID的接口信息
    def get_interface(self, *, interface_id, group_id):
        url = (
            '{host}/interface/item'
            '?id={id}&group={group}&project={project}&sbdoctimestamps={ts}'
            .format(
                host=self.host,
                id=interface_id,
                group=group_id,
                project=self.project_id,
                ts=int(time.time())))

        r = self.session.get(url=url)
        if r.status_code == 200:
            data = r.json()['data']
            return data
        else:
            return r.status_code

    # 创建项目
    def create_project(self, project_name, comment=None):
        # 如已存在项目，直接返回
        project = self.get_project(name=project_name)
        if project:
            return project

        url = '{host}/project/create'.format(host=self.host)
        data = {'name': project_name, 'dis': comment or ''}

        r = self.session.post(url=url, data=data)
        body = r.json()
        if body['code'] == 200:
            return {'id': body['data']['_id'], 'name': project_name}
        else:
            return None

    # 创建分组
    def create_group(self, group_name):
        # 如已存在分组，直接返回
        groups = self.get_groups()
        group_id = groups.get(group_name)
        if group_id:
            return {'group_name': group_name, 'group_id': group_id}

        url = '{host}/group/create'.format(host=self.host)
        data = {'id': self.project_id, 'name': group_name}

        r = self.session.post(url=url, data=data)
        body = r.json()
        if body['code'] == 200:
            for group in body['data']:
                if group['name'] == group_name:
                    return {'group_name': group_name, 'group_id': group['_id']}
        else:
            return None

    # 创建接口
    def create_interface(self, *, data, group_id=None, id=None):
        url = '{host}/interface/create'.format(host=self.host)

        data['project'] = self.project_id

        if not group_id:
            group_id = self.create_group('default')['group_id']

        data['group'] = group_id

        if id:
            data['id'] = id

        data['param'] = json.dumps(data['param'])
        r = self.session.post(url=url, json=data)
        if r.status_code == 200:
            data = r.json()
            return data
        else:
            return r.status_code


class Source(object):
    route = {}

    def __init__(self, *, app, fields):
        self.app = app
        self.fields = fields
        self.field_remark = Source.parse_fields(fields=self.fields)

    # 采集路由(用于api.add_resource)
    @classmethod
    def collect_route(cls, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            resource_cls = args[0]
            url = args[1]

            # 转为doclever的url
            pattern = re.compile('<(?:int|string):(\w+)>')
            doc_url = pattern.sub(r'{\1}', url)

            cls.route[doc_url] = {'resource': resource_cls, 'url': url}
            return func(*args, **kwargs)
        return wrapper

    @classmethod
    def parse_fields(cls, *, fields):
        # 生成response字段的全部注释字典
        field_remark = {}
        comment = ''
        comment_level = 0
        nested_prefix = [None] * 10
        tab_width = 4

        def get_level(line):
            space = 0
            for char in line:
                if char == ' ':
                    space += 1
                else:
                    break
            level = int(space / tab_width) - 1

            return level

        for line in inspect.getsourcelines(fields)[0]:
            if len(line) < tab_width:
                continue

            if '#' in line:
                level = get_level(line)

                line = line.strip()
                if line[0] == '#':
                    comment = line[2:]
                    comment_level = level
            elif line[tab_width] != ' ' and ' = {' in line:
                index = line.find(' =')
                key = line[tab_width: index]
                nested_prefix[0] = key
                comment = ''
            elif ': ' in line:
                level = get_level(line)

                line = line.strip()
                index = line.find('\': ')
                name = line[1:index]

                nested_prefix[level] = name
                key = '.'.join(nested_prefix[:level+1])

                field_remark[key] = comment if comment_level == level else ''
                comment = ''

        return field_remark

    @classmethod
    def get_argtype(cls, resource):
        argument_type = {}

        if not hasattr(resource, 'req'):
            return argument_type

        for arg in resource.req.args:
            if hasattr(arg.type, '__name__'):
                if arg.type.__name__ in ['int',
                                         'float',
                                         'double',
                                         'positive_decimal',
                                         'natural',
                                         'positive']:
                    argument_type[arg.name] = DOCTYPE_NUM
                else:
                    argument_type[arg.name] = DOCTYPE_STR
            else:
                argument_type[arg.name] = DOCTYPE_STR

            if arg.action == 'append':
                argument_type[arg.name] = DOCTYPE_LIST

        return argument_type

    @classmethod
    def generate_response(cls, *, name, value, prefix, field_remark):
        key = prefix + '.' + name if name else prefix
        remark = field_remark.get(key, '')

        response = {
            'name': name,
            'type': DOCTYPE_STR,
            'remark': remark,
            'must': 1,
            'mock': '',
        }

        number_type = (fields.Integer, fields.Float)
        if value == fields.String or isinstance(value, fields.String):
            response['type'] = DOCTYPE_STR
        elif value in number_type or isinstance(value, number_type):
            response['type'] = DOCTYPE_NUM
        elif value == fields.Boolean or isinstance(value, fields.Boolean):
            response['type'] = DOCTYPE_BOOL
        elif value == fields.List or isinstance(value, fields.List):
            response['type'] = DOCTYPE_LIST
            response['data'] = [
                cls.generate_response(
                    name=None,
                    value=value.container,
                    prefix=key,
                    field_remark=field_remark)]
        elif value == fields.Nested or isinstance(value, fields.Nested):
            response['type'] = DOCTYPE_DICT
            response['data'] = [
                cls.generate_response(
                    name=n,
                    value=v,
                    prefix=key,
                    field_remark=field_remark)
                for n, v in value.nested.items()]

        return response

    def parse_resource(self, *, resource, url):
        # 解析resource代码，生成doclever文档代码
        interfaces = []
        comment = ''
        body = {
            'type': 1,
            'rawType': 2,
            'rawTextRemark': '',
            'rawFileRemark': '',
            'rawText': '',
            'rawJSON': [],
            'rawJSONType': 0}
        query = []
        rest = []
        argument_type = Source.get_argtype(resource)

        # 转换url(/users/<int:id> -> /users/{id})
        pattern = re.compile('<(?:int|string):(\w+)>')
        rest_params = pattern.findall(url)
        if rest_params:
            url = pattern.sub(r'{\1}', url)

            # 解析地址参数
            rest = [{
                'name': rest_param,
                'remark': rest_param,
                'value': {
                    'type': 0,
                    'status': '',
                    'data': [{
                        'value': '1',
                        'remark': ''}]}}
                for rest_param in rest_params]

        for line in inspect.getsourcelines(resource)[0]:
            line = line.strip()
            if len(line) == 0:
                continue

            if line[0] == '#':
                # 注释
                comment = line[2:]
            elif 'add_body' in line or 'add_argument' in line:
                # body
                pattern = re.compile('(?:add_body|add_argument)\(\'(\w+)\'')
                result = pattern.findall(line)

                name = result[0]
                remark = comment
                comment = ''
                # 取得request参数解析的数据类型
                data_type = argument_type.get(name)

                body['rawJSON'].append({
                    'name': name,
                    'must': 1,
                    'type': data_type,
                    'remark': remark,
                    'show': len(body['rawJSON']),
                    'mock': '',
                    'drag': 1})
            elif '@' in line and 'get_page' in line:
                # query 页码
                query.append({
                    'name': 'page_no',
                    'must': 1,
                    'remark': '页码',
                    'value': {
                        'type': 0,
                        'data': [{
                            'value': 1,
                            'remark': ''}],
                        'status': ''}
                })
                query.append({
                    'name': 'page_size',
                    'must': 1,
                    'remark': '记录数',
                    'value': {
                        'type': 0,
                        'data': [{
                            'value': 10,
                            'remark': ''}],
                        'status': ''}
                })
            elif '@' in line and 'query_params' in line:
                # query
                pattern = re.compile('\\\'(\w+)\\\'')
                result = pattern.findall(line)

                # 注释
                index = line.find('#')
                remark = line[index+2::] if index != -1 else ''

                query.append({
                    'name': result[0],
                    'must': 0,
                    'remark': remark,
                    'value': {
                        'type': 0,
                        'data': [{
                            'value': '',
                            'remark': ''}],
                        'status': ''}
                })
            elif 'def ' in line and '__init__' not in line:
                # 创建上一个解析的接口
                # 函数体
                name = comment
                comment = ''

                if 'get' in line:
                    method = 'GET'
                elif 'post' in line:
                    method = 'POST'
                elif 'put' in line:
                    method = 'PUT'
                elif 'delete' in line:
                    method = 'DELETE'
                else:
                    continue

                interface = {
                    'name': name,
                    'method': method,
                    'url': url,
                    'remark': '',
                    'finish': '0',
                    'param': [{
                        'after': {
                            'code': '',
                            'mode': 0
                        },
                        'before': {
                            'code': '',
                            'mode': 0
                        },
                        'name': 'default',
                        'id': str(uuid.uuid1()),
                        'remark': '',
                        'header': [{
                            'name': 'Content-Type',
                            'value': 'application/json',
                            'remark': ''
                        }],
                        'outInfo': {
                            'type': 0,
                            'rawRemark': '',
                            'rawMock': '',
                            'jsonType': 0
                        },

                        'queryParam': query,
                        'bodyParam': [],
                        'bodyInfo': body if method in ('POST', 'PUT') else [],
                        'outParam': [
                            {
                                'mock': 'OK',
                                'must': 1,
                                'remark': '返回码',
                                'type': DOCTYPE_STR,
                                'name': 'code'
                            },
                            {
                                'mock': '正确',
                                'must': 1,
                                'remark': '返回消息',
                                'type': DOCTYPE_STR,
                                'name': 'msg'
                            }
                        ],
                        'restParam': rest
                    }]
                }

                interfaces.append(interface)

                # 清空参数
                query = []
            elif 'return' in line and 'get_value' in line:
                # 返回结果
                data = []

                index = line.rfind('.')
                field_name = line[index+1:-1] if index != -1 else ''
                if hasattr(self.fields, field_name):
                    for name, value in getattr(self.fields, field_name).items():
                        data.append(
                            Source.generate_response(
                                name=name,
                                value=value,
                                prefix=field_name,
                                field_remark=self.field_remark))

                interface['param'][0]['outParam'].append({
                    'mock': '',
                    'must': 1,
                    'remark': '记录总数',
                    'type': DOCTYPE_NUM,
                    'name': 'count'
                })

                interface['param'][0]['outParam'].append({
                    'data': [{
                        'name': None,
                        'type': 4,
                        'remark': '',
                        'must': 1,
                        'mock': '',
                        'data': data}],
                    'mock': '',
                    'must': 1,
                    'remark': '记录值',
                    'type': DOCTYPE_LIST,
                    'name': 'data'
                })

        return interfaces

    def merge_interface(self, *, new_interface, old_interface):

        new_interface['remark'] = old_interface['remark']
        new_interface['finish'] = old_interface['finish']

        # 更新参数项目
        old_param = old_interface['param'][0]
        new_param = new_interface['param'][0]

        # 合并query, 若文档中没有代码中同名query则新建，否则更新query内容
        old_query = {
            query['name']: {
                'remark': query['remark'],
                'value': query['value'],
                'must': query['must'],
                }
            for query in old_param['queryParam']}

        for query in new_param['queryParam']:
            if not query['remark']:
                query['remark'] = old_query.get(query['name'], {}).get('remark')

            query['value'] = old_query.get(query['name'], {}).get('value')
            query['must'] = old_query.get(query['name'], {}).get('must', 0)

        # 合并body, 若文档中没有代码中同名body则新建，否则更新body内容
        if new_param.get('bodyInfo'):
            old_body = {}
            if old_param.get('bodyInfo'):
                old_body = {
                    body['name']: {
                        'remark': body['remark'],
                        'value': body.get('value'),
                        'data': body.get('data'),
                        'type': body['type'],
                        'must': body['must'],
                        'mock': body['mock'],
                        }
                    for body in old_param['bodyInfo']['rawJSON']}

            for body in new_param['bodyInfo']['rawJSON']:
                old_body_item = old_body.get(body['name'])
                if not old_body_item:
                    continue

                if old_body_item.get('data'):
                    body['data'] = old_body_item.get('data')

                if old_body_item.get('value'):
                    body['value'] = old_body_item.get('value')

                body['mock'] = old_body_item.get('mock', '')
                body['must'] = old_body_item.get('must', 1)

        return new_interface

