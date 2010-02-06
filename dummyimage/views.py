from django.http import Http404
from django.http import HttpResponse

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import re
import os

# TODO: move to settings
FONT_FILE = 'DroidSans.ttf'
FONT_PATH = os.path.join(os.path.dirname(__file__), 'fonts', FONT_FILE)

# @@@ settings
AVAILABLE_FORMATS = ('jpg', 'gif', 'png')
DEFAULT_COLORS = {
    'BG': 'white',
    'TEXT': 'grey',
    'BORDER': 'grey',
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
            color = '#%s' % ''.join(c*2 for c in value[1:]).upper()
        else:
            # invalid color
            color = DEFAULT_COLORS[type]
        return color
    else:
        # assume literal color. e.g. white, grey69, etc
        return value if value else DEFAULT_COLORS[type]

def render_image(request, width, height, format):
    # colors
    bgcolor = _get_color(request.GET.get('bgcolor'), 'BG')
    textcolor = _get_color(request.GET.get('textcolor'), 'TEXT')
    bordercolor = _get_color(request.GET.get('bordercolor'), 'BORDER')
    # text rotation
    rotate = request.GET.get('rotate', '0')

    # cast integer values
    try:
        width = int(width)
        height = int(height)
        rotate = int(rotate)
    except ValueError:
        # if any fail reset all
        width = 0
        height = 0
        rotate = 0

    # check restrictions
    if not 0 < width <= 1024 \
        or not 0 < height <= 1024 \
        or not -360 < rotate < 360 \
        or not format in AVAILABLE_FORMATS:
        raise Http404

    # custom text
    text = request.GET.get('text', '%d x %d' % (width, height))

    # mode. Use RGBA if transparent
    mode = 'RGBA' if request.GET.get('transparent') else 'RGB'
    size = (width, height)
    format = 'jpeg' if format == 'jpg' else format

    # allow transparent color
    if 'RGBA' == mode:
        bgcolor = None
    
    # color allows short hex format
    image = Image.new(mode, size, bgcolor) 
    draw = ImageDraw.Draw(image)

    # draw border
    if not request.GET.get('noborder'):
        draw.polygon([(0, 0), (width-1, 0), (width-1, height-1),
                      (0, height-1)], outline=bordercolor)

    # draw cross
    if request.GET.get('cross'):
        draw.line([(0, 0), (width-1, height-1)], fill=bordercolor)
        draw.line([(0, height-1), (width-1, 0)], fill=bordercolor)

    # draw text centered
    if text:
        font_size = width / 10
        font = ImageFont.truetype(FONT_PATH, width / 10)

        center = (width / 2, height / 2)
        text_size = font.getsize(text)
        text_center = (center[0] - text_size[0]/2, center[1] - text_size[1]/2)
        draw.text(text_center, text, font=font, fill=textcolor)

    # write image to response
    response = HttpResponse(mimetype='image/%s' % format)
    #TODO: catch exceptions
    image.save(response, format)

    return response

