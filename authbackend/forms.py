from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.core.mail import send_mail


class OTPAuthenticationForm(AuthenticationForm):
    otp = forms.CharField(required=False, widget=forms.PasswordInput)

    def clean(self):
        # Allow Django to detect can user log in
        super(OTPAuthenticationForm, self).clean()

        # If we got this far, we know that user can log in.
        if self.request.session.has_key('_otp'):
            if self.request.session['_otp'] != self.cleaned_data['otp']:
                raise forms.ValidationError("Invalid OTP.")
            del self.request.session['_otp']
        else:
            # There is no OTP so create one and send it by email
            otp = "1234"
            send_mail(
                subject="Your OTP Password",
                message="Your OTP password is %s" % otp,
                from_email='info@xeoscript.com',
                recipient_list=[self.user_cache.email]
            )
            self.request.session['_otp'] = otp
            # Now we trick form to be invalid
            raise forms.ValidationError("Enter OTP you received via e-mail")




class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        required=True,
        label='Username',
        max_length=32
    )
    email = forms.CharField(
        required=True,
        label='Email',
        max_length=32,
    )
    password = forms.CharField(
        required=True,
        label='Password',
        max_length=32,
        widget=forms.PasswordInput()
    )


# class SignUpForm(UserCreationForm):
#     """ Require email address when a user signs up """
#     email = forms.EmailField(label='Email address', max_length=75)
#
#     class Meta:
#         model = User
#         fields = ('username', 'email',)
#
#     def clean_email(self):
#         email = self.cleaned_data["email"]
#
#         try:
#             user = User.objects.get(email=email)
#             raise forms.ValidationError("This email address already exists. Did you forget your password?")
#         except User.DoesNotExist:
#             return email
#
#     def save(self, commit=True):
#         user = super(UserCreationForm, self).save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         user.email = self.cleaned_data["email"]
#         user.is_active = True  # change to false if using email activation
#         if commit:
#             user.save()
#         return user