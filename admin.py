from django.contrib import admin
from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import ugettext as _

from django.contrib.sites.models import Site

from django.shortcuts import render
from django.http import HttpResponseRedirect

from django_bigbluebutton.models import Meeting
from django_bigbluebutton.models import RegisteredUser
from django_bigbluebutton.models import PreRegisteredUser

from django_bigbluebutton.forms import SendMailForm


class MeetingAdmin(admin.ModelAdmin):
    list_display = ['name']
    ordering = ['name']
    actions = ['send_information_mail',
               'send_inscription_mail']

    def send_information_mail(self, request, queryset):
        form = None

        if 'send_mail' in request.POST:
            form = SendMailForm(request.POST)

            if form.is_valid():
                mail_content = form.cleaned_data['mail_content']

                for meeting in queryset.filter():
                    users = RegisteredUser.objects.filter(meetings=meeting)

                    mails = []

                    for user in users:
                        mails.append(user.mail)

                    subject = _("Informations for the meeting : {}".format(meeting.name))

                    send_mail(subject, content, settings.EMAIL_HOST_USER,
                              mails, fail_silently=False)

                    self.message_user(request, _("The confirmation mail was sent."))
                    return HttpResponseRedirect(request.get_full_path())

        for meeting in queryset.filter():
            content = _("The meeting will begin the {} GMT+1 (Paris time).\n\n"
                        "To join the meeting, follow this link : "
                        "http://{}/{}/{}/{}\n\n"
                        "You can join the meeting using this password : {}"
                        .format(meeting.date, Site.objects.get_current().domain,
                                settings.DJANGO_BBB_BASE_URL, meeting.unique_id,
                                settings.DJANGO_BBB_CONNECTION_URL,
                                meeting.attendee_pw))
            break

        if not form:
            form = SendMailForm(initial={'mail_content': content,
                                         '_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

        return render(request, 'admin/send_mail.html', {'meetings': queryset, 'mail_form': form,
                                                        'action': 'send_information_mail'})

    send_information_mail.short_description = _(
        'Send a mail to selected meeting registered users.'
    )

    def send_inscription_mail(self, request, queryset):
        form = None

        if 'send_mail' in request.POST:
            form = SendMailForm(request.POST)

            if form.is_valid():
                mail_content = form.cleaned_data['mail_content']

                for meeting in queryset.filter():
                    users = PreRegisteredUser.objects.filter(meetings=meeting)

                    mails = []

                    for user in users:
                        mails.append(user.mail)

                    subject = _("Subscription link to the meeting : {}".format(meeting.name))

                    send_mail(subject, mail_content, settings.EMAIL_HOST_USER,
                              mails, fail_silently=False)

                    self.message_user(request, _("The pre-registering mail was sent."))
                    return HttpResponseRedirect(request.get_full_path())

        for meeting in queryset.filter():
            content = _("Hello,\n"
                        "We send you an email because we think you can be interested "
                        "in this meeting which will be the {}. GMT+1 (Paris time)\n"
                        "If you want to subscribe, follow this link :\n"
                        "http://{}/{}/{}/{}\n"
                        .format(meeting.date, Site.objects.get_current().domain,
                                settings.DJANGO_BBB_BASE_URL, meeting.unique_id,
                                settings.DJANGO_BBB_SUBSCRIPTION_URL))
            break

        if not form:
            form = SendMailForm(initial={'mail_content': content,
                                         '_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

        return render(request, 'admin/send_mail.html', {'meetings': queryset, 'mail_form': form,
                                                       'action': 'send_inscription_mail'})

    send_inscription_mail.short_description = _(
        'Send a mail to selected meeting pre-registered users.'
    )

admin.site.register(Meeting, MeetingAdmin)
admin.site.register(RegisteredUser)
admin.site.register(PreRegisteredUser)
