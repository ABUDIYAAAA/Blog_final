from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
# Create your views here.
def home(request):
    return render(request, "blog/post_list.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return render(request, "blog/fail_page.html", {'reason': "Username already exist! Please try some other username."})

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return render(request, "blog/fail_page.html", {'reason': "Email Already Registered!!"})

        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return render(request, "blog/fail_page.html", {'reason': "Username must be under 20 charcters!!"})

        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return render(request, "blog/fail_page.html", {'reason': "Passwords didn't matched!!"})

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return render(request, "blog/fail_page.html", {'reason': 'Username must be Alpha-Numeric!! (must contain atealst 1 letter)'})
        User.objects.create_user(username, email, pass1)

        # myuser.is_active = False
        #myuser.is_active = False

        messages.success(request, "Your Account has been created succesfully!!")
    return render(request, "authentication/signup.html")





def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            # messages.success(request, "Logged In Sucessfully!!")
            return render(request, "blog/post_list.html",{"fname":fname})
        else:
            messages.error(request, "Bad Credentials!!")
            return render(request, "blog/fail_page.html", {'reason': "Bad Credentials!! (Password or username are wrong)"})

    return render(request, "authentication/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return render(request, "authentication/signin.html")
