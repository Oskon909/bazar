import datetime

import redis
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializer import *

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip

def get_post_number(client, number, pk):
    data = redis.Redis()
    data_value = data.get(str(client))
    client = str(client)
    print(number)

    if data_value is None or data_value.decode('utf-8') != number[0]['phone_number']:
        data.mset({client: number[0]['phone_number']})

        date = datetime.datetime.now(tz=None)
        today = date.date()




        post_object = Post.objects.get(pk=pk)
        number = PhoneNumber.objects.get(post_number=post_object)
        viewscontact_object = ViewsContact.objects.filter(phone=number).filter(date=today).exists()
        print('ooooooooooooooooooo')
        if viewscontact_object ==False:
            object_view=Views.objects.get(post=post_object)
            ViewsContact.objects.create(phone=number,date=today,view_key=object_view)


        name = ViewsContact.objects.filter(phone=number).filter(date=today).values('pk')
        name = ViewsContact.objects.get(pk=name[0]['pk'])
        name.date = today
        name.save(update_fields=["date"])
        name.views += 1
        name.save(update_fields=["views"])

        return False
    else:
        return True



class Contacts_1(APIView):
    def get(self, request, pk):


        post_object = Post.objects.get(pk=pk)
        number = PhoneNumber.objects.get(post_number=post_object)

        print(number,"<<<<<<<<<<<<<<<<<www")

        value_number = PhoneNumber.objects.filter(post_number=post_object).values('phone_number')
        ip = get_client_ip(request)
        print('<<<<<<<<<<<<<<<<')
        if request.user.is_authenticated:
            if not get_post_number(request.user, value_number, pk):
                number.view += 1
                number.save(update_fields=["view"])
        else:
            if not get_post_number(ip, value_number, pk):
                number.view += 1
                number.save(update_fields=["view"])
        print('-------------------------')

        post_object=Post.objects.get(pk=pk)
        object=PhoneNumber.objects.get(post_number=post_object)
        queryset = object
        serializer = ContactSerializer(queryset, many=False).data

        return Response(serializer)

