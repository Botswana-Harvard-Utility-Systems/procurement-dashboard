import os
from django.apps import apps as django_apps

from ....utils import generate_pdf


class PdfResponseMixin(object, ):
    pdf_name = None
    pdf_template = None
    model = None

    def get_pdf_name(self):
        return self.pdf_name

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
