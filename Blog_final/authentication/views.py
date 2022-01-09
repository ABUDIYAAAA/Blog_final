from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from .forms import UserProfileForm,UserProfileUpdateForm
from django.views.generic import TemplateView, UpdateView, DetailView
from .models import UserProfile
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from blog.models import Post




def home(request):
    return render(request, "blog/post_list.html")



def ProfileView(request):
    model_ = Post
    author = User.objects.get(username=request.user.username)
    posts = Post.objects.filter(author=author)
    return render(request, 'authentication/user_profile.html', {'posts': posts})

# def ProfileView(request):
#         author = User.objects.get(username=request.user.username)
#         posts = Post.objects.filter(title__contains=request.user.username)
#         return render(request, 'authentication/user_profile.html', {'posts': posts})

class ProfileUpdateView(UpdateView):
    model = UserProfile
    template_name = 'authentication/profile_change.html'
    form_class = UserProfileUpdateForm
    success_url = reverse_lazy('post_list')


def signup(request):
    form = UserProfileForm(request.POST)
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        age = request.POST['age']

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
        user = User.objects.create_user(username, email, pass1)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()

        return redirect('post_list')
        # myuser.is_active = False
        #myuser.is_active = False

        messages.success(request, "Your Account has been created succesfully!!")
    return render(request, "authentication/signup.html", {'form': form})





def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            # messages.success(request, "Logged In Sucessfully!!")
            return redirect('post_list')
        else:
            messages.error(request, "Bad Credentials!!")
            return render(request, "blog/fail_page.html", {'reason': "Bad Credentials!! (Password or username are wrong)"})

    return render(request, "authentication/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('post_list')

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('post_list')
