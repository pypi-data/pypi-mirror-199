from ddreport.exceptd import exceptContentObj
from jsonpath import jsonpath
import requests
import ast
import traceback
import json
requests.packages.urllib3.disable_warnings()


def set_default(obj):
    if not isinstance(obj, (list, dict)):
        return str(obj).replace('<', '&lt;').replace('>', '&gt;')


class PytestQuery:
    def __init__(self, host=''):
        self.__HOST = host

    # 加载错误信息并抛出异常
    def __errdata(self, dict_data):
        if isinstance(dict_data, dict):
            self.__info.update(dict_data)
        self.__execptions()

    # 抛出异常
    def __execptions(self):
        exceptContentObj.raiseException(self.__info)

    # 接口请求
    def __pyQueryData(self, kwargs):
        self.__info = dict()
        if not kwargs['url'].startswith('http'):
            kwargs['url'] = self.__HOST + kwargs['url']
        try:
            r = requests.request(**kwargs)
        except Exception  as e:
            self.__errdata({"错误详情": f"{traceback.format_exc()}"})
        try:
            response = r.json()
        except Exception:
            response = r.text.replace('<', '&lt;').replace('>', '&gt;')
        # 一个完整的信息
        jd1 = json.dumps(kwargs, indent=4, ensure_ascii=False, default=set_default)
        jd2 = json.dumps(dict(r.headers), indent=4, ensure_ascii=False)
        jd3 = json.dumps(r.cookies.get_dict(), indent=4, ensure_ascii=False)
        jd4 = json.dumps(response, indent=4, ensure_ascii=False, default=set_default)
        self.__info.update({"请求内容": jd1, "响应头": jd2, "响应Cookies": jd3, "响应体": jd4})
        return r

    def __assertType(self, k_v):
        if k_v.upper() not in ["JSON", "TEXT"]:
            self.__errdata({"错误详情": f"断言异常，类型只能为JSON或TEXT"})

    # json断言数据类型判断
    def __assertParamsType(self, check):
        if not isinstance(check, (dict, list)):
            self.__errdata({"错误详情": f"断言异常，参数必须为json类型\n{check}"})
        if isinstance(check, dict):
            check = [check]
        return check

    # 响应的json数据类型判断
    def __assertDataType(self, r):
        try:
            response = r.json()
            return response
        except Exception:
            self.__errdata({"错误详情": f"响应体不是JSON类型"})

    # json数据匹配
    def __assertJsonCheck(self, data1, data2, n):
        if data1['value'] != data2:
            data1 = str(data1).replace('<', '&lt;').replace('>', '&gt;')
            self.__errdata({"失败详情": f"*** 断言匹配失败\n条数：{n + 1}\n匹配详情:{data1}"})

    # 文本数据匹配
    def __assertTextCheck(self, data1, data2, n):
        if data1['value'] not in data2:
            data1 = str(data1).replace('<', '&lt;').replace('>', '&gt;')
            self.__errdata({"失败详情": f"*** 断言匹配失败\n条数：{n + 1}\n匹配详情:{data1}"})

    # 断言主程序
    def __assertData(self, r, check):
        # 没有断言时的返回
        if not check:
            if r.status_code == 200:
                return r
            else:
                self.__errdata(None)
        # 断言验证
        else:
            check = self.__assertParamsType(check)
            for n, ass in enumerate(check):
                if ass['type'].upper() == 'JSON':
                    response = self.__assertDataType(r)
                    jsonpath_results = jsonpath(response, ass.get('exp')) or []
                    json_result = jsonpath_results[0] if len(jsonpath_results) == 1 else jsonpath_results
                    self.__assertJsonCheck(ass, json_result, n)
                elif ass['type'].upper() == 'TEXT':
                    if not isinstance(ass['value'], str):
                        ass['value'] = str(ass['value'])
                    self.__assertTextCheck(ass, r.text, n)
                else:
                    self.__assertType(ass['type'])
            return r

    def query(self, kwargs, check=None):
        r = self.__pyQueryData(kwargs)
        return self.__assertData(r, check)