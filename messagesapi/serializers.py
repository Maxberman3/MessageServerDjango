from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.SerializerMethodField(read_only=True)
    receiver_username = serializers.SerializerMethodField(read_only=True)

    def get_sender_username(self, obj):
        return obj.sender.username

    def get_receiver_username(self, obj):
        return obj.receiver.username

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver',
                  'message', 'subject', 'creation_date', 'read', 'sender_username', 'receiver_username']


class UserSerializer(serializers.ModelSerializer):
    sent_messages = MessageSerializer(many=True, read_only=True)
    received_messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password',
                  'sent_messages', 'received_messages')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
