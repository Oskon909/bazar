from django.shortcuts import render
from rest_framework import generics, viewsets, status, filters as f
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


class ProductList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = SearchSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter


