from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def index(requeset):
    return HttpResponse("안녕하세요")

