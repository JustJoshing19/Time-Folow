from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from TimeFollow.models import Post

########### Home page ###########
def index(request):
    if request.method == 'POST':
        username = request.POST['']

    User = get_user_model()
    all_users = User.objects.all()

    return render(request, 'TimeFollow/Home.html', {'title':'Home', 'users': all_users})

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
            messages.info(request, f'Account does not exist. Please sign in.')
    form = AuthenticationForm()
    return render(request, 'TimeFollow/login.html', {'form':form, 'title':'Log in'})

########### Creating and Viewing ###########
def CreatePost(request):
    if request.method == 'POST':
        if request.POST['content'] != '' and len(request.POST['content']) <= 200:
            content = request.POST['content']
            poster = request.user
            
            newPost = Post(user=poster, postContent=content)
            #newPost.save()
            messages.success(request, f'Successfully posted!')
            return redirect('timeline')
        
        elif request.POST['content'] == '':
            messages.warning(request, f'Please enter a message before posting.')
        elif len(request.POST['content']) > 200:
            messages.warning(request, f'Please enter a message that is shorter than 200 characters.')

    return render(request, 'TimeFollow/createPost.html', {'title':'Create Post'})

def ViewTimelineCurrentUser(request):
    return render(request, 'TimeFollow/timeline.html', {'title':'Timeline', 'cUser': request.user})

def ViewTimeline(request, username):    
    return render(request, 'TimeFollow/timeline.html', {'title':'Timeline', 'cUser': username})