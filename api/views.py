"""
This module renders the one and only page of the calender application

"""
from django.shortcuts import render

def index(request):
    """
    This method renders the calender html page of the application

    """
    return render(request, 'api/calender.html')
