from pydoc_data.topics import topics
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Message, Room, Topic, User
from .forms import CreateRoomForm, UserUpdateForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def home(request):
    q = ''
    if request.GET.get('q') is not None:
        q = request.GET.get('q')
    
    rooms = Room.objects.filter(Q(topic__topic_name__icontains = q) | Q(room_name__icontains = q) |Q(room_description__icontains = q))
    # print(rooms)

    room_count = rooms.count()
    '''
    topic__topic_name__icontains

    topic(ColumnName Of Room Table) + topic_name(ColumnName Of Topic Table) + icontains

    icontains = i + contains

        --> i Means Case Insensitive

        --> Contains matches every characher of 'q' with topic_name in topic table and filter 
            the Result
    '''

    topics = Topic.objects.all()[0:5]

    '''
    topic.room_set.all.count

    Count Set Of Rooms Which Belongs To Particular Topic
    '''

    # room_messages = Message.objects.all()
    room_messages = Message.objects.filter(Q(room__topic__topic_name__icontains = q))

    contextDict = {'rooms':rooms, 'topics':topics, 'room_count':room_count, 'room_messages':room_messages}
    return render(request, 'baseApp/home.html', contextDict)

def userProfile(request, pk):
    user = User.objects.get(id = pk)
    topics = Topic.objects.all()
    
    rooms = user.room_set.all()
    # Give Us Set of Rooms Which Are Created By Particular User

    room_messages = user.message_set.all()
    # Give Us Set of Messages Which Are Created By Particular User

    contextDict = {'user':user, 'topics':topics, 'rooms':rooms, 'room_messages':room_messages}
    return render(request, 'baseApp/user_profile.html', contextDict)


def room(request, pk):
    loggedIn_user = request.user
    # ['request.user'] is used to get user which are Logged In....
 
    room = Room.objects.get(id = pk)

    room_messages = room.message_set.all()
    # It means ' Give Us The Set Of Messages Which Are Related To This Particular Room'

    participants = room.participants.all()

    if request.method == 'POST':
        msg = Message(user=loggedIn_user, room = room, message_body= request.POST.get('messageBody'))
        msg.save()
        room.participants.add(request.user)
        return redirect('Room_Path', pk = room.id)
    
    selectDict = { 'room' : room, 'room_messages':room_messages, 'participants':participants} 
    return render(request, 'baseApp/room.html', selectDict)

@login_required(login_url='/signIn')
def createRoom(request):
    loggedIn_user = request.user
    # ['request.user'] is used to get user which are Logged In....

    topics = Topic.objects.all()
 
    if request.method == 'POST':
        roomName = request.POST.get('room_name')
        roomDescription = request.POST.get('room_description')
        topicName = request.POST.get('topic_name')

        topic , created_time = Topic.objects.get_or_create(topic_name = topicName)
        '''
        If topic is already exist In Table....then existed Topic Is Assigned in topicGetOrCreate

        Else Topic Is Created And Assigned In topicGetOrCreate
        '''
        Room.objects.create(
            host = loggedIn_user,
            topic = topic,
            room_name = roomName,
            room_description = roomDescription
        )
        return redirect('Home_Path')
    
    contextDict = {'form': CreateRoomForm(), 'topics':topics}
    # form = CreateRoomForm() 
    # It is used to create form
    return render(request, 'baseApp/createRoomForm.html', contextDict)


@login_required(login_url='/signIn')
def updateRoom(request, pk):
    room = Room.objects.get(id = pk)
    formGET = CreateRoomForm(instance = room)

    if request.user != room.host:
        return HttpResponse('You Are Not Allowed To Perform This Task')

    '''
    --> We can not EDIT the Other Host's Room

    --> MihirDavada Can Edit His Own Room......But He Can Not Edit MadhavParmar's Room

    '''

    if request.method == 'POST':
        roomName = request.POST.get('room_name')
        roomDescription = request.POST.get('room_description')
        topicName = request.POST.get('topic_name')

        topic , created_time = Topic.objects.get_or_create(topic_name = topicName)
        '''
        If topic is already exist In Table....then existedTopic Is Assigned in topic

        Else Topic Is Created And Assigned In topic
        '''
        room.room_name = roomName
        room.room_description = roomDescription
        room.topic = topic
        room.save() 
        return redirect('Home_Path')

    contextDict = {'form':formGET, 'room':room}
    return render(request, 'baseApp/createRoomForm.html', contextDict)

@login_required(login_url='/signIn')
def deleteRoom(request, pk):
    room = Room.objects.get(id = pk)

    if request.user != room.host:
        return HttpResponse('You Are Not Allowed To Perform This Task')

    if request.method == 'POST':
        room.delete()
        return redirect('Home_Path')

    contextDict = {'obj':room.room_name}
    return render(request, 'baseApp/deleteForm.html', contextDict)


@login_required(login_url='/signIn')
def deleteMessage(request, pk):
    msg = Message.objects.get(id = pk)

    if request.user != msg.user:
        return HttpResponse('You Are Not Allowed To Perform This Task')

    if request.method == 'POST':
        msg.delete()
        return redirect('Home_Path')
    
    contextDict = {'obj':msg.message_body}
    return render(request, 'baseApp/deleteForm.html', contextDict)

def signIn(request):
    page = 'signIn'

    if request.user.is_authenticated:
        return redirect('Home_Path')

    if request.method == 'POST':
        user_name = request.POST.get('username').lower()
        pass_word = request.POST.get('password')

        user = authenticate(username = user_name, password = pass_word)
        '''
            --> authenticate(username = , password = ) is used to authenticate details which is entered by 
                user in signIn form and signUp form

            --> We authenticate sighIn details with signUp details
        '''
        if user is not None:
            login(request, user)
            '''
            --> With the help of login(request, user), user can login in the page
            '''
            return redirect('Home_Path')
        else:
            messages.error(request, 'User Does Not Exist')

    contextDict = {'page':page}
    return render(request,'baseApp/signInSignUp.html', contextDict)

def signOut(request):
    logout(request)         
    '''
    --> With the help of logout(request), user can logout from the page
    '''
    messages.success(request, 'Logged Out SuccessFuly')
    return redirect('Home_Path')

def signUp(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        # It Is Used To Add Data in Model for which form is created 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower() 
            user.save()
            login(request, user)
            return redirect('Home_Path')
        else:
            messages.error(request, 'An Error Occoured During Registration')

    contextDict = {'form':form}
    return render(request, 'baseApp/signInSignUp.html', contextDict)


@login_required(login_url='/signIn')
def updateUser(request):
    loggedIn_user = request.user
    form = UserUpdateForm(instance=loggedIn_user)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=loggedIn_user)
        # It Is Used To Add Data in Model for which form is created 
        if form.is_valid():
            form.save()
            return redirect('User_Profile_Path', pk=loggedIn_user.id)

    contextDict = {'form':form}
    return render(request, 'updateUser.html',  contextDict)

def topics(request):

    q = ''
    if request.GET.get('q') is not None:
        q = request.GET.get('q')

    topics = Topic.objects.filter(topic_name__icontains=q)

    contextDict = {'topics':topics}

    return render(request, 'baseApp/topics.html', contextDict)

def activities(request):
    room_messages = Message.objects.all()
    contextDict = {'room_messages':room_messages}
    return render(request, 'baseApp/activity.html', contextDict)