#############################################
# File Name: setup.py
# Author: duanliangcong
# Mail: 137562703@qq.com
# Created Time:  2022-11-02 15:00:00
#############################################

from jsonpath import jsonpath
import requests
import pytest
import time
import json
import os, sys
import re
import ast
import traceback
from ddreport.api import PytestQuery
from ddreport.db import PytestMysql
from ddreport.orm import PytestOrm
from ddreport.func import PytestFunctions


requests.packages.urllib3.disable_warnings()

test_result = {
    "title": "",
    "desc": "",
    "tester": "",
    "start_time": "",
    "end_time": "",
    "failed": 0,
    "passed": 0,
    "skipped": 0,
    "error": 0,
    "cases": [],
}

dict_data = {
    "project": '',
    "model_sub": '0'
}


def getEnvData(env_path, env_name):
    try:
        with open(env_path, 'r', encoding='utf-8')as f:
            envs = json.loads(f.read())
        return jsonpath(envs, f'$..[?(@.env_name=="{env_name}")]')[0]
    except Exception:
        return dict()


def node_handle(node, item, call):
    d = dict()
    # 模块
    model_path = item.location[0].replace('.py', '').replace('\\', '/')
    d['model'] = dict_data['project'] + '/'.join(model_path.split('/')[int(dict_data['model_sub']):])
    # 类
    cf = item.location[-1].split('.')
    d['classed'] = None if len(cf) == 1 else cf[0]
    # 方法
    d['method'] = item.originalname
    # 描述
    d['doc'] = item.function.__doc__
    # 响应时间
    d['duration'] = str(call.duration)[:4]
    # 结果
    d['status'] = node.outcome
    # 详细内容
    if node.sections:
        d["print"] = ''.join(node.sections[0][1:]).replace('<', '&lt;').replace('>', '&gt;')

    if call.excinfo:
        try:
            excinfo = {"info": call.excinfo.value.value.value}
        except Exception:
            try:
                excinfo_str = re.findall(r'<ExceptionInfo.*?\("(.*?)"', str(call.excinfo))[0].replace('\\n', '\n')
            except Exception:
                excinfo_str = str(call.excinfo)
                sub_len = len(re.findall('tblen=\d+>', excinfo_str)[-1])
                excinfo_str = excinfo_str[:-sub_len]
                if excinfo_str.startswith('<'):
                    excinfo_str = excinfo_str[1:]
                if excinfo_str.endswith('>'):
                    excinfo_str = excinfo_str[:-1]
            try:
                if d['status'] != 'skipped':
                    _traceback = excinfo_str + '\n' + '\n'.join([str(i) for i in call.excinfo._traceback])
                else:
                    _traceback = excinfo_str.replace('ExceptionInfo ', '')
            except Exception:
                _traceback = '未知错误'
            excinfo = {"error": _traceback.replace('<', '&lt;').replace('>', '&gt;')}
        d.update(excinfo)
    return d


def pytest_addoption(parser):
    """添加main的可调用参数"""
    group = parser.getgroup("testreport")
    group.addoption(
        "--ddreport",
        action="store",
        default=None,
        help="测试报告标识",
    )
    group.addoption(
        "--title",
        action="store",
        default=None,
        help="测试报告最顶部标题",
    )
    group.addoption(
        "--desc",
        action="store",
        default=None,
        help="当前测试报告的说明",
    )
    group.addoption(
        "--tester",
        action="store",
        default=None,
        help="测试人员",
    )
    group.addoption(
        "--project",
        action="store",
        default=None,
        help="项目名称",
    )
    group.addoption(
        "--model_sub",
        action="store",
        default=None,
        help="测试模块显示的范围",
    ),
    group.addoption(
        "--env_path",
        action="store",
        default=None,
        help="环境配置路径",
    ),
    group.addoption(
        "--env_name",
        action="store",
        default=None,
        help="环境名称",
    ),
    group.addoption(
        "--receive_dict",
        action="store",
        default=None,
        help="接收一个字典类型的参数",
    ),


def pytest_sessionstart(session):
    test_result['start_time'] = time.strftime("%Y-%m-%d %H:%M:%S")
    test_result['title'] = session.config.getoption('--title') or ''
    test_result['tester'] = session.config.getoption('--tester') or ''
    test_result['desc'] = session.config.getoption('--desc') or ''
    dict_data['project'] = session.config.getoption('--project') or ''
    dict_data['model_sub'] = session.config.getoption('--model_sub') or '0'


def pytest_sessionfinish(session, exitstatus):
    def set_default(obj):
        if isinstance(obj, (list, dict)):
            return str(obj).replace('<', '&lt;').replace('>', '&gt;')
            # return f'{obj} ************************'
        # raise TypeError
    test_result['end_time'] = time.strftime("%Y-%m-%d %H:%M:%S")
    ddreport = session.config.getoption('--ddreport')
    if ddreport:
        report_dirOrFile = ddreport.replace('\\', '/').strip()
        if not report_dirOrFile.endswith('.html'):
            report_dir, report_name = report_dirOrFile, f'testReport {time.strftime("%Y-%m-%d_%H%M%S")}.html'
        else:
            report_dir, report_name = '/'.join(report_dirOrFile.split('/')[:-1]), report_dirOrFile.split('/')[-1]
        if not os.path.exists(report_dir):
            os.makedirs(report_dir)
        report_save_path = os.path.join(report_dir, report_name)
        # 读取测试报告文件
        template_path = os.path.join(os.path.dirname(__file__), './template')
        with open(f'{template_path}/index.html', 'r', encoding='utf-8')as f:
            template = f.read()
        # report_template = template.replace('templateData', json.dumps(test_result, default=set_default))
        report_template = template.replace('templateData', json.dumps(test_result))
        with open(report_save_path, 'w', encoding='utf-8') as f:
            f.write(report_template)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == 'call':
        test_result[report.outcome] += 1
        info = node_handle(report, item, call)
        test_result["cases"].append(info)
    elif report.outcome == 'failed':
        report.outcome = 'error'
        test_result['error'] += 1
        info = node_handle(report, item, call)
        test_result["cases"].append(info)
    elif report.outcome == 'skipped':
        test_result[report.outcome] += 1
        info = node_handle(report, item, call)
        test_result["cases"].append(info)


@pytest.fixture(scope='session')
def ddreport(request):
    # 环境获取
    env_path = request.config.getoption("--env_path")
    env_name = request.config.getoption("--env_name")
    get_env = getEnvData(env_path, env_name)
    # 全局变量
    receive_dict = request.config.getoption("--receive_dict")
    if receive_dict:
        try:
            receive_dict = json.loads(receive_dict)
        except Exception:
            receive_dict = ast.literal_eval(receive_dict)
        except Exception:
            receive_dict = None
    host = get_env.get('host') or ''
    db = get_env.get('db') or None
    db_ssh = get_env.get('db_ssh') or None
    orm = get_env.get('orm') or None
    return MyFixture(host, db, db_ssh, receive_dict, orm)


class MyFixture:
    def __init__(self, host, _db, ssh_db, receive_dict, orm):
        self.API = PytestQuery(host)
        self.FC = PytestFunctions()
        if _db:
            from ddreport.db import PytestMysql
            self.DB = PytestMysql(_db, ssh_db)
        else:
            self.DB = None
        if orm:
            from ddreport.orm import PytestOrm
            self.ORM = PytestOrm(orm)
        else:
            self.ORM = None
        self.GVALUE = dict()
        if isinstance(receive_dict, dict):
            self.GVALUE.update(receive_dict)
        super().__init__()