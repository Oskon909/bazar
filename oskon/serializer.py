from rest_framework import serializers

from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title', 'icon_image')


class Subscription0(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['choice']


class SubscriptionSerializer(serializers.ModelSerializer):
    Subscription = Subscription0(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('title', 'from_price', 'image', 'subcategory', 'Subscription')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'from_price', 'image', 'subscription')


class NewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'from_price', 'image', 'subcategory', 'date_created')

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields =('title','image','from_price','subcategory')