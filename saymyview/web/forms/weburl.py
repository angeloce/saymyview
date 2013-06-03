
from saymyview.datamodel.user import User
from saymyview.form.base import Form,ModelForm

#from fields import *








class TForm(ModelForm, User):
    pass


t = TForm()
print t._fields








# class TestForm(Form):
#     ac = TextField('ac')
#     dc2 = TextField('dc2')
#
#
#
# form = TestForm({'ac2': '33333333', 'dc2': '12222'})
# if not form.validate():
#     for e in form.errors:
#         print e, form.errors[e][0]

