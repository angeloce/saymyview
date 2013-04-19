#coding:utf-8


import os
import sys

sys.path.insert(0, os.path.abspath('..'))

from saymyview.web.application import application
from saymyview.web.models.session import *



from sqlalchemy import event





s = Session.create_session('fffffff43ffffffff', {"df":3})
print s.session_data




