from django.urls import path, include
from rest_framework import routers

from .views import *

urlpatterns = [

    path("12", CategoryAPIView.as_view()),
    path('13', SubscriptionApi.as_view()),
    path('14', NewAdApiView.as_view()),
    path('15', FilterAPIView.as_view()),
    path('16', ProductList.as_view()),
    path('17', SearchAPIListView.as_view()),
    path('18', PostFilterList.as_view()),
]
