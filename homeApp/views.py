from django.shortcuts import render


# home page view
def homeView(request):
    return render(request, 'homeApp/home.html')
