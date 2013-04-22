#coding:utf-8


import os
import sys

sys.path.insert(0, os.path.abspath('..'))

from saymyview.web.application import application
from saymyview.web.models.session import *



from sqlalchemy import event





s = Session.select().all()
for i in s:
    print i.session_data
    i.set(user='222222222222')





