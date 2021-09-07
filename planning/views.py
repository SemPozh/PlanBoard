from django.shortcuts import render
from django.http import HttpResponse


def testview(request):
    return render(request, 'planning/index.html')
