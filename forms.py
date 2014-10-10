from django import forms
from django.forms import widgets
from django_bigbluebutton.models import Meeting, RegisteredUser


class JoinMeetingForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    password = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


class RegisteredUserForm(forms.ModelForm):
    class Meta:
        model = RegisteredUser
        fields = ['mail', 'last_name', 'first_name', 'company', 'phone_number']
        widgets = {
            'mail': forms.EmailInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SendMailForm(forms.Form):
    mail_content = forms.CharField(widget=forms.Textarea)
