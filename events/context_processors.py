def navbar_context(request):
    path = request.path

    nav_items = [
        {"name": "Home", "url": "/", "active": False},
        {"name": "About", "url": "/about/", "active": False},
        {"name": "Contact", "url": "/contact/", "active": False},
        {"name": "Dashboard", "url": "/dashboard/", "active": False},
    ]

    if path.startswith("/dashboard"):
        nav_items = [
            {"name": "Home", "url": "/", "active": path == "/"},
            {
                "name": "Dashboard",
                "url": "/dashboard/",
                "active": path == "/dashboard/",
            },
            {
                "name": "Events",
                "url": "events/dashboard/EventDashboard.html",
                "active": path.startswith("/events/"),
            },
            {
                "name": "Participants",
                "url": "events/dashboard/participants.html",
                "active": path.startswith("/participants/"),
            },
            {
                "name": "Categories",
                "url": "events/dashboard/categories.html",
                "active": path.startswith("/categories/"),
            },
        ]
    else:
        for item in nav_items:
            item["active"] = item["url"] == path

    return {"navbar": nav_items}
