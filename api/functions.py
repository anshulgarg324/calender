"""
This module contains all the assissted functions neede to make the apis

"""
from models import GoogleData, Event

import datetime
import requests
import json

EVENT_PROFILE_PARAMS = ['name',
                       'location',
                       'description',
                       'start_date',
                       'end_date',
                       'all_day',
                      ]

DATE_TIME_FORMAT = "%Y-%m-%d"
URL = "https://www.googleapis.com/calendar/v3/calendars/primary/events/"
QUERY_STRING = {"key":"AIzaSyD_NLuaGG4BrX-EGyE94K407pUBAm57x9k"}
ACCESS_URL = "https://www.googleapis.com/oauth2/v4/token"

def convert_date_string_obj(date):
    """
    this function return date object frm a string of date

    """
    date_obj = datetime.datetime.strptime(date, DATE_TIME_FORMAT).date()
    return date_obj

def form_dictionary(event_obj):
    """
    this function forms a dictionary needed to transact data from calender
    to google calender

    """
    convert_start_date = event_obj.start_date
    convert_end_date = event_obj.end_date
    dictionary = {
                    "description": str(event_obj.description),
                    "start": {
                    "date": convert_start_date.strftime(DATE_TIME_FORMAT)
                    },
                    "end": {
                    "date": convert_end_date.strftime(DATE_TIME_FORMAT)
                    },
                    "location": str(event_obj.location)
                }
    return dictionary

def post_or_update_event(event_obj, **kwargs):
    """
    this function post or update event of a dictionary handles both

    """
    event_data = {}
    parameter_dictionary = kwargs['parameter_dict']
    for items in EVENT_PROFILE_PARAMS:
        parameter = parameter_dictionary.get(items, False)
        if parameter:
            event_data[items] = parameter
    for i in event_data:
        if i == 'start_date':
            start_date_object = convert_date_string_obj(event_data[i])
            event_obj.start_date = start_date_object
        elif i == 'end_date':
            end_date_object = convert_date_string_obj(event_data[i])
            event_obj.end_date = end_date_object
        else:
            setattr(event_obj, i, event_data[i])
    event_obj.is_updated = True
    event_obj.save()
    ret = {'msg':True}
    return ret

def post_events(user_obj, **kwargs):
    """
    this function post events on calender app

    """
    event = Event()
    event.user = user_obj
    result = post_or_update_event(event, **kwargs)
    if result['msg']:
        ret = {'success':True, 'msg': 'Event Registered'}
        return ret
    else:
        ret = {'success':False, 'msg': 'Invalid User'}
        return ret

def update_event(user_obj, pk, **kwargs):
    """
    this function update or post the events of a calender

    """
    try:
        event_query = Event.objects.get(pk=pk, user=user_obj, is_active=True)
        if event_query:
            result = post_or_update_event(event_query, **kwargs)
            if result['msg']:
                ret = {'success':True, 'msg':'Successfully Updated'}
                return ret
        else:
            ret = {'success':False, 'msg': 'Invalid Entry'}
            return ret
    except:
        ret = {'success':False, 'msg': 'Invalid Entry'}
        return ret

def delete_event(user_obj, pk):
    """
    this function delete the event from the calender

    """
    try:
        event_query = Event.objects.get(pk=pk, user=user_obj)
        if event_query:
            event_query.is_active = False
            event_query.save()
            ret = {'success':True, 'msg':'Successfully Deleted'}
            return ret
        else:
            ret = {'success':False, 'msg': 'Invalid Entry'}
            return ret
    except:
        ret = {'success':False, 'msg': 'Invalid Entry'}
        return ret

def get_access_token(refresh_token):
    """
    This function return the access token from the refresh token
    and given credentials

    """
    ACCESS_URL_PARAMETERS = {'grant_type':'refresh_token',
                            'refresh_token':refresh_token,
                            'client_id':'275915691673-0sbbt3cn4o49u4bjj3q2dvbgc9edvnqn.apps.googleusercontent.com',
                            'client_secret':'bbiNHqtN4791FtzWAiykYMPN'}
    response = requests.request("POST",
                       ACCESS_URL, params=ACCESS_URL_PARAMETERS)
    the_dict = json.loads(response.text)
    return the_dict['access_token']

def get_sync_event(user_obj):
    """
    this function save the synchronised event from the calender to the
    google calender to oour and vice versa

    """
    google_data_obj = GoogleData.objects.get(user=user_obj)
    if google_data_obj:
        access_token = get_access_token(str(google_data_obj.refresh_token))
        response = sync_from_google(user_obj, access_token)
        result = start_sync(user_obj ,access_token)
        return {'response':response, 'result':result}
    else:
        result = {"success":False, "msg":"Token not valid"}
        return result

