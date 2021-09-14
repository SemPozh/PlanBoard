from django.shortcuts import render
import os
from django.http import HttpResponse


def index(request):
    return render(request, 'planning/index.html')
