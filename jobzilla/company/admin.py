from django.contrib import admin
from .models import *

# Register your models here.
# Ye admin login may data dekhe.
admin.site.register(User)
admin.site.register(Company)
admin.site.register(jobpost)
admin.site.register(postlike)
admin.site.register(Ruser)
admin.site.register(upost)
