"""
@author: 益章
@contact: WX:YiZhang_You 
@Created on: 2023/3/28 21:43
@Remark: 
"""

import json
import re
import traceback
from ast import literal_eval
from collections import namedtuple
from json import JSONDecodeError
from urllib import parse

from pymongo import MongoClient


class PyMongoRawQuery:
    """mongo原生查询（只支持查询）"""

    def printt(self):
        print(11)
