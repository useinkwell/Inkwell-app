from django.contrib import admin
from .models import User, InvalidAccessToken

# Register your models here.
admin.site.register(User)
admin.site.register(InvalidAccessToken)

