from django.contrib import admin
from account.model.index import *

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Member._meta.get_fields()]