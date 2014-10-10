from django.shortcuts import render, redirect
from django.views.generic import View
from django.conf import settings
from django.utils.translation import ugettext as _
from django.core.mail import send_mail

from django_bigbluebutton.bbb_api import getMeetings, joinMeetingURL
from django_bigbluebutton.forms import JoinMeetingForm, RegisteredUserForm
from django_bigbluebutton.models import RegisteredUser, Meeting


class MeetingsView(View):
    template_name = 'django_bigbluebutton/meetings.html'

    def get(self, request):
        join_meeting_form = JoinMeetingForm()
        registered_user_form = RegisteredUserForm()

        return_code = 'ERROR'
        is_meetings = False
        meetings = []

        list_meetings = getMeetings(settings.BBB_URL, settings.BBB_SECRET)

        if list_meetings is not None:
            return_code = list_meetings['returncode']

            if list_meetings['meetings'] is not None:
                meetings = list(list_meetings['meetings'].values())
                is_meetings = True

        return render(request, self.template_name, locals())

    def post(self, request):
        wrong_password = False



        return_code = 'ERROR'
        is_meetings = False
        meetings = []

        list_meetings = getMeetings(settings.BBB_URL, settings.BBB_SECRET)

        if list_meetings is not None:
            return_code = list_meetings['returncode']

            if list_meetings['meetings'] is not None:
                meetings = list(list_meetings['meetings'].values())
                is_meetings = True

        return render(request, self.template_name, locals())


class MeetingSubscriptionView(View):
    template_name = 'django_bigbluebutton/subscription.html'

    def get(self, request, *args):
        # Get the meeting ID in the URL
        meeting_id = args[0]

        registered_user_form = RegisteredUserForm()

        return render(request, self.template_name, locals())

    def post(self, request, *args):
        # Get the meeting ID in the URL
        meeting_id = args[0]

        registered_user_form = RegisteredUserForm(request.POST)

        if registered_user_form.is_valid():
            mail = registered_user_form.cleaned_data['mail']
            last_name = registered_user_form.cleaned_data['last_name']
            first_name = registered_user_form.cleaned_data['first_name']
            company = registered_user_form.cleaned_data['company']
            phone_number = registered_user_form.cleaned_data['phone_number']

            try:
                user = RegisteredUser.objects.get(mail=mail)
                user.meetings.add(
                    Meeting.objects.get(unique_id=int(meeting_id))
                )

            except RegisteredUser.DoesNotExist:
                user = RegisteredUser(mail=mail, last_name=last_name,
                                      first_name=first_name,
                                      company=company,
                                      phone_number=phone_number)
                user.save()
                user.meetings.add(
                    Meeting.objects.get(unique_id=int(meeting_id))
                )

            subject = _("Subscription to the meeting : {}"
                        .format(Meeting.objects.get(unique_id=int(meeting_id)).name))

            content = _("Thank you to subscribed to this meetings.\n"
                        "You will receive a mail one day before the meeting begins.\n\n"
                        "The ABlogiX team.")

            send_mail(subject, content, settings.EMAIL_HOST_USER,
                      [user.mail, ], fail_silently=False)

        return render(request, self.template_name, locals())


class MeetingConnectionView(View):
    template_name = 'django_bigbluebutton/connection.html'

    def get(self, request, *args):
        # Get the meeting ID in the URL
        meeting_id = args[0]

        join_meeting_form = JoinMeetingForm()

        return render(request, self.template_name, locals())

    def post(self, request, *args):
        # Get the meeting ID in the URL
        meeting_id = args[0]

        join_meeting_form = JoinMeetingForm(request.POST)

        if join_meeting_form.is_valid():
            username = join_meeting_form.cleaned_data['username']
            password = join_meeting_form.cleaned_data['password']

            meeting = Meeting.objects.get(unique_id=meeting_id)

            if meeting.attendee_pw == password or meeting.moderator_pw == password:
                meeting_url = joinMeetingURL(meeting_id, username,
                                             password, settings.BBB_URL,
                                             settings.BBB_SECRET)
                return redirect(meeting_url)

            else:
                wrong_password = True

        return render(request, self.template_name, locals())
