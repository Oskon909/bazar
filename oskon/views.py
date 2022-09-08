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
def get_post(ip, title):

    data = redis.Redis()
    data_value = data.get(ip)

    print(data_value.decode('utf-8'),'1111')

    if data_value is None or data_value.decode('utf-8') != title:
        data.mset({ip: title})
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


class ViewNews(APIView):
    def get(self, request, pk):
        posts = get_object_or_404(Post, title=pk)
        serializer = AddPostSerializer(posts, many=False).data

        title = Post.objects.values('title').filter(title=pk)
        title = title[0]['title']
        ip = get_client_ip(request)

        if not get_post(ip, title):
            posts.views += 1
            posts.save(update_fields=["views"])
            serializer = AddPostSerializer(posts, many=False).data
            context = {'IP': ip,
                       'add': serializer}
            return Response(context)

        else:
            return Response(serializer)
