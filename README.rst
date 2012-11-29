Django DummyImage
=================

A simple app to generate dummy/filler images on the fly at whatever size you want.

Inspired by http://dummyimage.com/ and http://github.com/xxx/fakeimage

Installation
============

Installation using ``pip``::

  $ pip install django-dummyimage

Running tests::

  $ DJANGO_SETTINGS_MODULE=dummyimage.settings python -m dummyimage.tests

Running dummyimage demo::

  $ DJANGO_SETTINGS_MODULE=dummyimage.settings django-admin.py runserver
  $ xdg-open "http://localhost:8000/500x150.png?text=hello+world"


Template Tag
============

Code::

    <img src="{% get_dummyimage_url 320 240 %}" />

Output::

    <img src="/dummyimage/320x240.jpg" />


Example::

    {% get_dummyimage_url 320 240 png as image %}
    <img src="{{ image }}?text=hello+world" />


Query Parameters
================

Available parameters:

  - ``text=string`` text to be rendered in the middle of the image.
  - ``textcolor=color`` text color.
  - ``bgcolor=color`` background color.
  - ``bordercolor=color`` border color.
  - ``noborder=1`` disable border.
  - ``cross=1`` draw a cross in the through the image.

.. note::

  Colors can be literal color names (e.g. ``white``, ``red``) or hexadecimal 
  values starting with ``!``, for example: ``!333``, ``!AAA``, ``white``,
  ``blue``, ``!CBCBCB``.
