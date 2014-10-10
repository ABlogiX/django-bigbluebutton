from django.contrib import admin
from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import ugettext as _

from django_bigbluebutton.models import Meeting
from django_bigbluebutton.models import RegisteredUser
from django_bigbluebutton.models import PreRegisteredUser

from django.contrib.sites.models import Site


class MeetingAdmin(admin.ModelAdmin):
    list_display = ['name']
    ordering = ['name']
    actions = ['send_mail_to_registered_users',
               'send_inscription_mail']

    def send_mail_to_registered_users(self, request, queryset):
        for meeting in queryset.filter():
            users = RegisteredUser.objects.filter(meetings=meeting)

            mails = []

            for user in users:
                mails.append(user.mail)

            subject = _("Informations for the meeting : {}".format(meeting.name))
            content = _("The meeting will begin the meeting.date at meeting.time\n\n"
                        "To join the meeting, follow this link : "
                        "http://{}/{}/{}/{}\n\n"
                        "You can join the meeting using this password : {}"
                        .format(#meeting.date, meeting.time,
                                Site.objects.get_current().domain,
                                settings.DJANGO_BBB_BASE_URL, meeting.unique_id,
                                settings.DJANGO_BBB_CONNECTION_URL,
                                meeting.attendee_pw))

            send_mail(subject, content, settings.EMAIL_HOST_USER,
                      mails, fail_silently=False)

    send_mail_to_registered_users.short_description = _(
        'Send an email to selected meetings registered users.'
    )

    def send_inscription_mail(self, request, queryset):
        for meeting in queryset.filter():
            users = PreRegisteredUser.objects.filter(meetings=meeting)

            mails = []

            for user in users:
                mails.append(user.mail)

            subject = _("Subscription link to the meeting : {}".format(meeting.name))
            content = _("Hello,\n"
                        "We send you an email because we think you can be interested in this meeting.\n"
                        "If you want to subscribe, follow this link :"
                        "http://{}/{}/{}/{}\n"
                        .format(Site.objects.get_current().domain,
                                settings.DJANGO_BBB_BASE_URL, meeting.unique_id,
                                settings.DJANGO_BBB_SUBSCRIPTION_URL))

            send_mail(subject, content, settings.EMAIL_HOST_USER,
                      mails, fail_silently=False)

    send_inscription_mail.short_description = _(
        'Send an email to pre-registered users.'
    )

admin.site.register(Meeting, MeetingAdmin)
admin.site.register(RegisteredUser)
admin.site.register(PreRegisteredUser)
