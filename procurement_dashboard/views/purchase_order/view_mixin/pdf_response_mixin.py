import os
import base64
from io import BytesIO
from django.apps import apps as django_apps
from django.conf import settings
from pdf2image import convert_from_path

from .report_view_mixin import ReportViewMixin
from ....utils import generate_pdf


class PdfResponseMixin(ReportViewMixin):
    pdf_name = None
    pdf_template = None
    model = None

    def get_pdf_name(self):
        return f'{self.kwargs.get("order_number")}'

    def check_upload_dir_exists(self, upload_dir):
        file_path = 'media/%(upload_dir)s' % {'upload_dir': upload_dir}

        if not os.path.exists(file_path):
            os.makedirs(file_path)
        return file_path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        result = self.model_obj(**kwargs)
        model_obj_set = self.model_obj_set(result)
        context.update(
            result=result,
            model_obj_set=model_obj_set, )
        template = self.pdf_template

        upload_to = self.model_cls.file.field.upload_to

        upload_dir = self.check_upload_dir_exists(upload_to)

        output_filename = f'{upload_dir}{self.get_pdf_name()}.pdf'
        pdf = generate_pdf(
            template, output_filename=output_filename, context_dict=context)
        if not pdf:
            model_obj = self.model_obj(**kwargs)
            if model_obj:
                model_obj.file = f'{upload_to}{self.get_pdf_name()}.pdf'
                model_obj.save()
            context.update(file_name=output_filename)
        pdf_images_bytes = self.pdf_images_as_bytes(model_obj)
        context.update(pdf_images_bytes=pdf_images_bytes)
        return context

    @property
    def model_cls(self):
        return django_apps.get_model(self.model)

    def model_obj(self, **kwargs):
        filter_options = self.filter_options(**kwargs)
        try:
            return self.model_cls.objects.get(**filter_options)
        except self.model_cls.DoesNotExist:
            return None

    def model_obj_set(self, model_obj):
        return []

    def filter_options(self, **kwargs):
        return {}

    def pdf_images_as_bytes(self, model_obj):
        base_dir = settings.BASE_DIR
        pdf_path = f'{base_dir}{model_obj.file.url}'
        image_bytes = []
        pdf_images = convert_from_path(pdf_path)
        buffer = BytesIO()
        for pdf_image in pdf_images:
            pdf_image.save(buffer, "PNG")
            img_str = base64.b64encode(buffer.getvalue()).decode('ascii')
            image_bytes.append(img_str)
        return image_bytes
