from django.shortcuts import render
from events.models import Event, Category, Participant
from django.utils import timezone


def home(request):

    query = request.GET.get("query", "").strip()
    category = request.GET.get("category", "").strip()
    start_date = request.GET.get("start_date", "").strip()
    end_date = request.GET.get("end_date", "").strip()

    events = Event.objects.select_related("category").prefetch_related("participants")

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

    event = (
        Event.objects.select_related("category")
        .prefetch_related("participants")
        .get(id=event_id)
    )

    context = {
        "event": event,
    }

    return render(request, "event/eventDetails.html", context)


def dashboard(request):
    current_date = timezone.now().date()

    events = list(
        Event.objects.select_related("category").prefetch_related("participants")
    )

    context = {
        "events": events,
        "participants_count": Participant.objects.count(),
        "upcoming_events": Event.objects.filter(date__gte=current_date),
        "past_events": Event.objects.filter(date__lt=current_date),
    }

    return render(request, "Dashboard.html", context)


def event(request):
    current_date = timezone.now().date()

    events = list(
        Event.objects.select_related("category").prefetch_related("participants")
    )

    context = {
        "events": events,
        "participants_count": Participant.objects.count(),
        "upcoming_events": Event.objects.filter(date__gte=current_date),
        "past_events": Event.objects.filter(date__lt=current_date),
    }

    return render(request, "dashboard/EventDashboard.html", context)
