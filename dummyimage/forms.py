import re
import sys
from django import forms
from django.conf import settings


MAX_DIMENSION = getattr(settings, 'DUMMYIMAGE_MAX_DIMENSION', sys.maxint)
DEFAULT_BG = getattr(settings, 'DUMMYIMAGE_DEFAULT_BG', 'white')
DEFAULT_TEXT = getattr(settings, 'DUMMYIMAGE_DEFAULT_TEXT', 'grey')
DEFAULT_BORDER = getattr(settings, 'DUMMYIMAGE_DEFAULT_BORDER', 'grey')

DEFAULT_COLORS = {
    'BG': DEFAULT_BG,
    'TEXT': DEFAULT_TEXT,
    'BORDER': DEFAULT_BORDER,
    }

RE_HEX_FULL = re.compile('^[A-F0-9]{6}$', re.IGNORECASE)
RE_HEX_SHORT = re.compile('^[A-F0-9]{3}$', re.IGNORECASE)


def _get_color(value, type):
    """Returns valid color"""
    if value and value.startswith('!'):
        # normalize hex color
        if RE_HEX_FULL.match(value[1:]):
            color = '#%s' % ''.join(value[1:]).upper()
        elif RE_HEX_SHORT.match(value[1:]):
            # duplicate short values
            color = '#%s' % ''.join(c * 2 for c in value[1:]).upper()
        else:
            # invalid color
            color = DEFAULT_COLORS[type]
        return color
    else:
        # assume literal color. e.g. white, grey69, etc
        return value if value else DEFAULT_COLORS[type]


class DummyImageForm(forms.Form):
    bgcolor = forms.CharField(initial=DEFAULT_BG, required=False)
    transparent = forms.BooleanField(initial=False, required=False)

    text = forms.CharField(required=False)
    textcolor = forms.CharField(initial=DEFAULT_TEXT, required=False)

    bordercolor = forms.CharField(initial=DEFAULT_BORDER, required=False)
    noborder = forms.BooleanField(initial=False, required=False)
    cross = forms.BooleanField(initial=False, required=False)

    width = forms.IntegerField(min_value=1, max_value=MAX_DIMENSION)
    height = forms.IntegerField(min_value=1, max_value=MAX_DIMENSION)
    rotate = forms.IntegerField(min_value=-359, max_value=359, initial=0,
                                required=False)

    def clean_bgcolor(self):
        color = self.cleaned_data['bgcolor']
        color = _get_color(color, 'BG')
        return color

    def clean_textcolor(self):
        color = self.cleaned_data['textcolor']
        color = _get_color(color, 'TEXT')
        return color

    def clean_bordercolor(self):
        color = self.cleaned_data['bordercolor']
        color = _get_color(color, 'BORDER')
        return color

    def clean(self):
        cleaned_data = super(DummyImageForm, self).clean()
        text = cleaned_data.get('text')
        width = cleaned_data.get('width')
        height = cleaned_data.get('height')

        if not text and width and height:
            text = '%d x %d' % (width, height)

        return cleaned_data
