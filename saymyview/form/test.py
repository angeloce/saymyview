
from saymyview.datamodel.user import User
from base import Form,ModelForm

from fields import *
from validators import *


# print User
#
#
#
# def model_form(model_class):
#     if isinstance(model_class, Table):
#         pass
#
#
# class TForm(Form, User):
#     pass
#
#
# t = TForm()
# print t._fields


class TestForm(Form):
    ac = TextField('ac', validators=[url()])
    dc2 = TextField('dc2')



form = TestForm({'ac2': '33333333', 'dc2': '12222'})
if not form.validate():
    for e in form.errors:
        print e, form.errors[e][0]

