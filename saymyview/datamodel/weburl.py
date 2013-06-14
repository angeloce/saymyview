#coding:utf-8

from sqlalchemy.orm import validates

from saymyview.datamodel.base import BaseModel
from saymyview.datamodel.tables import web_url_table, web_url_script_table


class WebUrlModel(BaseModel):
    __table__ = web_url_table

    @validates("url")
    def validate_url(self, key, url):
        return url


class WebUrlScriptModel(BaseModel):
    __table__ = web_url_script_table
