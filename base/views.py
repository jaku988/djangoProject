from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from .models import Room, Topic, Message
from .forms import RoomForm, TopicForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

def login_page(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    #standardowe sprawdzenie czy użytkownik podał dane
    if request.method == 'POST':
        #pobieramy login i hasło do zmiennych
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        #upewniamy się że użytkownik istnieje w bazie danych
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist!')

        #akceptujemy uzytkownika w sesji
        user = authenticate(request, username=username, password=password)

        #jeżeli dane użytkownika udało się zaakceptować, logujemy go i przechodzimy na stronę główną
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR Password does not exist!')

    context = {'page': page}
    return render(request, 'base/login_registration.html', context)

def logout_user(request):

    logout(request)
    return redirect('home')

def register_user(request):
    page = 'register'

    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration!')


    context = {'page': page,
               'form': form}
    return render(request, 'base/login_registration.html', context)

def home(request):

    #sprawdzamy czy istnieje argument do filtrowania
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    #filtrujemy po argumencie q wyszukując nazwy tematow, pokoi oraz opisow
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    room_count = rooms.count()

    context = {'rooms': rooms,
               'topics': topics,
               'room_count': room_count}

    return render(request, 'base/home.html',  context)

def room(request, pk):

    room = Room.objects.get(id=pk)

    if request.method == 'POST':
        body = request.POST.get("body")
        message = Message.objects.create(body=body, room=room, user=request.user)
        message.save()
        return redirect('room', pk)

    room_messages = room.message_set.all().order_by('created')

    context = {'room': room,
               'room_messages': room_messages}
    return render(request, 'base/room.html', context)


@login_required(login_url="login_page")
def create_room(request):

    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save()
            room.user = request.user
            room.save()

            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.user:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def delete_room(request, pk):

    room = Room.objects.get(id=pk)

    if request.user == room.user:
        if request.method == 'POST':

            room.delete()
            return redirect('home')

    return render(request, 'base/delete.html', {'obj': room})

def topic_list(request):

    topics = Topic.objects.all()

    content = {'topics': topics}
    return render(request, 'base/topic_list.html', content)

@login_required(login_url="login_page")
def create_topic(request):
    form = TopicForm()

    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("topic_list")

    context = {'form': form}
    return render(request, 'base/create_topic.html', context)