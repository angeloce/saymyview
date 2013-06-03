
import itertools
import datetime
import time
from tornado.escape import to_unicode, utf8
import widgets

from base import Field, ValidateError

__all__ = (
    'Field', 'TextField',
)


class TextField(Field):
    def __call__(self, **kwargs):
        if self.maxlength:
            kwargs['maxlength'] = str(self.maxlength)
        return self.widget(self, **kwargs)

    def _value(self):
        if self.data:
            return to_unicode(self.data)
        return to_unicode('')


class HiddenField(TextField):
    """
    Represents an ``<input type="hidden">``.
    """
    widget = widgets.HiddenInput()


class TextAreaField(TextField):
    """
    This field represents an HTML ``<textarea>`` and can be used to take
    multi-line input.
    """
    widget = widgets.TextArea()


class PasswordField(TextField):
    """
    Represents an ``<input type="password">``.
    """
    widget = widgets.PasswordInput()


class IntegerField(TextField):
    """
    A text field, except all input is coerced to an integer.  Erroneous input
    is ignored and will not be accepted as a value.
    """
    def _value(self):
        if self.raw_data:
            return self.raw_data[0]
        elif self.data is not None:
            return to_unicode(str(self.data))
        return ''

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = int(valuelist[0])
            except ValueError:
                raise ValueError(self.translate('Not a valid integer value'))


class FloatField(TextField):
    """
    A text field, except all input is coerced to an float.  Erroneous input
    is ignored and will not be accepted as a value.
    """
    def _value(self):
        if self.raw_data:
            return self.raw_data[0]
        elif self.data is not None:
            return to_unicode(self.data)
        return ''

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = float(valuelist[0])
            except ValueError:
                raise ValueError(self.translate('Not a valid float value'))


class BooleanField(Field):
    """
    Represents an ``<input type="checkbox">``.
    """
    widget = widgets.CheckboxInput()

    def process_data(self, value):
        self.data = bool(value)

    def process_formdata(self, valuelist):
        # Checkboxes and submit buttons simply do not send a value when
        # unchecked/not pressed. So the actual value="" doesn't matter for
        # purpose of determining .data, only whether one exists or not.
        self.data = bool(valuelist)

    def _value(self):
        if self.raw_data:
            return to_unicode(self.raw_data[0])
        return 'y'


class DateTimeField(Field):
    """
    A text field which stores a `datetime.datetime` matching a format.
    """
    widget = widgets.TextInput()

    def __init__(self, label=None, validators=None, format='%Y-%m-%d %H:%M:%S', **kwargs):
        super(DateTimeField, self).__init__(label, validators, **kwargs)
        self.format = format

    def _value(self):
        if self.raw_data:
            return to_unicode(' '.join(self.raw_data))
        return self.data and self.data.strftime(self.format) or ''

    def process_formdata(self, valuelist):
        if valuelist:
            date_str = to_unicode(' '.join(valuelist))
            try:
                timetuple = time.strptime(date_str, self.format)
                self.data = datetime.datetime(*timetuple[:6])
            except ValueError:
                self.data = None
                raise ValueError(self.translate('Not a valid datetime value'))


class DateField(DateTimeField):
    """
    Same as DateTimeField, except stores a `datetime.date`.
    """
    def __init__(self, label=None, validators=None, format='%Y-%m-%d', **kwargs):
        super(DateField, self).__init__(label, validators, format, **kwargs)

    def process_formdata(self, valuelist):
        if valuelist:
            date_str = to_unicode(' '.join(valuelist))
            try:
                timetuple = time.strptime(date_str, self.format)
                self.data = datetime.date(*timetuple[:3])
            except ValueError:
                self.data = None
                raise ValueError(self.translate('Not a valid date value'))


class SelectFieldBase(Field):
    option_widget = widgets.Option()

    """
    Base class for fields which can be iterated to produce options.

    This isn't a field, but an abstract base class for fields which want to
    provide this functionality.
    """
    def __init__(self, label=None, validators=None, option_widget=None, **kwargs):
        super(SelectFieldBase, self).__init__(label, validators, **kwargs)

        if option_widget is not None:
            self.option_widget = option_widget

    def iter_choices(self):
        """
        Provides data for choice widget rendering. Must return a sequence or
        iterable of (value, label, selected) tuples.
        """
        raise NotImplementedError()

    def __iter__(self):
        opts = dict(widget=self.option_widget, _name=self.name, _form=None)
        for i, (value, label, checked) in enumerate(self.iter_choices()):
            opt = self._Option(label=label, id='%s-%d' % (self.id, i), **opts)
            opt.process(None, value)
            opt.checked = checked
            yield opt

    class _Option(Field):
        checked = False

        def _value(self):
            return self.data


class SelectField(SelectFieldBase):
    widget = widgets.Select()

    def __init__(self, label=None, validators=None, coerce=to_unicode, choices=None, **kwargs):
        super(SelectField, self).__init__(label, validators, **kwargs)
        self.coerce = coerce
        self.choices = choices

    def iter_choices(self):
        for value, label in self.choices:
            label = self.translate(label)
            yield (value, label, self.coerce(value) == self.data)

    def process_data(self, value):
        try:
            self.data = self.coerce(value)
        except (ValueError, TypeError):
            self.data = None

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = self.coerce(valuelist[0])
            except ValueError:
                raise ValueError(self.translate('Invalid Choice: could not coerce'))

    def pre_validate(self, form):
        for v, _ in self.choices:
            if self.data == v:
                break
        else:
            raise ValueError(self.translate('Not a valid choice'))


class SelectMultipleField(SelectField):
    """
    No different from a normal select field, except this one can take (and
    validate) multiple choices.  You'll need to specify the HTML `rows`
    attribute to the select field when rendering.
    """
    widget = widgets.Select(multiple=True)

    def iter_choices(self):
        for value, label in self.choices:
            selected = self.data is not None and self.coerce(value) in self.data
            yield (value, label, selected)

    def process_data(self, value):
        try:
            self.data = list(self.coerce(v) for v in value)
        except (ValueError, TypeError):
            self.data = None

    def process_formdata(self, valuelist):
        try:
            self.data = list(self.coerce(x) for x in valuelist)
        except ValueError:
            raise ValueError(self.translate('Invalid choice(s): one or more data inputs could not be coerced'))

    def pre_validate(self, form):
        if self.data:
            values = list(c[0] for c in self.choices)
            for d in self.data:
                if d not in values:
                    raise ValueError(self.translate("'%(value)s' is not a valid choice for this field") % dict(value=d))
