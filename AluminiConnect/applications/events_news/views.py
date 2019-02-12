from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Event, Attendees
from django.db.models import Count
from django.contrib.auth.models import User
from django.utils import timezone
from itertools import chain
# Create your views here.
def events(request):
    now = timezone.now()
    events = Event.objects.filter(start_date__gte=now).order_by('start_date')
    events_completed = Event.objects.filter(end_date__lt=now).order_by('-start_date')
    return render(request, "events_news/index.html", {'events' : list(chain(events, events_completed))})

def event(request, id):
    e = Event.objects.get(event_id = id)
    attending = Attendees.objects.filter(event_id = e)
    check = False
    if request.user.is_authenticated:
        try:
            if Attendees.objects.get(user_id = User.objects.get(username=request.user.username), event_id = e):
                check = True
        except:
            pass
    
    if request.POST.get("submit") == "rsvp":
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/login/?next="+request.path)

        attendee = Attendees()
        attendee.user_id = User.objects.get(username = request.user.username)
        attendee.event_id = Event.objects.get(event_id = id)
        attendee.save()
        check = True
        return HttpResponseRedirect("/events/event/"+id+"/")

    return render(request, "events_news/event.html", {"event" : e, "check":check, "count":attending.count()})
