from django.shortcuts import render

# Create your views here.


def show_event(request):
    """
    Render the event show page.
    """
    return render(request, "show.html")
