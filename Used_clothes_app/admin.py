from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from Used_clothes_app.models import User, Category, Institution, Donation
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


admin.site.register(get_user_model())
admin.site.register(Category)
admin.site.register(Institution)
admin.site.register(Donation)
