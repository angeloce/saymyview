
import re
from tornado.escape import to_unicode
from tornado.options import options

__all__ = ['BaseForm', 'FormMeta', 'TornadoForm']



class BaseField(object):
    pass



class BaseForm(object):
    pass

class MetaForm(type):
    """
    The metaclass for `Form` and any subclasses of `Form`.

    `FormMeta`'s responsibility is to create the `_unbound_fields` list, which
    is a list of `UnboundField` instances sorted by their order of
    instantiation.  The list is created at the first instantiation of the form.
    If any fields are added/removed from the form, the list is cleared to be
    re-generated on the next instantiaton.

    Any properties which begin with an underscore or are not `UnboundField`
    instances are ignored by the metaclass.
    """


    def __new__(cls, name, bases, attrs):
        fields = {}
        for name in attrs:
            if not name.startswith('__') and isinstance(attrs[name], BaseField):
                field = attrs[name]
                field.name = name
                fields[name] = field
        attrs["_fields"] = fields
        return type.__new__(cls, name, bases, attrs)


class Form(BaseForm):
    __metaclass__ = MetaForm

    def __init__(self, data=None):
        self._data = data or {}
        self._errors = None

    def process(self, formdata=None, obj=None, **kwargs):
        """
        Take form, object data, and keyword arg input and have the fields
        process them.

        :param formdata:
            Used to pass data coming from the enduser, usually `request.POST` or
            equivalent.
        :param obj:
            If `formdata` has no data for a field, the form will try to get it
            from the passed object.
        :param `**kwargs`:
            If neither `formdata` or `obj` contains a value for a field, the
            form will assign the value of a matching keyword argument to the
            field, if provided.
        """
        if formdata is not None and not hasattr(formdata, 'getlist'):
            formdata = _TornadoArgumentsWrapper(formdata)

        for name, field, in self._fields.iteritems():
            if obj is not None and hasattr(obj, name):
                field.process(formdata, getattr(obj, name))
            elif name in kwargs:
                field.process(formdata, kwargs[name])
            else:
                field.process(formdata)

    def validate(self, extra_validators=None):
        print self._fields
        is_ok = True
        for name, field in self._fields.items():
            if name not in self._data:
                if not field.optional:
                    is_ok = False
                    raise
            else:
                if not field.validate(self, self._data[name]):
                    is_ok = False
        return is_ok

    @property
    def data(self):
        return dict((name, f.data) for name, f in self._fields.iteritems())

    @property
    def errors(self):
        if self._errors is None:
            self._errors = dict((name, f.errors) for name, f in self._fields.iteritems() if f.errors)
        return self._errors



class _TornadoArgumentsWrapper(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError:
            raise AttributeError

    def getlist(self, key):
        try:
            values = []
            for v in self[key]:
                v = to_unicode(v)
                if isinstance(v, unicode):
                    v = re.sub(r"[\x00-\x08\x0e-\x1f]", " ", v)
                values.append(v)

            values.reverse()
            return values
        except KeyError:
            raise AttributeError

