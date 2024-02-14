from django.shortcuts import render
from django.http import HttpResponse


def display_hello(request):
    return HttpResponse("Hello World")


