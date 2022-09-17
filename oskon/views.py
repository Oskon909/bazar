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







def get_post(client, title, pk):
    data = redis.Redis()
    data_value = data.get(str(client))
    if data_value is None or data_value.decode('utf-8') != title:
        data.mset({str(client): title})
        date = datetime.datetime.now(tz=None)
        today = date.date()
        # today = datetime.date(year=2022, month=9, day=9)
        post_object = Post.objects.get(title=pk)
        view_object = Views.objects.filter(post=post_object).filter(date=today).exists()

        if view_object == False:
            Views.objects.create(post=post_object, date=today)

        name = Views.objects.filter(post=post_object).filter(date=today).values('pk')
        name = Views.objects.get(pk=name[0]['pk'])
        name.date = today
        name.save(update_fields=["date"])
        name.views += 1
        name.save(update_fields=["views"])

        return False
    else:
        return True


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


class DetailPost(APIView):
    def get(self, request, pk):
        posts = get_object_or_404(Post, title=pk)
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

        post_object = Post.objects.get(title=pk)
        date = datetime.datetime.now(tz=None)
        today = date.date()
        view = Views.objects.filter(post=post_object).filter(date=today).exists()

        if not view:
            Views.objects.create(post=post_object, date=today)

        view = Views.objects.filter(post=post_object).filter(date=today)
        view = view[0]

        serializer_view = ViewSerializer(view, many=False).data
        serializer = AddPostSerializer(posts, many=False).data

        context = {
            'add': serializer,
            'view': serializer_view
        }
        return Response(context)


class ListViewApi(APIView):
    def get(self, request, pk):
        queryset = Views.objects.filter(post=pk)

        serializer = ViewSerializer(queryset, many=True).data
        context = {

            'views': serializer
        }
        return Response(context)


def get_post_number(client, number, pk):
    data = redis.Redis()
    data_value = data.get(str(client))
    client = str(client)

    if data_value is None or data_value.decode('utf-8') != number[0]['phone_number_0']:
        data.mset({client: number[0]['phone_number_0']})

        date = datetime.datetime.now(tz=None)
        today = date.date()
        post_object = Post.objects.filter(pk=pk).values('phone_number')
        phone_object = PhoneNumber.objects.filter(pk=post_object[0]['phone_number']).values('pk')
        view_object = ViewsContact.objects.filter(phone=phone_object[0]['pk']).filter(date=today).exists()

        if view_object == False:
            object_of_phone = PhoneNumber.objects.get(pk=phone_object[0]['pk'])
            post_object = Post.objects.get(pk=pk)
            view = Views.objects.get(post=post_object, date=today)
            ViewsContact.objects.create(phone=object_of_phone, date=today, view_key=view)

        name = ViewsContact.objects.filter(phone=object_of_phone).filter(date=today).values('pk')
        name = ViewsContact.objects.get(pk=name[0]['pk'])
        name.date = today
        name.save(update_fields=["date"])
        name.views += 1
        name.save(update_fields=["views"])
        return False
    else:
        return True


class Contacts(APIView):
    def get(self, request, pk):
        object_of_post = Post.objects.filter(pk=pk).values('phone_number')
        queryset = PhoneNumber.objects.filter(pk=object_of_post[0]['phone_number'])
        number = get_object_or_404(PhoneNumber, pk=object_of_post[0]['phone_number'])
        value_nomber = PhoneNumber.objects.filter(pk=object_of_post[0]['phone_number']).values('phone_number_0')
        ip = get_client_ip(request)

        if request.user.is_authenticated:
            if not get_post_number(request.user, value_nomber, pk):
                number.view += 1
                number.save(update_fields=["view"])
        else:
            if not get_post_number(ip, value_nomber, pk):
                number.view += 1
                number.save(update_fields=["view"])

        queryset = queryset[0]
        serializer = ContactSerializer(queryset, many=False).data

        return Response(serializer)


class StatistictsApi(APIView):
    def get(self, requests, pk):
        post = Post.objects.get(pk=pk)
        serializer_post = StatisticsPostSerilizer(post, many=False).data
        date = datetime.datetime.now(tz=None)
        month = date.month
        yaer = date.year
        today = date.day

        id_post = Post.objects.filter(pk=pk).values('pk')
        view_every_day = Views.objects.filter(post=id_post[0]['pk']).filter(date__year=yaer, date__month=month)
        serializer_view_every_day = StatisticsViewSerializer(view_every_day, many=True).data

        id_phonenumber = Post.objects.filter(pk=pk).values('phone_number')
        number = PhoneNumber.objects.get(pk=id_phonenumber[0]['phone_number'])
        serializer_view_number = StaticsNumberSerializer(number, many=False).data

        view_today_id = Views.objects.filter(post=id_post[0]['pk']).filter(date__year=yaer,
                                                                           date__month=month,
                                                                           date__day=today).values('pk').exists()
        object_post = Post.objects.get(pk=pk)

        if view_today_id == False:
            Views.objects.create(post=object_post, date=date)
            view_today_id = Views.objects.filter(post=object_post).filter(date=date).values('pk')
        else:
            view_today_id = Views.objects.filter(post=object_post).filter(date=date).values('pk')

        view_today = Views.objects.get(pk=view_today_id[0]['pk'])
        serializer_view_today = TodaySerializer(view_today, many=False).data

        context = {
            'common post view': serializer_post,
            'view post today': serializer_view_today,
            'common view number of contacts': serializer_view_number,
            'view post every day': serializer_view_every_day,

        }

        return Response(context)

