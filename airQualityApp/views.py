from django.shortcuts import render


def about_view(request):
    context = {
        'title': 'About',
        'content': 'Welcome to the about page.'
    }

    return render(request, 'airQualityApp/about.html', context)
