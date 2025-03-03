from django.http import HttpResponse
from django.shortcuts import render


def test(request):
    return render(request, 'accounts/test.html')


def login(request):
    return render(request, 'accounts/login.html')
