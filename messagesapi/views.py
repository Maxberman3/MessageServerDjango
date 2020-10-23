from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, MessageSerializer
from .view_utils import checkAndReturn, findByPk
from .models import Message
from django.contrib.auth.models import User
from .permissions import IsOwnerOrCantDelete


class UserController(APIView):
    """View for the creation of Users"""

    def post(self, request, format=None):
        """Post request expects a username and password"""
        serializer = UserSerializer(data=request.data)
        return checkAndReturn(serializer)


class UserMessages(APIView):
    """View for returning messages belonging to a particular user"""

    def get_object(self, pk):
        return findByPk(User, pk)

    def get(self, request, pk, format=None):
        """Get request expects a path id parameter and allows for an optional query parameter to return only unread messages"""
        unread = request.query_params.get('unread', None)
        user = self.get_object(pk)
        all_messages = user.sent_messages.all() | user.received_messages.all()
        if unread is None or unread == 'False':
            serializer = MessageSerializer(all_messages.all(), many=True)
            return Response(serializer.data)
        only_unread = all_messages.filter(read=False)
        serializer = MessageSerializer(only_unread, many=True)
        return Response(serializer.data)


class MessageList(APIView):
    """View to return a list of messages belonging to a logged in user, as well as the sending of messages"""

    def post(self, request, format=None):
        """Post request expects a json body defining sender, receiver, subject, and message"""
        serializer = MessageSerializer(data=request.data)
        return checkAndReturn(serializer)

    def get(self, request, format=None):
        if request.user.is_anonymous:
            return Response({"error": "only a logged in user can get a full list of their messages"}, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        all_messages = user.sent_messages.all() | user.received_messages.all()
        serializer = MessageSerializer(all_messages, many=True)
        return Response(serializer.data)


class MessageDetail(APIView):
    """View for a specific message"""
    permission_classes = [IsOwnerOrCantDelete]

    def get_object(self, pk):
        message = findByPk(Message, pk)
        self.check_object_permissions(self.request, message)
        return message

    def get(self, request, pk, format=None):
        """Get request for details on a particular message, expects a path id parameter"""
        message = self.get_object(pk)
        message.read = True
        message.save()
        serializer = MessageSerializer(message)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        """Delete request can only be performed by the sender or receiver, expects a path id parameter"""
        message = self.get_object(pk)
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
