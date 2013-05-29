#coding:utf-8

from sqlalchemy import event
from sqlalchemy.orm import validates

from saymyview.datamodel.base import BaseModel
from saymyview.datamodel.tables import web_url_table


class WebUrl(BaseModel):
    __table__ = web_url_table

    @validates('url')
    def validate_url(self, key, url):
        return url


# def check_url_valid(mapper, connection, target):
#     pass
#
# event.listen(WebLink, 'before_insert', check_url_valid)
