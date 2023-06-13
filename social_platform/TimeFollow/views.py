from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm, NewPost
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from TimeFollow.models import Post

########### Home page ###########
def index(request):
    User = get_user_model()
    all_users = User.objects.all()

    return render(request, 'TimeFollow/Home.html', {'title':'Home', 'users': all_users})

def logoutUser(request):
    logout(request)
    messages.success(request, "You have been Logged out.")
    return redirect('home')

########### Login and Register ###########
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            
            #Mail system
            htmly = get_template('TimeFollow/Email.html')
            d = {'username': username}
            subject, from_email, to = 'Welcome', 'beebob1919@gmail.com', email
            html_conent = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_conent, from_email, [to])
            msg.attach_alternative(html_conent, 'text/html')
            msg.send()
            #Mail system END

            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'TimeFollow/register.html', {'form': form, 'title':'register here'})

def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password=password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f'welcome {username} !!')
            
            return redirect('home')
        else:
            messages.warning(request, f'Account does not exist. Please use valid details.')
    form = AuthenticationForm()
    return render(request, 'TimeFollow/login.html', {'form':form, 'title':'Log in'})

########### Creating and Viewing ###########
def CreatePost(request):
    if request.method == 'POST':            # To be changed for new model form
        content = request.POST['postContent']
        poster = request.user
        newPost = Post(user=poster, postContent=content)
        newPost.save()
        messages.success(request, 'Succesfully posted!')
        return redirect('timeline')

    form = NewPost()
    return render(request, 'TimeFollow/createPost.html', {'title':'Create Post', 'form': form})

def ViewTimelineCurrentUser(request):
    posts = Post.objects.all().filter(user_id = request.user).order_by('-timeStamp')
    hasPost = True
    if not posts:
        hasPost = False
    return render(request, 'TimeFollow/timeline.html', {'title':'Timeline', 'cUser': request.user, 'posts': posts, 'hasPosts': hasPost})

def ViewTimeline(request, username):
    selectedUser = get_user_model().objects.all().filter(username=username).order_by('-timeStamp')
    posts = Post.objects.all().filter(user_id = selectedUser[0])
    hasPost = True
    if not posts:
        hasPost = False
    return render(request, 'TimeFollow/timeline.html', {'title':'Timeline', 'cUser': username, 'posts':posts, 'hasPosts': hasPost})

########### Creating and Viewing ###########

def viewProfile(request):
    if request.method == 'POST':
        pass

    return render(request, 'TimeFollow/profile.html', {'UserInfoForm': '', 'title': 'Profile'})