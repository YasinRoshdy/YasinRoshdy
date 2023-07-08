from django.urls import path

from dynamic_select.admin import DynamicModelAdminMixin

urlpatterns = [
    path('<app_label>/<model_name>/<field_name>/',
         DynamicModelAdminMixin.render_field),
]
