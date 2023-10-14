from django.shortcuts import render, redirect
#from django.http import HttpResponse
from .models import Room, Topic
from .forms import RoomForm, TopicForm

#rooms = [
#    {'id': 1, 'name': 'Lets learn python!'},
#    {'id': 2, 'name': 'Design with me'},
#    {'id': 3, 'name': 'Frondend Dev'},
#]


def home(request):

    q = request.GET.get('q')

    if q == None:
        rooms = Room.objects.all()
    else:
        rooms = Room.objects.filter(topic__name__icontains=q)

    topics = Topic.objects.all()

    context = {'rooms': rooms,
               'topics': topics}

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