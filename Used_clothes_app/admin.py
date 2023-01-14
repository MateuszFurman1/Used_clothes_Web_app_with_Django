from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from Used_clothes_app.models import User, Category, Institution, Donation

# admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Institution)
admin.site.register(Donation)
