

from base import Form

from fields import *



class TestForm(Form):
    ac = TextField('ac')
    dc2 = TextField('dc2', maxlength=3)



form = TestForm({'ac': '33333333', 'dc2': '12222'})
if form.validate():
    print form.errors
