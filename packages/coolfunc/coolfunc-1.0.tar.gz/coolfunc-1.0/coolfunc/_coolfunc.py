'''
Copyright [2023] [许灿标]
license: Apache License, Version 2.0
email: lcctoor@outlook.com
'''

from vtype import SysEmpty

# 以下模块允许被其它模块导入
from json import dumps as jsonDumps
from json import loads as jsonLoads
from pickle import dumps as pickleDumps
from pickle import loads as pickleLoads
from pathlib import Path as libpath
from os.path import abspath


def jsonChinese(data): return jsonDumps(data, ensure_ascii=False)

# 三元表达式
def ternary(tv, obj, fv): return tv if obj else fv

def setDir(path):
    return libpath(path).mkdir(parents=True, exist_ok=True)
def setParentDir(path):
    return libpath(path).parent.mkdir(parents=True, exist_ok=True)

def readJson(fpath, default=SysEmpty, mode=3):
    '''
    mode:
        等于1时: 文件不存在时返回default
        等于2时: 文件内容解析错误时返回default
        等于3时: 无论哪种错误, 都返回default
    '''
    try:
        return jsonLoads(libpath(fpath).read_text('utf8'))
    except BaseException as e:
        if default is not SysEmpty:
            if mode == 3: return default
            if mode == 1 and type(e) is FileNotFoundError: return default
        raise

def writeJson(fpath, data, ensure_ascii=False):
    fpath = libpath(fpath)
    data = jsonDumps(data, ensure_ascii=ensure_ascii)
    try:
        return fpath.write_text(data, 'utf8')
    except FileNotFoundError:
        fpath.parent.mkdir(parents=True, exist_ok=True)
        return fpath.write_text(data, 'utf8')

def rePathClash(path):
    # 解决命名冲突
    while libpath(path).exists():
        path += '_'
    return path