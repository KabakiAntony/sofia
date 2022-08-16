from django.shortcuts import render


def homepage(request):
    # return HttpResponse('this is the homepage')
    return render(request, "index.html")