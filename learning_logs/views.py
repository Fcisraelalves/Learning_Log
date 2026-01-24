from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Create your views here.
def index(request):
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user).all()
    context = {'topics' : topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if topic.owner == request.user:
        entries = topic.entry_set.order_by('-date_added')

        context = {
            'topic' : topic,
            'entries' : entries
        }

        return render(request, 'learning_logs/topic.html', context)
    return render(request, 'learning_logs/HTTP_404.html')

@login_required
def new_topic(request):
    
    if request.method == 'POST':
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('topics'))
    else:
        form = TopicForm()
    
    context = {'form' : form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def delete_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        return render(request, 'learning_logs/HTTP_404.html')
    topic.delete()

    return HttpResponseRedirect(reverse('topics'))

@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        return render(request, 'learning_logs/HTTP_404.html')
    if request.method == 'POST':
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('topic', args=[topic.id]))
    else:
        form = EntryForm()

    context = {'form' : form,
               'topic' : topic}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        return render(request, 'learning_logs/HTTP_404.html')
    if request.method == 'POST':
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topic', args=[topic.id]))
    else:
        form = EntryForm(instance=entry)

    context = {'entry' : entry,
               'form' : form}
    
    return render(request, 'learning_logs/edit_entry.html', context)

@login_required
def delete_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        return render(request, 'learning_logs/HTTP_404.html')
    entry.delete()
    return HttpResponseRedirect(reverse('topic', args=[topic.id]))
