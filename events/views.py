from django.contrib import messages
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
        messages.error(request, "Event not found.")
        return redirect("home")

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
            event = form.save()
            messages.success(
                request, f"Event '{event.name}' has been created successfully!"
            )
            return redirect("event")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EventForm()

    return render(request, "form/EventsForm.html", {"form": form, "is_update": False})


def update_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        messages.error(request, "Event not found.")
        return redirect("event")

    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            updated_event = form.save()
            messages.success(
                request, f"Event '{updated_event.name}' has been updated successfully!"
            )
            return redirect("event")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EventForm(instance=event)

    return render(request, "form/EventsForm.html", {"form": form, "is_update": True})


def delete_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        messages.error(request, "Event not found.")
        return redirect("event")

    if request.method == "POST":
        event_name = event.name
        event.delete()
        messages.success(
            request, f"Event '{event_name}' has been deleted successfully!"
        )
        return redirect("event")

    return render(request, "dashboard/EventDashboard.html", {"event": event})


def create_participant(request):
    if request.method == "POST":
        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save()
            messages.success(
                request,
                f"Participant '{participant.name}' has been created successfully!",
            )
            return redirect("participant_dashboard")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ParticipantForm()

    return render(
        request, "form/ParticipantForm.html", {"form": form, "is_update": False}
    )


def update_participant(request, participant_id):
    try:
        participant = Participant.objects.get(id=participant_id)
    except Participant.DoesNotExist:
        messages.error(request, "Participant not found.")
        return redirect("participant_dashboard")

    if request.method == "POST":
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            updated_participant = form.save()
            messages.success(
                request,
                f"Participant '{updated_participant.name}' has been updated successfully!",
            )
            return redirect("participant_dashboard")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ParticipantForm(instance=participant)

    return render(
        request, "form/ParticipantForm.html", {"form": form, "is_update": True}
    )


def delete_participant(request, participant_id):
    try:
        participant = Participant.objects.get(id=participant_id)
    except Participant.DoesNotExist:
        messages.error(request, "Participant not found.")
        return redirect("participant_dashboard")

    if request.method == "POST":
        participant_name = participant.name
        participant.delete()
        messages.success(
            request, f"Participant '{participant_name}' has been deleted successfully!"
        )
        return redirect("participant_dashboard")

    return render(
        request, "dashboard/ParticipantDashboard.html", {"participant": participant}
    )


def create_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(
                request, f"Category '{category.name}' has been created successfully!"
            )
            return redirect("category_dashboard")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CategoryForm()

    return render(request, "form/CategoryForm.html", {"form": form, "is_update": False})


def update_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        messages.error(request, "Category not found.")
        return redirect("category_dashboard")

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            updated_category = form.save()
            messages.success(
                request,
                f"Category '{updated_category.name}' has been updated successfully!",
            )
            return redirect("category_dashboard")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CategoryForm(instance=category)

    return render(request, "form/CategoryForm.html", {"form": form, "is_update": True})


def delete_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        messages.error(request, "Category not found.")
        return redirect("category_dashboard")

    if request.method == "POST":
        category_name = category.name
        category.delete()
        messages.success(
            request, f"Category '{category_name}' has been deleted successfully!"
        )
        return redirect("category_dashboard")

    return render(request, "dashboard/CategoryDashboard.html", {"category": category})
