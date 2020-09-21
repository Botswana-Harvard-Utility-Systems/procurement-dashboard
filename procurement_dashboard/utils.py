from django.conf import settings
from django.contrib.staticfiles import finders
import os
import posixpath
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa


class UnsupportedMediaPathException(Exception):
    pass


def fetch_resources(uri, rel):
    """
    Callback to allow xhtml2pdf/reportlab to retrieve Images,Stylesheets, etc
    @param uri: is the href attribute from the html link element.
    @param rel: gives a relative path, but it's not used here.
    """

    if uri.startswith("http://") or uri.startswith("https://"):
        return uri

    if settings.DEBUG:
        newpath = uri.replace(settings.STATIC_URL, "").replace(settings.MEDIA_URL, "")
        normalized_path = posixpath.normpath(newpath).lstrip('/')
        absolute_path = finders.find(normalized_path)
        if absolute_path:
            return absolute_path

    if settings.MEDIA_URL and uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT,
                            uri.replace(settings.MEDIA_URL, ""))
    elif settings.STATIC_URL and uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT,
                            uri.replace(settings.STATIC_URL, ""))
        if not os.path.exists(path):
            for d in settings.STATICFILES_DIRS:
                path = os.path.join(d, uri.replace(settings.STATIC_URL, ""))
                if os.path.exists(path):
                    break
    else:
        raise UnsupportedMediaPathException(
                                'media urls must start with %s or %s' % (
                                settings.MEDIA_URL, settings.STATIC_URL))
    return path


def generate_pdf(
        template_src, file_object=None, context_dict=None, link_callback=fetch_resources):
    """
        Uses the xhtml2pdf library to render a PDF to the passed file_object,
        from the given template name.
        @return: passed-in file object, filled with the actual PDF data.
        In case the passed in file object is none, it will return a BytesIO instance.
    """
    if not file_object:
        file_object = BytesIO()
    if not context_dict:
        context_dict = {}
    template = get_template(template_src)

    html = template.render(context_dict)

    pdf = pisa.pisaDocument(
        BytesIO(html.encode("ISO-8859-1")), file_object, link_callback=link_callback)
    if not pdf.err:
        return HttpResponse(
            file_object.getvalue(), content_type='application/pdf')
    return None
