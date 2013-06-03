#coding:utf-8

import re
from tornado.escape import to_unicode
from tornado.options import options
from validators import ValidateError, Required

__all__ = ['BaseForm', 'FormMeta', 'TornadoForm']





class Field(object):
    def __init__(self, label=None, validators=None, name=None, filters=tuple(),
                 optional=False, default=None):
        self.name = name
        self.label = label or name
        if validators is None:
            validators = []
        self.validators = validators
        self.filters = filters
        self.type = type(self).__name__
        self.default = default
        self.raw_data = None
        self.optional = optional
        self.errors = []
        self._has_validated = False

    def validate(self, form):

        if self._has_validated:
            return self.errors

        if not self.optional:
            for validator in self.validators:
                if isinstance(validator, Required):
                    break
            else:
                self.validators.insert(0, Required())

        # Run validators
        for validator in self.validators:
            try:
                validator(self, form.raw_data)
            except ValidateError, err:
                self.errors.append(err.message)
                if err.stopped:
                    break

        return len(self.errors) == 0

    def process(self, formdata, data):
        """
        Process incoming data, calling process_data, process_formdata as needed,
        and run filters.

        If `data` is not provided, process_data will be called on the field's
        default.

        Field subclasses usually won't override this, instead overriding the
        process_formdata and process_data methods. Only override this for
        special advanced processing, such as when a field encapsulates many
        inputs.
        """
        self.process_errors = []
        try:
            self.process_data(data)
        except ValueError as e:
            self.process_errors.append(e.args[0])

        # logical fix. obj is the default value
        if formdata and self.name in formdata:
            try:
                self.raw_data = formdata.getlist(self.name)
                self.process_formdata(self.raw_data)
            except ValueError as e:
                self.process_errors.append(e.args[0])

        for _filter in self.filters:
            try:
                self.data = _filter(self.data)
            except ValueError as e:
                self.process_errors.append(e.args[0])

    def process_data(self, value):
        """
        Process the Python data applied to this field and store the result.

        This will be called during form construction by the form's `kwargs` or
        `obj` argument.

        :param value: The python object containing the value to process.
        """
        self.data = value

    def process_formdata(self, valuelist):
        """
        Process data received over the wire from a form.

        This will be called during form construction with data supplied
        through the `formdata` argument.

        :param valuelist: A list of strings to process.
        """
        if valuelist:
            self.data = to_unicode(valuelist[0])
        else:
            self.data = to_unicode(None)





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
        if "_fields" in attrs:
            fields.update(attrs["_fields"])

        found_fields = [(name, attr) for name, attr in attrs.items()
                        if not name.startswith('__') and isinstance(attr, Field)]

        for name, field in found_fields:
            field = attrs[name]
            field.name = name
            fields[name] = field
            del attrs[name]

        attrs["_fields"] = fields
        return type.__new__(cls, name, bases, attrs)


class Form(object):
    __metaclass__ = MetaForm

    def __init__(self, data=None):
        self._data = data or {}

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

    def validate(self):
        is_ok = True
        for name, field in self._fields.items():
            if not field.validate(self):
                is_ok = False
        return is_ok

    @property
    def data(self):
        return {name: field.data for name, field in self._fields.items()}

    @property
    def raw_data(self):
        return self._data

    @property
    def errors(self):
        if not hasattr(self, "_errors"):
            self._errors = {name: field.errors for name, field in self._fields.items() if field.errors}
        return self._errors


class MetaModelForm(MetaForm):
    def __new__(cls, name, bases, attrs):
        if "model" not in attrs:
            raise ValueError(u"ModelForm need one juti model")
        model = attrs["model"]

        return MetaForm.__new__(cls, name, bases, attrs)


class ModelForm(Form):
    def __init__(self, data, instance=None):
        Form.__init__(self, data)
        self.instance = instance

    def save(self):
        pass


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

