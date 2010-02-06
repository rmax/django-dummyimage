=================
Django DummyImage
=================

A simple app to generate dummy/filler images on the fly at whatever size you want.

Inspired by http://dummyimage.com/ and http://github.com/xxx/fakeimage

Demo: 

Usage in templates:

    Code:
        <img src="{% get_dummyimage_url 320 240 %}" />
    Output:
        <img src="/dummyimage/320x240.jpg" />


    Example:
        {% get_dummyimage_url 320 240 png as image %}
        <img src="{{ image }}?text=hello+world" />

Optional query parameters:
    bgcolor     - background color*
    textcolor   - text color*
    bordercolor - border color*
    text        - custom image text. default size
    noborder    - no draw border if set
    cross       - draw a cross in the middle of the image 

*Colors can be literal color names (e.g. white, red) or hexadecimal 
 values with !. e.g. !333 instead of #333
 Example colors: !333, !AAA, white, blue, !CBCBCB
