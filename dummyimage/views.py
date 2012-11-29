from django.http import Http404
from django.http import HttpResponse

from .models import DummyImage

AVAILABLE_FORMATS = ('jpeg', 'gif', 'png')


def render_image(request, width, height, format):
    params = dict(request.GET.items())
    image_format = 'jpeg' if format == 'jpg' else format
    try:
        dummyimage = DummyImage.new(width, height, **params)
    except DummyImage.InvalidParams:
        raise Http404

    if image_format not in AVAILABLE_FORMATS:
        raise Http404

    # write image to response
    response = HttpResponse(mimetype='image/%s' % image_format)
    #TODO: catch exceptions
    dummyimage.save(response, image_format)

    return response
