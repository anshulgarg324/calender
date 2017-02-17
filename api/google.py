"""
This module handles the Google Signup for a new user

"""
from oauth2client import client
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework.authtoken.models import Token

from models import GoogleData

import httplib2
import json

flow = client.flow_from_clientsecrets(
        './client_secrets.json',
        scope='https://www.googleapis.com/auth/drive.metadata.readonly https://www.googleapis.com/auth/calendar https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile',
        redirect_uri='http://localhost:8000/oauth2callback'
        )
flow.params['access_type'] = 'offline'
flow.params['prompt'] = 'consent'

@api_view(['GET'])
def google_signup(request):
    """
    This method redirects the user to the different url which provides
	the code

    """
    auth_uri = flow.step1_get_authorize_url()
    return redirect(auth_uri)

@api_view(['GET'])
def callback(request):
    """
    This method sign up the user to the calender app and redirect to
    the main page

    """
    code = request.GET['code']
    credentials = flow.step2_exchange(code)
    http_auth = credentials.authorize(httplib2.Http())
    user_dictionary = json.loads(credentials.to_json())
    try:
        email = str(user_dictionary['id_token']['email'])
        username = User.objects.get(username=email)
    except User.DoesNotExist:
        username = None
    if username is None:
        user = User()
        user.username = str(user_dictionary['id_token']['email'])
        user.set_password(str(user_dictionary['refresh_token']))
        user.save()
        new_token = Token.objects.create(user=user)
        new_token.save()
        google_obj = GoogleData()
        google_obj.refresh_token = str(user_dictionary['refresh_token'])
        google_obj.user = user
        google_obj.save()
        return render(request, 'api/index.html',
                    {'key' : str(new_token.key),
                    'msg':"Signup Successful"})
    else:
        old_token = Token.objects.get(user=username)
        return render(request, 'api/index.html',
                    {'msg': 'Email already exists',
                    'key' : str(old_token.key)})