def start_sync(user_obj, access_token):
    """
    this function synchronis calender app to the google app

    """
    HEADERS = {
    'authorization': "Bearer" +' '+str(access_token),
    'content-type': "application/json",
    }
    deleted_list = Event.objects.filter(user=user_obj, is_active=False)
    if deleted_list:
        for items in deleted_list:
            if items.google_id:
                event_id = str(items.google_id)
                url_delete = URL + event_id
                r = requests.request("DELETE",
                    url_delete, headers=HEADERS, params=QUERY_STRING)
                if r.status_code == 204:
                    success = True
                else:
                    success = False
            else:
                success = True
        if success:
            Event.objects.filter(user=user_obj, is_active=False).delete()
        else:
            ret = {'success':False, 'msg':'Failure'}
            return ret
    else:
        pass
    updated_or_created_list = Event.objects.filter(user=user_obj,
                                                  is_updated=True)
    if updated_or_created_list:
        for i in updated_or_created_list:
            if i.google_id:
                e_id = str(i.google_id)
                data = form_dictionary(i)
                url_update = URL + e_id
                r = requests.request("PUT",
                                     url_update, data=json.dumps(data),
                                     headers=HEADERS, params=QUERY_STRING)
                if r.status_code == 200:
                    i.is_updated = False
                    i.save()
                else:
                    ret = {'success':False, 'msg':'Failure'}
                    return ret
            else:
                data = form_dictionary(i)
                r = requests.request("POST",
                                    URL, data=json.dumps(data),
                                    headers=HEADERS, params=QUERY_STRING)
                if r.status_code == 200:
                    i.is_updated = False
                    response = r.json()
                    i.google_id = response['id']
                    i.save()
                else:
                    ret = {'success':False, 'msg':'Failure'}
                    return ret
        ret = {'success':True, 'msg':'Synchronised'}
        return ret

    else:
        ret = {'success':True, 'msg':'No objects to delete'}
        return ret

def sync_from_google(user_obj, access_token):
    """
    this function synchronises the google calender to the calender app

    """
    HEADERS = {
    'authorization': "Bearer" +' '+str(access_token),
    'content-type': "application/json",
    }
    google_data_obj = GoogleData.objects.get(user=user_obj)
    updated_min = None
    page_token = None
    while True:
        QUERY_PARAMS = {"key":"AIzaSyD_NLuaGG4BrX-EGyE94K407pUBAm57x9k",
                        "page_token":page_token,
                        "updated_min":updated_min
                        }
        response = requests.request("GET",
            URL, headers=HEADERS, params=QUERY_PARAMS)
        event_dictionary = json.loads(response.text)
        if event_dictionary['items']:
            for event in event_dictionary['items']:
                try:
                    event_obj = Event.objects.get(google_id=str(event['id']), 
                               is_active=True)
                    if event_obj.is_updated == True:
                        continue
                except:
                    event_obj = Event()
                    event_obj.user = user_obj
                try:
                    event_obj.location = event.get('location')
                except:
                    event_obj.location = ''
                try:
                    event_obj.description = event.get('description')
                except:
                    event_obj.description = ''
                try:
                    date = (event['start']['date']).split('T')
                    date_obj = convert_date_string_obj(date[0])
                    event_obj.start_date = date_obj
                    date = (event['end']['date']).split('T')
                    end_date_obj = convert_date_string_obj(date[0])
                    event_obj.end_date = end_date_obj
                except:
                    date = (event['start']['dateTime']).split('T')
                    date_obj = convert_date_string_obj(date[0])
                    event_obj.start_date = date_obj
                    date = (event['end']['dateTime']).split('T')
                    end_date_obj = convert_date_string_obj(date[0])
                    event_obj.end_date = end_date_obj
                event_obj.google_id = event['id']
                event_obj.is_updated = False
                try:
                    event_obj.save()
                except:
                    pass
            page_token = event.get('nextPageToken')
            google_data_obj.last_sync = datetime.datetime.utcnow()
            updated_min = google_data_obj.last_sync.isoformat("T")+"Z"
            google_data_obj.save()
            if page_token:
                pass
            else:
                result = {'success':True}
                return result
        else:
            result = {'success':False}
            return result

def get_events_on_a_date(user_obj, date):
    """
    this function return events on a specified date
    """
    event_date_obj = convert_date_string_obj(date)
    events_list = Event.objects.filter(user=user_obj,
                                       start_date=event_date_obj,
                                       is_active=True)
    event = []
    event_dictionary = {}
    for items in events_list:
        dictionary = {}
        dictionary['description'] = str(items.description)
        dictionary['start_date'] = date
        dictionary['end_date'] = items.end_date.strftime(DATE_TIME_FORMAT)
        dictionary['location'] = str(items.location)
        dictionary['pk'] = str(items.pk)
        event.append(dictionary)
    event_dictionary['events'] = event
    return event_dictionary
