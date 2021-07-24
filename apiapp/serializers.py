from rest_framework import serializers
from home.models import Page


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        fields = ('post_id', 'headline', 'date', 'content', 'category')