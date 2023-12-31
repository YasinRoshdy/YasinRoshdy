from itertools import filterfalse

from django.apps import apps
from django.contrib import admin
from django.http import HttpResponse


class DynamicModelAdminMixin:
    dynamic_fields = ()

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        self.dynamic_select_fields = filter(
            self._is_related_field, self.dynamic_fields)
        self.dynamic_input_fields = filterfalse(
            self._is_related_field, self.dynamic_fields)
        return form

    def _is_related_field(self, field_name):
        # return self.opts.get_field(field_name).is_relation
        return True

    @staticmethod
    def render_field(request, app_label, model_name, field_name):
        model = apps.get_model(app_label, model_name)

        # instantiate model form from request data and get field
        model_admin = admin.site._registry[model]
        model_form = model_admin.get_form(request)
        bound_form = model_form(request.POST)

        bound_field = bound_form[field_name]

        # save custom queryset in field
        method_name = f"get_dynamic_{field_name}_field"
        if hasattr(model_admin, method_name):
            method = getattr(model_admin, method_name)
            bound_form.full_clean()
            queryset, value = method(bound_form.cleaned_data)
            bound_field.field.queryset = queryset

            bound_field.form.data = bound_field.form.data.copy()
            bound_field.form.data[field_name] = value

        html = bound_field.as_widget()
        return HttpResponse(html, status=200)

    class Media:
        js = ('https://unpkg.com/htmx.org@1.5.0',)
