from django.core.urlresolvers import reverse
from django.template import Library
from django.template import Node
from django.template import TemplateSyntaxError
from django.template import Variable
from django.template import resolve_variable
from django.utils.translation import ugettext as _

register = Library()

class DummyImageUrlNode(Node):
    def __init__(self, width, height, format, context_var):
        # TODO: support variable names instead of only integers
        self.width = width
        self.height = height
        self.format = format
        self.context_var = context_var

    def render(self, context):
        url = reverse('dummyimage.views.render_image',
                args=(self.width, self.height, self.format))

        if self.context_var:
            # push url to context
            context[self.context_var] = url
            return ''
        else:
            # render url
            return url

def do_get_dummyimage_url(parser, token):
    """
    Returns dummy image URL

    Available formats: gif, jpg, png
    Filename format: {w}x{h}.{format} e.g. 100x100.jpg

    Usage::
        {% get_dummyimage_url [width] [height] [format] as [varname] %}
        {% get_dummyimage_url [width] [height] as [varname] %}
        {% get_dummyimage_url [filename] as [varname] %}

        {% get_dummyimage_url [width] [height] [format] %}
        {% get_dummyimage_url [width] [height] %}
        {% get_dummyimage_url [filename] %}

    Example::
        <img src="{% get_dummyimage_url 320x240.png %}" />
        <img src="{% get_dummyimage_url 320 240 %}" />

        {% get_dummyimage_url 320 240 png as image_url %}
        {% get_dummyimage_url 320 240 as image_url %}
        {% get_dummyimage_url 320x240.gif as image_url %}
    """
    bits = token.contents.split()
    # optional arguments
    format = None
    varname = None

    # tag + 1-5 arguments
    if not 1 < len(bits) <= 6:
        raise TemplateSyntaxError(_("%s tag requires between one and five arguments") % bits[0])

    # tag + 5 arguments
    if len(bits) == 6:
        if not bits[4] == 'as':
            raise TemplateSyntaxError(_("if given, fourth argument to %s tag must be 'as'") % bits[0])

        width = bits[1]
        height = bits[2]
        format = bits[3]
        varname = bits[5]
 
    # tag + 4 arguments
    if len(bits) == 5:
        if not bits[3] == 'as':
            raise TemplateSyntaxError(_("if given, third argument to %s tag must be 'as'") % bits[0])

        width = bits[1]
        height = bits[2]
        varname = bits[4]

    # tag + 3 arguments
    if len(bits) == 4:
        if bits[2] == 'as':
            varname = bits[3]
            try:
                width, remain = bits[1].split('x')
                height, format = remain.split('.')
            except ValueError:
                raise TemplateSyntaxError(_("first argument to %s tag must be in format 'WidthxHeight.format'. e.g. 320x240.png") % bits[0])
        else:
            width = bits[1]
            height = bits[2]
            format = bits[3]

    # tag + 2 arguments
    if len(bits) == 3:
        width = bits[1]
        height = bits[2]

    # tag + 1 argument
    if len(bits) == 2:
        try:
            width, remain = bits[1].split('x')
            height, format = remain.split('.')
        except ValueError:
            raise TemplateSyntaxError(_("first argument to %s tag must be in format 'WidthxHeight.format'. e.g. 320x240.png") % bits[0])

    # validate width and height integers
    try:
        width = int(width)
        height = int(height)
    except ValueError:
        raise TemplateSyntaxError(_("width and height argument to %s tag must be integers") % bits[0])

    # validate format
    if not format:
        format = 'jpg' # default
    elif not format in ('jpg', 'gif', 'png'):
        raise TemplateSyntaxError(_("format argument must be either jpg, png or gif"))

    return DummyImageUrlNode(width, height, format, varname)

register.tag('get_dummyimage_url', do_get_dummyimage_url)


