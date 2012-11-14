#!/usr/bin/env python

if __name__ == '__main__':
    import os
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.core.urlresolvers import reverse
from django.template import Context
from django.template import Template

from django.test import Client
from django.test import TestCase

from dummyimage.forms import _get_color


class TemplateTagTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.get_url = lambda w, h, fmt: reverse(
                            'dummyimage.views.render_image',
                            args=(w, h, fmt))

    def get_template(self, arguments):
        return '{%% load dummyimage_tags %%}{%% get_dummyimage_url %s %%}' % arguments

    def test_render_filename(self):
        url = self.get_url(100, 100, 'jpg')
        t = Template(self.get_template('100x100.jpg'))
        c = Context({})
        self.failUnlessEqual(url, t.render(c))

    def test_render_filename_to_context(self):
        url = self.get_url(100, 100, 'jpg')
        t = Template(self.get_template('100x100.jpg as myvar'))
        c = Context({})
        t.render(c)
        self.failUnlessEqual(url, c['myvar'])

    def test_render_width_and_height(self):
        url = self.get_url(100, 100, 'jpg')
        #@@@ default format jpg
        t = Template(self.get_template('100 100'))
        c = Context({})
        self.failUnlessEqual(url, t.render(c))

    def test_render_width_and_height_to_context(self):
        url = self.get_url(100, 100, 'jpg')
        #@@@ default format jpg
        t = Template(self.get_template('100 100 as myvar'))
        c = Context({})
        t.render(c)
        self.failUnlessEqual(url, c['myvar'])

    def test_render_width_height_format(self):
        url = self.get_url(100, 200, 'png')
        #@@@ default format jpg
        t = Template(self.get_template('100 200 png'))
        c = Context({})
        self.failUnlessEqual(url, t.render(c))

    def test_render_width_height_format_to_context(self):
        url = self.get_url(100, 200, 'png')
        #@@@ default format jpg
        t = Template(self.get_template('100 200 png as myvar'))
        c = Context({})
        t.render(c)
        self.failUnlessEqual(url, c['myvar'])


class RenderViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.get_url = lambda w, h, fmt: reverse(
                            'dummyimage.views.render_image',
                            args=(w, h, fmt))

    def test_sizes_boundaries(self):
        # sizes
        response = self.client.get(self.get_url(0, 0, 'jpg'))
        self.failUnlessEqual(response.status_code, 404)

        response = self.client.get(self.get_url(1, 1, 'jpg'))
        self.failUnlessEqual(response.status_code, 200)

        response = self.client.get(self.get_url(1024, 1024, 'jpg'))
        self.failUnlessEqual(response.status_code, 200)

        response = self.client.get(self.get_url(1025, 1025, 'jpg'))
        self.failUnlessEqual(response.status_code, 404)

    def test_valid_formats(self):
        # formats
        response = self.client.get(self.get_url(1, 1, 'jpg'))
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(response['Content-Type'], 'image/jpeg')

        response = self.client.get(self.get_url(1, 1, 'gif'))
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(response['Content-Type'], 'image/gif')

        response = self.client.get(self.get_url(1, 1, 'png'))
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(response['Content-Type'], 'image/png')

    def test_invalid_formats(self):
        response = self.client.get(self.get_url(1, 1, 'avi'))
        self.failUnlessEqual(response.status_code, 404)

        response = self.client.get(self.get_url(1, 1, 'pic'))
        self.failUnlessEqual(response.status_code, 404)

        response = self.client.get(self.get_url(1, 1, 'bmp'))
        self.failUnlessEqual(response.status_code, 404)


    def test_rotation_param(self):
        ## Check Params
        url = self.get_url(1, 1, 'jpg')

        # rotation
        response = self.client.get(url, {'rotate': '-359'})
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get(url, {'rotate': '0'})
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get(url, {'rotate': '359'})
        self.failUnlessEqual(response.status_code, 200)

    def test_invalid_rotation_param(self):
        url = self.get_url(1, 1, 'jpg')
        # invalid
        response = self.client.get(url, {'rotate': 'asdf'})
        self.failUnlessEqual(response.status_code, 404)

        response = self.client.get(url, {'rotate': '-360'})
        self.failUnlessEqual(response.status_code, 404)
        response = self.client.get(url, {'rotate': '360'})
        self.failUnlessEqual(response.status_code, 404)



class GetColorTest(TestCase):
    def test_get_color_util(self):
        """
        Tests return of _get_color function
        """
        #@@@ defaults: bg -> white, text -> black, border -> grey

    def test_default_returns(self):
        # Test defaults
        self.failUnlessEqual('white', _get_color('', 'BG'))
        self.failUnlessEqual('grey', _get_color('', 'TEXT'))
        self.failUnlessEqual('grey', _get_color('', 'BORDER'))

    def test_default_values_if_invalid(self):
        self.failUnlessEqual('white', _get_color('!invalid', 'BG'))
        self.failUnlessEqual('grey', _get_color('!invalid', 'TEXT'))
        self.failUnlessEqual('grey', _get_color('!invalid', 'BORDER'))

    def test_hex_values(self):
        # Test hex values
        self.failUnlessEqual('#000000', _get_color('!000000', 'BG'))
        self.failUnlessEqual('#FFFFFF', _get_color('!ffffff', 'BG'))

    def test_short_hex_values(self):
        # Shorts
        self.failUnlessEqual('#001122', _get_color('!012', 'BG'))
        self.failUnlessEqual('#AABBCC', _get_color('!abc', 'BG'))

    def test_invalid_hex_values(self):
        # invalids
        self.failUnlessEqual('grey', _get_color('!xyz', 'TEXT'))
        self.failUnlessEqual('grey', _get_color('!1234567', 'BORDER'))

    def test_invalid_type(self):
        # Test exceptions
        # invalid type
        self.failUnlessRaises(KeyError, _get_color, '', 'TYPE')
        self.failUnlessRaises(KeyError, _get_color, '!invalid', 'TYPE')


if __name__ == '__main__':
    import os
    from django.core.management.commands.test import Command

    test_argv = [os.sys.argv[0], '', 'dummyimage'] + os.sys.argv[1:]
    test_command = Command()
    test_command.run_from_argv(test_argv)
