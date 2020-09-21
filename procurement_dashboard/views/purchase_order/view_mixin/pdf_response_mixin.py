from django.http.response import HttpResponse

from ....utils import generate_pdf


class PdfResponseMixin(object, ):
    pdf_name = None

    def get_pdf_name(self):
        return self.pdf_name

    def render_to_response(self, context, **kwargs):
        context = super().get_context_data(**kwargs)
        template = self.get_template_names()[0]
        resp = HttpResponse(content_type='application/pdf')
        resp['Content-Disposition'] = 'attachment; filename="{0}.pdf"'.format(
            self.get_pdf_name())
        result = generate_pdf(template, file_object=resp, context_dict=context)
        return result
