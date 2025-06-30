from django.shortcuts import render

# Create your views here.


def home(request):
    current_path = request.path
    navbar = [
        {"name": "Home", "url": "/", "active": current_path == "/"},
        {"name": "About", "url": "/about/", "active": current_path == "/about/"},
        {"name": "Events", "url": "/events/", "active": current_path == "/events/"},
        {"name": "Contact", "url": "/contact/", "active": current_path == "/contact/"},
        {
            "name": "Dashboard",
            "url": "/dashboard/",
            "active": current_path == "/dashboard/",
        },
    ]
    return render(request, "home.html", {"navbar": navbar})
