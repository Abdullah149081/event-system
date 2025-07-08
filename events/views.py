from django.shortcuts import render
from events.models import Event, Category, Participant
from django.utils import timezone
from django.http import HttpResponseNotFound


def all_events():
    return (
        Event.objects.select_related("category").prefetch_related("participants").all()
    )


def home(request):
    events = all_events()
    query = request.GET.get("query", "").strip()
    category = request.GET.get("category", "").strip()
    start_date = request.GET.get("start_date", "").strip()
    end_date = request.GET.get("end_date", "").strip()

    if category:
        events = events.filter(category__name=category)

    if query:
        events = events.filter(name__icontains=query)

    if start_date and end_date:
        events = events.filter(date__range=[start_date, end_date])
    elif start_date:
        events = events.filter(date__gte=start_date)
    elif end_date:
        events = events.filter(date__lte=end_date)

    categories = Category.objects.all()

    context = {
        "events": events,
        "categories": categories,
    }

    return render(request, "home.html", context)


def event_detail(request, event_id):
    try:
        event = (
            Event.objects.select_related("category")
            .prefetch_related("participants")
            .get(id=event_id)
        )
    except Event.DoesNotExist:
        return HttpResponseNotFound("Event not found")

    context = {
        "event": event,
    }

    return render(request, "event/eventDetails.html", context)


def dashboard(request):
    events = all_events()
    current_date = timezone.now().date()

    context = {
        "events": events,
        "today_events": events.filter(date=current_date),
        "participants_count": Participant.objects.count(),
        "upcoming_events": Event.objects.filter(date__gte=current_date),
        "past_events": Event.objects.filter(date__lt=current_date),
    }

    return render(request, "Dashboard.html", context)


def event(request):
    events = all_events()
    context = {
        "events": events,
    }

    return render(request, "dashboard/EventDashboard.html", context)


def participant_dashboard(request):
    participants = Participant.objects.all()
    context = {
        "participants": participants,
    }

    return render(request, "dashboard/ParticipantDashboard.html", context)


def category_dashboard(request):
    categories = Category.objects.all()
    context = {
        "categories": categories,
    }

    return render(request, "dashboard/CategoryDashboard.html", context)
