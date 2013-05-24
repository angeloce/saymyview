#coding:utf-8


from saymyview.utils import date
from saymyview.datamodel.base import BaseModel
from saymyview.datamodel.tables import session_table


class Session(BaseModel):
    __table__ = session_table
    # DO NOT use session_data field directly

    def set(self, **kwargs):
        if self.session_data is None:
            self.session_data = {}
        for name, value in kwargs.items():
            if value is None and value in self.session_data:
                del self.session_data[name]
                continue
            self.session_data[name] = value
        self.update()

    def get(self, name, default=None):
        if not self.session_data:
            return None
        return self.session_data.get(name, default)

    @classmethod
    def get_session(cls, session_id):
        session = cls.select().filter_by(session_id=session_id).first()
        if session and session.expires < date.now():
            return session.delete()
        return session

