from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from .models import Room, Topic
from .forms import RoomForm, TopicForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

def login_page(request):

    #standardowe sprawdzenie czy użytkownik podał dane
    if request.method == 'POST':
        #pobieramy login i hasło do zmiennych
        username = request.POST.get('username')
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

    return render(request, 'base/login_registration.html')

def logout_user(request):

    logout(request)
    return redirect('home')


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

    context = {'room': room}
    return render(request, 'base/room.html', context)

def create_room(request):

    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def delete_room(request, pk):

    room = Room.objects.get(id=pk)
    if request.method == 'POST':

        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': room})

def topic_list(request):

    topics = Topic.objects.all()

    content = {'topics': topics}
    return render(request, 'base/topic_list.html', content)

def create_topic(request):
    form = TopicForm()

    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("topic_list")

    context = {'form': form}
    return render(request, 'base/create_topic.html', context)