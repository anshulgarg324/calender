"""
This module shows all the apis related to the calender

"""
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import authentication, permissions

import functions

class Calender(APIView):
    """
    This class is related to post,update and delete events done by the
    user within the calender

    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        """
        This method helps in posting the events from the calender
        and stored it in the database

        """
        kwargs = {}
        user_obj = request.user
        kwargs['parameter_dict'] = request.data
        result = functions.post_events(user_obj, **kwargs)
        return Response(result)

    def put(self, request, pk):
        """
        This method helps in updating the events from the calender
        and stored it in the database

        """
        user_obj = request.user
        kwargs = {}
        kwargs['parameter_dict'] = request.data
        result = functions.update_event(user_obj, pk, **kwargs)
        return Response(result)

    def delete(self, request, pk):
        """
        This method helps in deleting the events from the calender
        and delete it from the database

        """
        user_obj = request.user
        result = functions.delete_event(user_obj, pk)
        return Response(result)

class SyncEvent(APIView):
    """
        This class helps in synchronising the events from the calender
        and stored it in the database

    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """
        This method helps in getting the events from the google calender
        and stored it in the database as well as from our calender to the
        database

        """
        user_obj = request.user
        result = functions.get_sync_event(user_obj)
        return Response(result)

@api_view(['POST'])
def get_events_on_a_date(request):
    """
        This method helps in getting the events on the basis of datepick
        by the user

    """
    date = request.data.get('date', False)
    user_obj = request.user
    result = functions.get_events_on_a_date(user_obj, date)
    return Response(result)
