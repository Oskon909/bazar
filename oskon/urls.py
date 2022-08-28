from django.urls import path, include
from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register('', PostAddViewSet, 'Add')

urlpatterns = [
    path('Add/', include(router.urls)),
    path('Category', CategoryAPIView.as_view()),
    path('Subscription', SubscriptionApi.as_view()),
    path('New', NewAdApiView.as_view()),
    path('Ordering', FilterAPIView.as_view()),
    path('Filter', Filter.as_view()),
    path('Search', SearchAPIListView.as_view()),
    path('filterCategory', PostFilterList.as_view()),
    path('sub/<int:pk>', SubcategoryAPIView.as_view())
]
