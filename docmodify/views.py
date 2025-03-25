from django.shortcuts import render
from django.http import HttpResponse

def hello_there(request):
    return render(request, 'docmodify/letterhead_upload.html')

