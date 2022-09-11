import redis
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from rest_framework import generics, viewsets, status, filters as f
from rest_framework.decorators import api_view

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters
from .models import Category, Subscription
from .serializer import *
from django_filters import rest_framework as filters
import datetime


# Create your views here.
# Просмотр каталога и обьявления

class CategoryAPIView(generics.ListAPIView):
    queryset = Category.objects.all()[0:9]
    serializer_class = CategorySerializer


# def get(self, request, pr):
#        movie = Product.objects.filter(category=pr)
#        serializer = ListProductSerializer
#        return Response(serializer(movie, many=True).data)
#
class SubscriptionApi(APIView):

    def get(self, request):
        x = Subscription.objects.values('post')
        print(x)
        wer = []
        for i in x:
            print(i['post'])

            qq = Post.objects.get(pk=i['post'])
            wer.append(qq)

        movie = Post.objects.all()[0:10]
        print(wer)

        serializer = SubscriptionSerializer
        return Response(serializer(wer, many=True).data)


class NewAdApiView(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-date_created')[0:20]
    serializer_class = NewSerializer


# _________
# Поиск
class SearchAPIListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = SearchSerializer
    filter_backends = [f.SearchFilter]
    search_fields = ['title']


# ---------
# Фильтр по категориям
class Filter(filters.FilterSet):
    class Meta:
        model = Post
        fields = ['category']


class PostFilterList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = SearchSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = Filter


# Фильтры
class FilterAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = SearchSerializer
    filter_backends = [f.OrderingFilter]
    ordering_fields = ['date_created', 'from_price']


class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="from_price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="from_price", lookup_expr='lte')

    class Meta:
        model = Post
        fields = ['category', 'city']


class Filter(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = SearchSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter


# ____________________________

class SubcategoryAPIView(APIView):
    def get(self, request, pk):

        posts = Post.objects.filter(category=pk)
        serializer222 = SearchSerializer(posts, many=True).data

        count = dict()
        for i in Subcategory.objects.values('id', 'title', 'category').filter(category=pk):
            count[i['title']] = Post.objects.filter(subcategory=i['id']).count()
            idcategory = i['category']

        try:
            NameCategory = Category.objects.filter(id=idcategory).values('title')
        except:
            raise Http404

        Name = NameCategory[0]['title']
        context = {
            'Category': Name,
            'Subcategory': count,
            Name: serializer222
        }
        return Response(context)


class PostAddViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = AddPostSerializer


# Просмотр обьвления
# def get_post(client, title):
#
#     data = redis.Redis()
#     print('ppppppppppp')
#     client = str(client)
#     data_value = data.get(client)
#
#     print('kkkkkkk')
#
#
#     if data_value is None or data_value.decode('utf-8') != title:
#         data.mset({client: title})
#         date=datetime.date()
#         post=Post.objects.get(title=title)
#
#         # if Views.objects.get(date=date).filter(post=post)
#         #     Views.objects.create(date=date,post=post)
#
#         Views.views += 1
#         Views.save(update_fields=["views"])
#         return False
#     else:
#         return True
#

def get_post(client, title, pk):
    date = datetime.datetime.now(tz=None)
    today = date.date()

    post_object = Post.objects.get(title=pk)






    try:
        baza = Baza_view.objects.filter(view_key=post_object).values('ip_or_user', 'date')

        print('lop')

    except:

        Baza_view.objects.create(view_key=post_object, ip_or_user=client, date=today)
        # baza = Baza_view.objects.filter(view_key=post_object).values('ip_or_user', 'date')
        Views.objects.create(post=post_object, date=today)

        view_object = Views.objects.get()
        view_object.views += 1
        view_object.save(update_fields=["views"])

        return True
    print('loeree')


    list_user=[]
    list_date=[]
    for i in baza:
        list_user.append(str(i['ip_or_user']))

    print('kzkz')
    for i in baza:
        if str(i['ip_or_user']) == str(client) and i['date'] == today:
            print('они равны')
            print('lllllllllll')
            return False




    if str(client) in list_user:
        name=Baza_view.objects.get(ip_or_user=client)
        name.date=today
        name.save(update_fields=["date"])

        view_object = Views.objects.get()
        view_object.views+=1
        view_object.save(update_fields=["views"])
        print('hello world')

    else:
        print('nnnnnnnnnnnnnnnn')
        Baza_view.objects.create(view_key=post_object ,ip_or_user=client,date=today)

        date_view = Views.objects.filter(post=post_object).filter(date=today).values('date')
        if date_view == today:
            pass
        else:
            Views.objects.create(post=post_object, date=today)

        name = Baza_view.objects.get(ip_or_user=client)
        name.date = today
        name.save(update_fields=["date"])

        view_object = Views.objects.get()
        view_object.views += 1
        view_object.save(update_fields=["views"])



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


class ViewNews(APIView):
    def get(self, request, pk):
        posts = get_object_or_404(Post, title=pk)

        print(request.user.is_authenticated)
        print(request.user)

        title = Post.objects.values('title').filter(title=pk)
        title = title[0]['title']
        ip = get_client_ip(request)
        if request.user.is_authenticated:
            if not get_post(request.user, title, pk):
                posts.views += 1
                posts.save(update_fields=["views"])
        else:
            if not get_post(ip, title, pk):
                posts.views += 1
                posts.save(update_fields=["views"])
        id_post=Post.objects.filter(title=pk).values('id')

        view=Views.objects.get(post=id_post[0]['id'])

        serializer_view=ViewSerializer(view,many=False).data

        serializer = AddPostSerializer(posts, many=False).data
        context = {'IP': ip,
                   'add': serializer,
                   'view':serializer_view
                   }
        return Response(context)
