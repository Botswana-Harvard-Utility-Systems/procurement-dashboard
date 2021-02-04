import os
import posixpath
from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template.loader import get_template
from django.urls.base import reverse
from io import BytesIO
from procurement.forms import ReportEmailForm

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
            'media urls must start with %s or %s' % (settings.MEDIA_URL, settings.STATIC_URL))
    return path


def generate_pdf(
        template_src, output_filename=None, context_dict=None, link_callback=fetch_resources):
    """
        Uses the xhtml2pdf library to render a PDF to the passed file_object,
        from the given template name.
        @return: passed-in file object, filled with the actual PDF data.
        In case the passed in file object is none, it will return a BytesIO instance.
    """
    # open output file for writing (truncated binary)
    result_file = open(output_filename, "w+b")

    if not context_dict:
        context_dict = {}

    template = get_template(template_src)

    source_html = template.render(context_dict)
    # convert HTML to PDF
    pisa_status = pisa.CreatePDF(
            BytesIO(source_html.encode("ISO-8859-1")),
            dest=result_file,
            link_callback=link_callback)

    # close output file
    result_file.close()

    return pisa_status.err


def email_report(request):
    if request.method == 'POST':
        report_email_form = ReportEmailForm(request.POST)
        if report_email_form.is_valid():
            sender_email = report_email_form.cleaned_data['sender_email']
            recipient_email = report_email_form.cleaned_data['recipient_email']
            subject = report_email_form.cleaned_data['subject']
            message = report_email_form.cleaned_data['message']

            if recipient_email and sender_email:
                send_mail(subject, message, sender_email, [recipient_email, ])
                report_email_form.save()
                order_number = request.POST.get('order_number')
                return redirect(reverse('procurement_dashboard:purchase_order_report_url',
                               kwargs=dict(order_number=order_number)))
