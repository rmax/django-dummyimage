from django.conf.urls.defaults import *

WIDTH_RE = r'(?P<width>\d+)'
HEIGHT_RE = r'(?P<height>\d+)'
FORMAT_RE = r'(?P<format>[a-z]{3})'
IMAGE_RE = r'^%sx%s\.%s$' % (WIDTH_RE, HEIGHT_RE, FORMAT_RE)

urlpatterns = patterns('dummyimage.views',
    url(IMAGE_RE, 'render_image', name='dummyimage_render'),
)
