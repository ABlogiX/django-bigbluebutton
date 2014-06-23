from django.shortcuts import render, redirect
from django.views.generic import View
from django.conf import settings

from django_bigbluebutton.bbb_api import getMeetings, joinMeetingURL
from django_bigbluebutton.forms import JoinMeetingForm, RegisteredUserForm
from django_bigbluebutton.models import RegisteredUser, Meeting

from django.core.mail import send_mail


class MeetingsView(View):
    template_name = 'django_bigbluebutton/meetings.html'
    secret = settings.BBB_SECRET
    url = settings.BBB_URL

    def get(self, request):
        join_meeting_form = JoinMeetingForm()
        registered_user_form = RegisteredUserForm()

        return_code = 'ERROR'
        is_meetings = False
        meetings = []

        list_meetings = getMeetings(self.url, self.secret)

        if list_meetings is not None:
            return_code = list_meetings['returncode']

            if list_meetings['meetings'] is not None:
                meetings = list(list_meetings['meetings'].values())
                is_meetings = True

        return render(request, self.template_name, locals())

    def post(self, request):
        wrong_password = False
        
        if 'join_meeting' in request.POST:
            join_meeting_form = JoinMeetingForm(request.POST)
            registered_user_form = RegisteredUserForm()

            if join_meeting_form.is_valid() and request.POST['meeting_id']:
                username = join_meeting_form.cleaned_data['username']
                password = join_meeting_form.cleaned_data['password']
                meeting_id = request.POST['meeting_id']
                
                meeting = Meeting.objects.get(unique_id=meeting_id)

                if meeting.attendee_pw == password or meeting.moderator_pw == password:
                    meeting_url = joinMeetingURL(meeting_id, username, password, self.url, self.secret)
                    return redirect(meeting_url)
                
                else:
                    wrong_password = True

        if 'subscribe_meeting' in request.POST:
            registered_user_form = RegisteredUserForm(request.POST)
            join_meeting_form = JoinMeetingForm()
            
            if registered_user_form.is_valid() and request.POST['meeting_id']:
                mail = registered_user_form.cleaned_data['mail']
                last_name = registered_user_form.cleaned_data['last_name']
                first_name = registered_user_form.cleaned_data['first_name']
                company = registered_user_form.cleaned_data['company']
                phone_number = registered_user_form.cleaned_data['phone_number']
                meeting_id = request.POST['meeting_id']

                try:
                    user = RegisteredUser.objects.get(mail=mail)
                    user.meetings.add(Meeting.objects.get(unique_id=int(meeting_id)))

                except RegisteredUser.DoesNotExist:
                    user = RegisteredUser(mail=mail, last_name=last_name, first_name=first_name, company=company, phone_number=phone_number)
                    user.save()
                    user.meetings.add(Meeting.objects.get(unique_id=int(meeting_id)))
                
                subject = 'Inscription à la conférence : ' + Meeting.objects.get(unique_id=int(meeting_id)).name
                content = 'Merci de vous être inscrit à cette conférence. Vous serez informé par mail 24h avant le début de celle-ci.'
                
                send_mail(subject, content, 'alexandre.papin72@gmail.com', [user.mail, ], fail_silently=False)

        return_code = 'ERROR'
        is_meetings = False
        meetings = []

        list_meetings = getMeetings(self.url, self.secret)

        if list_meetings is not None:
            return_code = list_meetings['returncode']

            if list_meetings['meetings'] is not None:
                meetings = list(list_meetings['meetings'].values())
                is_meetings = True

        return render(request, self.template_name, locals())