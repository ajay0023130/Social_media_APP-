from django.contrib import admin

# Register your models here.
from .models import Profile,Contact
admin.site.register(Contact)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']
    raw_id_fields = ['user']