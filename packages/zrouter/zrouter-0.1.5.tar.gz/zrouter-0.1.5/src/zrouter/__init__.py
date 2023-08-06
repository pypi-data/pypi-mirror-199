from flask import Blueprint, request
from zrouter.exception import MessagePrompt
from inspirare import json, random
import json as json_ 


class RouterUtility:
    @staticmethod
    def get_params():
        """ 获取路由参数"""
        if request.method == 'GET':
            return json.to_lowcase(request.args)
        elif 'upload' in str(request.url_rule):
            file_data = request.files['file']
            return {
                'file_data': file_data,
                'file_params': request.form.to_dict()
            }
        else:
            request_data = request.get_data()
            if request_data:
                try:
                    params = json_.loads(request_data.decode('utf-8'))
                    if isinstance(params, dict):
                        return json.to_lowcase(params)
                except Exception as e:
                    print(e)
                    return {'data': request_data}
            else:
                return {}

    @staticmethod
    def clean_params(params):
        """空值参数清理"""
        tmp = {}
        for k, v in params.items():
            if v == '': 
                tmp[k] = None
            elif v == 'null':
                tmp[k] = None
            elif v is None:
                pass
            else:
                tmp[k] = v
        return tmp


class Router(Blueprint, RouterUtility):
    """路由"""
    def __init__(self, *args, **kwargs):
        Blueprint.__init__(self, *args, **kwargs)

    def route_(self, rule, **options):
        """改写route方法, 解决endpoint重名问题"""
        def decorator(f):
            name = random.string(5)
            endpoint = options.pop("endpoint", name)
            self.add_url_rule(rule, endpoint, f, **options)
            return f
        return decorator

    def before_route(self):
        return True

    def on_route(self, func, params, is_direct):
        """路由处理函数"""
        code = 200
        msg = '操作成功'
        data = []
        try:
            data = func(params)
            if is_direct:
                return data
        except Exception as e:
            if isinstance(e, MessagePrompt):
                code = 500       
                msg = str(e)
            else: 
                raise e
        if isinstance(data, dict):
            data = json.iter_camel(data)
        elif isinstance(data, list):
            try:
                data = [json.iter_camel(item) for item in data]
            except AttributeError:
                pass
        return {
            'code': code,
            'msg': msg,
            'data': data
        }

    def add(self, *args, **kwargs):
        is_open = kwargs.pop('open', False)
        is_direct = kwargs.pop('direct', False)
        def wrapper(func):
            @self.route_(*args, **kwargs)
            def wrapper_(*args_, **kwargs_):
                params = self.get_params()
                params = self.clean_params(params)
                if not self.before_route():
                    if not is_open:
                        return {
                            'code': 401,
                            'msg': '用户无权限',
                        }
                return self.on_route(func, params, is_direct)
            return wrapper_
        return wrapper
