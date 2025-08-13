from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.db.models import Count
from events.models import Event, Category
from events.utils import (
    is_admin,
    is_organizer,
    is_participant,
    get_user_role,
)
from users.signals import send_rsvp_confirmation_email
from django.utils import timezone
from events.forms import EventForm, CategoryForm


def all_events():

    return (
        Event.objects.select_related("category", "created_by")
        .prefetch_related("participants")
        .all()
    )


def get_user_statistics():

    group_stats = Group.objects.annotate(user_count=Count("user")).values(
        "name", "user_count"
    )

    stats = {group["name"]: group["user_count"] for group in group_stats}

    total_users = User.objects.count()

    return {
        "total_users": total_users,
        "admin_count": stats.get("Admin", 0),
        "organizer_count": stats.get("Organizer", 0),
        "participants_count": stats.get("Participant", 0),
    }


@login_required
def rsvp_event(request, event_id):

    event = get_object_or_404(Event, id=event_id)
    user = request.user

    if request.method == "POST":

        if user not in event.participants.all():

            event.participants.add(user)
            send_rsvp_confirmation_email(user, event)
            messages.success(request, f"Successfully RSVP'd to {event.name}!")
        else:
            messages.info(request, f"You have already RSVP'd to {event.name}!")

        return redirect(request.META.get("HTTP_REFERER", "home"))

    return redirect(request.META.get("HTTP_REFERER", "home"))


@login_required
def cancel_rsvp(request, event_id):

    event = get_object_or_404(Event, id=event_id)
    user = request.user

    if request.method == "POST":

        if user in event.participants.all():

            event.participants.remove(user)
            messages.success(request, f"Successfully cancelled RSVP for {event.name}!")
        else:
            messages.info(request, f"You haven't RSVP'd to {event.name}!")

        return redirect(request.META.get("HTTP_REFERER", "home"))

    return redirect(request.META.get("HTTP_REFERER", "home"))


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


@login_required
def dashboard(request):

    user_role = get_user_role(request.user)

    if is_admin(request.user):
        return admin_dashboard(request)
    elif is_organizer(request.user):
        return organizer_dashboard(request)
    elif is_participant(request.user):
        return participant_dashboard(request)
    else:

        return redirect("home")


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):

    events = all_events()
    current_date = timezone.now().date()

    user_stats = get_user_statistics()

    context = {
        "events": events,
        "today_events": events.filter(date=current_date),
        "upcoming_events": Event.objects.filter(date__gte=current_date),
        "past_events": Event.objects.filter(date__lt=current_date),
        "total_events": Event.objects.count(),
        "total_categories": Category.objects.count(),
        "user_role": "Admin",
        **user_stats,
    }

    return render(request, "dashboard/AdminDashboard.html", context)


@login_required
@user_passes_test(is_organizer)
def organizer_dashboard(request):

    events = Event.objects.filter(created_by=request.user).prefetch_related(
        "participants"
    )
    current_date = timezone.now().date()

    total_rsvps = sum(event.participants.count() for event in events)

    user_stats = get_user_statistics()

    context = {
        "events": events,
        "today_events": events.filter(date=current_date),
        "upcoming_events": events.filter(date__gte=current_date),
        "past_events": events.filter(date__lt=current_date),
        "total_rsvps": total_rsvps,
        "my_events_count": events.count(),
        "user_role": "Organizer",
        "participants_count": user_stats["participants_count"],
    }

    return render(request, "dashboard/OrganizerDashboard.html", context)


@login_required
def participant_dashboard(request):

    user_rsvps = Event.objects.filter(participants=request.user).select_related(
        "category"
    )
    current_date = timezone.now().date()

    available_events = (
        Event.objects.filter(date__gte=current_date)
        .exclude(participants=request.user)
        .select_related("category")
    )

    user_stats = get_user_statistics()

    context = {
        "events": user_rsvps,
        "user_rsvps": user_rsvps,
        "today_events": user_rsvps.filter(date=current_date),
        "upcoming_events": user_rsvps.filter(date__gte=current_date),
        "past_events": user_rsvps.filter(date__lt=current_date),
        "available_events": available_events,
        "user_role": "Participant",
        "participants_count": user_stats["participants_count"],
    }

    return render(request, "dashboard/ParticipantDashboard.html", context)


@login_required
def event(request):
    if not (is_admin(request.user) or is_organizer(request.user)):

        context = {
            "error_title": "Access Denied",
            "error_message": "You need Admin or Organizer privileges to access the Event Dashboard.",
            "error_code": "403",
            "user_role": get_user_role(request.user),
            "suggested_action": "contact your administrator to request access",
        }
        return render(request, "error/access_denied.html", context)

    events = all_events()
    context = {
        "events": events,
    }

    return render(request, "dashboard/EventDashboard.html", context)


@login_required
def category_dashboard(request):

    if not (is_admin(request.user) or is_organizer(request.user)):

        context = {
            "error_title": "Access Denied",
            "error_message": "You need Admin or Organizer privileges to access the Category Dashboard.",
            "error_code": "403",
            "user_role": get_user_role(request.user),
            "suggested_action": "contact your administrator to request access",
        }
        return render(request, "error/access_denied.html", context)

    categories = Category.objects.prefetch_related("events").all()
    context = {
        "categories": categories,
    }

    return render(request, "dashboard/CategoryDashboard.html", context)


@login_required
@user_passes_test(lambda u: is_admin(u) or is_organizer(u))
def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            messages.success(
                request, f"Event '{event.name}' has been created successfully!"
            )
            return redirect("event")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EventForm()

    return render(request, "form/EventsForm.html", {"form": form, "is_update": False})


@login_required
@user_passes_test(lambda u: is_admin(u) or is_organizer(u))
def update_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)

        if not is_admin(request.user) and event.created_by != request.user:
            messages.error(request, "You don't have permission to edit this event.")
            return redirect("event")

    except Event.DoesNotExist:
        messages.error(request, "Event not found.")
        return redirect("event")

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
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


@login_required
@user_passes_test(lambda u: is_admin(u) or is_organizer(u))
def delete_event(request, event_id):

    try:
        event = Event.objects.get(id=event_id)

        if not is_admin(request.user) and event.created_by != request.user:
            messages.error(request, "You don't have permission to delete this event.")
            return redirect("event")

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


@login_required
@user_passes_test(lambda u: is_admin(u) or is_organizer(u))
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


@login_required
@user_passes_test(lambda u: is_admin(u) or is_organizer(u))
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


@login_required
@user_passes_test(lambda u: is_admin(u) or is_organizer(u))
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
