from rest_framework import serializers
from .models import Messages


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = ['id', 'title','post_id', 'post_category','post_thumbnail','post','no_likes','post_date', 'post_category','created']

class MassageValidation(serializers.ModelSerializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    class Meta:
        model = Messages
        fields = ['start_date', 'end_date']

class   likeValidation(serializers.ModelSerializer):
    no_likes = serializers.IntegerField()
    class Meta:
        model = Messages
        fields = ['no_likes']