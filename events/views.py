from django.shortcuts import render

# Create your views here.


def home(request):
    """
    Render the event home page.
    """
    return render(request, "home.html")
