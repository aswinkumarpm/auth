from django.shortcuts import render

# Create your views here.

from django.template import RequestContext
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
# from authbackend.forms import SignUpForm
from random import choice
from django import forms

from string import ascii_letters


from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from wkhtmltopdf.views import PDFTemplateResponse

from authbackend.forms import UserRegistrationForm



def home(request):
    return render(request, 'home.html')

def index(request):
    return HttpResponse("Congrats, you're now logged in!")


def test(request):
    temp_path = "test.html"

    options = {
        'page-size': 'A4',
    }

    user = request.user


    username = user.username
    email =user.email

    context = {
        "username": username,
        "email": email,

    }

    response = PDFTemplateResponse(
        request=request,
        show_content_in_browser=True,
        template=temp_path,
        # filename='hello.pdf',
        context=context,
        cmd_options=options,
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % "resume2.pdf"
    return response


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            email = userObj['email']
            password = userObj['password']
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
                user = authenticate(username=username, password=password)
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                raise forms.ValidationError('Looks like a username with that email or password already exists')

        else:
            return HttpResponse("Correct Your forms")
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})
