from django.contrib import admin

from django.contrib.sessions.models import Session

from .models import *

class SaleAdmin(admin.ModelAdmin):
    list_display = ('title',)

class SliderTopAdmin(admin.ModelAdmin):
    list_display = ('title',)

class SliderTwoAdmin(admin.ModelAdmin):
    list_display = ('title',)

admin.site.register(Sale, SaleAdmin)
admin.site.register(SliderTop, SliderTopAdmin)
admin.site.register(SliderTwo, SliderTwoAdmin)
admin.site.register(Partner)

class SessionAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'session_data', 'expire_date']
admin.site.register(Session, SessionAdmin)