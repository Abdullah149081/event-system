from django.shortcuts import render, redirect
from events.models import Event, Category, Participant
from django.utils import timezone
from django.http import HttpResponseNotFound
from events.forms import EventForm, ParticipantForm, CategoryForm


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
    categories = Category.objects.prefetch_related("events").all()
    context = {
        "categories": categories,
    }

    return render(request, "dashboard/CategoryDashboard.html", context)


def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("event")
    else:
        form = EventForm()

    return render(request, "form/EventsForm.html", {"form": form, "is_update": False})


def update_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return HttpResponseNotFound("Event not found")

    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect("event")
    else:
        form = EventForm(instance=event)

    return render(request, "form/EventsForm.html", {"form": form, "is_update": True})


def delete_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return HttpResponseNotFound("Event not found")

    if request.method == "POST":
        event.delete()
        return redirect("event")

    return render(request, "dashboard/EventDashboard.html", {"event": event})


def create_participant(request):
    if request.method == "POST":
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("participant_dashboard")
    else:
        form = ParticipantForm()

    return render(
        request, "form/ParticipantForm.html", {"form": form, "is_update": False}
    )


def update_participant(request, participant_id):
    try:
        participant = Participant.objects.get(id=participant_id)
    except Participant.DoesNotExist:
        return HttpResponseNotFound("Participant not found")

    if request.method == "POST":
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            return redirect("participant_dashboard")
    else:
        form = ParticipantForm(instance=participant)

    return render(
        request, "form/ParticipantForm.html", {"form": form, "is_update": True}
    )


def delete_participant(request, participant_id):
    try:
        participant = Participant.objects.get(id=participant_id)
    except Participant.DoesNotExist:
        return HttpResponseNotFound("Participant not found")

    if request.method == "POST":
        participant.delete()
        return redirect("participant_dashboard")

    return render(
        request, "dashboard/ParticipantDashboard.html", {"participant": participant}
    )


def create_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("category_dashboard")
    else:
        form = CategoryForm()

    return render(request, "form/CategoryForm.html", {"form": form, "is_update": False})


def update_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return HttpResponseNotFound("Category not found")

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("category_dashboard")
    else:
        form = CategoryForm(instance=category)

    return render(request, "form/CategoryForm.html", {"form": form, "is_update": True})


def delete_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return HttpResponseNotFound("Category not found")

    if request.method == "POST":
        category.delete()
        return redirect("category_dashboard")

    return render(request, "dashboard/CategoryDashboard.html", {"category": category})
