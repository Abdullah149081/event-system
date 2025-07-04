from django.shortcuts import render
from events.models import Event, Category


def get_navbar(request):
    current_path = request.path
    nav_items = [
        {"name": "Home", "url": "/", "active": False},
        {"name": "About", "url": "/about/", "active": False},
        {"name": "Events", "url": "/events/", "active": False},
        {"name": "Contact", "url": "/contact/", "active": False},
        {"name": "Dashboard", "url": "/dashboard/", "active": False},
    ]
    for item in nav_items:
        if item["url"] == current_path:
            item["active"] = True
            break
    return nav_items


def home(request):
    navbar = get_navbar(request)

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
        "navbar": navbar,
        "events": events,
        "categories": categories,
    }

    return render(request, "home.html", context)
