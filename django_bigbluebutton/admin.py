from django.contrib import admin
from django_bigbluebutton.models import Meeting
from django_bigbluebutton.models import RegisteredUser

admin.site.register(Meeting)
admin.site.register(RegisteredUser)