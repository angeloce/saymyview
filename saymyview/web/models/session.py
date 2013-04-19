#coding:utf-8


import json
from sqlalchemy import event

from saymyview.utils import date
from saymyview.web.models.base import BaseModel
from saymyview.web.models.tables import session_table



class Session(BaseModel):
    __table__ = session_table
    # DO NOT use session_data field directly

    def set(self, **kwargs):
        for name, value in kwargs.items():
            if value is None and value in self.session_data:
                del self.session_data[name]
                continue
            self.session_dict[name] = value
        self.update()

    def get(self, name, default=None):
        return self.session_data.get(name, default)

    @classmethod
    def get_session(cls, session_id):
        session = cls.select().filter_by(session_id=session_id).first()
        if session and session.expires < date.now():
            return session.delete()
        return session



def json_dump_session_data(target):
    if not hasattr(target, "session_dict"):
        json_load_session_data(target)
    print 'dump'
    target.session_data = json.dumps(target.session_dict)



def json_load_session_data(target):
    try:
        session_data = json.loads(target.session_data)
    except:
        session_data = {}
    target.session_dict = session_data


def asdkf(mapper, connection, target):
    print 'ddddddddddddddddddddddddddddddddddd'
    json_dump_session_data(target)

event.listen(Session, "load", lambda target, context: json_load_session_data(target))
# event.listen(Session, "before_insert", lambda mapper, connection, target: json_dump_session_data(target))
# event.listen(Session, "before_update", lambda mapper, connection, target: json_dump_session_data(target))
event.listen(Session, "before_insert", asdkf)
event.listen(Session, "before_insert", asdkf)




