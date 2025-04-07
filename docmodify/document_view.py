from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def createLetterhead(request):
    return render(request, 'docmodify/document/create_letterhead.html')