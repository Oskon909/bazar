from django.urls import path, include
from rest_framework import routers

from .view2 import Contacts_1
from .views import *

router = routers.DefaultRouter()
router.register('', PostAddViewSet, 'Add')

urlpatterns = [
    path('list/', include(router.urls)),
    path('Category', CategoryAPIView.as_view()),
    path('Subscription', SubscriptionApi.as_view()),
    path('New', NewAdApiView.as_view()),
    path('Ordering', FilterAPIView.as_view()),
    path('Filter', Filter.as_view()),
    path('Search', SearchAPIListView.as_view()),
    path('filterCategory', PostFilterList.as_view()),
    path('sub/<int:pk>', SubcategoryAPIView.as_view()),

    # path('view/<int:pk>',ViewNews.as_view()),
    path('view/<int:pk>', DetailPost.as_view()),
    path('listview/<int:pk>', ListViewApi.as_view()),

    path('phine/<int:pk>', Contacts.as_view()),
    path('statistica/<int:pk>',StatistictsApi.as_view()),

    path('post',list.as_view()),
    path('contact/<int:pk>',Contacts_1.as_view()),






]
