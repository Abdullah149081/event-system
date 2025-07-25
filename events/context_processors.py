def navbar_context(request):
    path = request.path

    nav_items = [
        {"name": "Home", "url": "/"},
        {"name": "About", "url": "/about/"},
        {"name": "Contact", "url": "/contact/"},
        {"name": "Dashboard", "url": "/dashboard/"},
        {"name": "Events", "url": "/events/dashboard/EventDashboard"},
        {"name": "Participants", "url": "/events/dashboard/ParticipantDashboard"},
        {"name": "Categories", "url": "/events/dashboard/CategoryDashboard"},
    ]

    if (
        path.startswith("/dashboard")
        or path.startswith("/events/dashboard/EventDashboard")
        or path.startswith("/events/dashboard/ParticipantDashboard")
        or path.startswith("/events/dashboard/CategoryDashboard")
    ):

        visible_names = {"Home", "Dashboard", "Events", "Participants", "Categories"}
    else:

        visible_names = {"Home", "About", "Contact", "Dashboard"}

    filtered_nav = []
    for item in nav_items:
        if item["name"] in visible_names:

            if item["name"] == "Dashboard":
                active = path.startswith("/dashboard/")
            elif item["name"] == "Events":
                active = path.startswith("/events/dashboard/EventDashboard")
            elif item["name"] == "Participants":
                active = path.startswith("/events/dashboard/ParticipantDashboard")
            elif item["name"] == "Categories":
                active = path.startswith("/events/dashboard/CategoryDashboard")
            else:
                active = item["url"] == path
            filtered_nav.append({**item, "active": active})

    return {"navbar": filtered_nav}
