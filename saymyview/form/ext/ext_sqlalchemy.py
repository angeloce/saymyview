#coding:utf-8

from sqlalchemy import *
from saymyview.form.fields import *

def mady_form(table):
    if not isinstance(table, Table):
        if hasattr(table, "__table__"):
            table = table.__table__

    columns = dict(table.columns)

    fields = []

    for name, column in columns.items():
        if isinstance(column.type, Integer):
            field = IntegerField()
        elif isinstance(column.type, String):
            field = TextField()
        else:
            field = TextField()

        field.name = column.name
        field.label = column.name
        field.type = column.type
        field.default = column.default
        field.optional = column.nullable
