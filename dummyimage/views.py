from django.http import Http404
from django.http import HttpResponse

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import os

from .forms import DummyImageForm

# TODO: move to settings
FONT_FILE = 'DroidSans.ttf'
FONT_PATH = os.path.join(os.path.dirname(__file__), 'fonts', FONT_FILE)


def render_image(request, width, height, format):
    data = dict(request.GET.items())
    data.update({
        'width': width,
        'height': height,
        'format': format
    })
    form = DummyImageForm(data=data)

    if not form.is_valid():
        raise Http404
    # custom text
    text = form.cleaned_data['text']

    # mode. Use RGBA if transparent
    mode = 'RGBA' if form.cleaned_data.get('transparent') else 'RGB'
    width = form.cleaned_data['width']
    height = form.cleaned_data['height']
    size = (width, height)

    # allow transparent color
    if 'RGBA' == mode:
        bgcolor = None
    else:
        bgcolor = form.cleaned_data['bgcolor']

    # color allows short hex format
    image = Image.new(mode, size, bgcolor)
    draw = ImageDraw.Draw(image)

    bordercolor = form.cleaned_data['bordercolor']
    # draw border
    if not form.cleaned_data.get('noborder'):
        draw.polygon([(0, 0), (width - 1, 0), (width - 1, height - 1),
                      (0, height - 1)], outline=bordercolor)

    # draw cross
    if form.cleaned_data.get('cross'):
        draw.line([(0, 0), (width - 1, height - 1)], fill=bordercolor)
        draw.line([(0, height - 1), (width - 1, 0)], fill=bordercolor)

    # draw text centered
    if text:
        font = ImageFont.truetype(FONT_PATH, width / 10)

        center = (width / 2, height / 2)
        text_size = font.getsize(text)
        text_center = (center[0] - text_size[0] / 2,
                       center[1] - text_size[1] / 2)
        draw.text(text_center, text, font=font,
                  fill=form.cleaned_data['textcolor'])

    format = form.cleaned_data['format']
    # write image to response
    response = HttpResponse(mimetype='image/%s' % format)
    #TODO: catch exceptions
    image.save(response, format)

    return response
