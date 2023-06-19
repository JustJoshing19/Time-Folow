from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm, NewPost, EditProfile
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from TimeFollow.models import Post
from .formErr import RegisterFormErrMessages
currentUser = settings.AUTH_USER_MODEL

########### Home page ###########
def index(request):
    User = get_user_model()
    all_users = User.objects.all()

    return render(request, 'TimeFollow/Home.html', {'title':'Home', 'users': all_users})

def logoutUser(request):
    logout(request)
    messages.success(request, "You have been Logged out.")
    AlertType = 'success'
    request.session['alerttype'] = AlertType
    return redirect('home')

########### Login and Register ###########
def register(request):          # TODO Add saving of first and last names.
    AlertType = ''

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
            AlertType = 'success'
            request.session['alerttype'] = AlertType
            return redirect('login')
        else:
            err = form.errors.as_data()
            errs = RegisterFormErrMessages(err)
            for err in errs:
                messages.warning(request, err)
            AlertType = "danger"
    else:
        form = UserRegistrationForm()
    return render(request, 'TimeFollow/register.html', {'form': form, 'title':'register here', 'alerttype':AlertType})

def Login(request):
    if 'alerttype' in request.session:
        AlertType = request.session['alerttype']
    else:
        AlertType = ''

    form = AuthenticationForm()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password=password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f'welcome {username} !!')
            AlertType = "success"
            request.session['alerttype'] = AlertType
            return redirect('home')
        else:
            messages.warning(request, f'Account does not exist. Please use valid details.')
            AlertType = "danger"
            form = AuthenticationForm(initial={'username':username})
            
    return render(request, 'TimeFollow/login.html', {'form':form, 'title':'Log in', 'alerttype':AlertType})

########### Creating and Viewing ###########
def CreatePost(request):
    if request.method == 'POST':            # To be changed for new model form
        content = request.POST['postContent']
        poster = request.user
        newPost = Post(user=poster, postContent=content)
        newPost.save()
        messages.success(request, 'Succesfully posted!')
        AlertType = "success"
        request.session['alerttype'] = AlertType
        return redirect('timeline')

    form = NewPost()
    return render(request, 'TimeFollow/createPost.html', {'title':'Create Post', 'form': form})

def ViewTimelineCurrentUser(request):
    if 'alerttype' in request.session:
        AlertType = request.session['alerttype']
    else:
        AlertType = ''
    posts = Post.objects.all().filter(user_id = request.user).order_by('-timeStamp')
    hasPost = True
    if not posts:
        hasPost = False
    return render(request, 'TimeFollow/timeline.html', {'title':'Timeline', 'cUser': request.user, 'posts': posts, 'hasPosts': hasPost, 'alerttype':AlertType})

def ViewTimeline(request, username):
    selectedUser = get_user_model().objects.all().filter(username=username)
    posts = Post.objects.all().filter(user_id = selectedUser[0]).order_by('-timeStamp')
    hasPost = True
    if not posts:
        hasPost = False
    return render(request, 'TimeFollow/timeline.html', {'title':'Timeline', 'cUser': username, 'posts':posts, 'hasPosts': hasPost})

########### Editing and Viewing Profile ###########
def viewProfile(request):
    AlertType = ''
    if request.method == 'POST':
        form = EditProfile(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been Updated!')
            AlertType = 'success'
        else:
            err = form.errors.as_data()
            errs = RegisterFormErrMessages(err)
            for err in errs:
                messages.warning(request, err)
            AlertType = "danger"

    form = EditProfile(instance=request.user)
    return render(request, 'TimeFollow/profile.html', {'UserInfoForm': '', 'title': 'Profile', 'form': form, 'alerttype':AlertType})