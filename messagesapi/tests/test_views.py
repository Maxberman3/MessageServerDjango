from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .tests_helper import InitDB
from rest_framework.test import APIClient
from ..models import Message


class UserControllerTest(TestCase):
    def test_create_user_adds_user(self):
        intialCount = User.objects.all().count()
        response = self.client.post(
            reverse('registration'), {'username': 'FrankReynolds', 'password': 'rumHam'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('FrankReynolds', response.content.decode())
        postCount = User.objects.all().count()
        self.assertEqual(postCount, intialCount + 1)


class UserMessagesTest(TestCase):
    def setUp(self):
        InitDB()

    def test_get_specific_user_messages_all(self):
        frank = User.objects.get(username='FrankReynolds')
        response = self.client.get(
            reverse('specific_users_messages', args=[frank.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('throw me in the trash', response.json()[0]['message'])
        frankMessages = frank.sent_messages.all() | frank.received_messages.all()
        self.assertEqual(len(response.json()), frankMessages.count())

    def test_get_specific_user_messages_only_unread(self):
        frank = User.objects.get(username='FrankReynolds')
        response = self.client.get(
            reverse('specific_users_messages', args=[frank.pk]), {'unread': True})
        self.assertEqual(response.status_code, 200)
        content = response.json()
        frankMessages = frank.sent_messages.all() | frank.received_messages.all()
        self.assertNotIn('spaghetti', str(content))
        self.assertEqual(
            len(content), frankMessages.filter(read=False).count())


class MessagesListTest(TestCase):
    def setUp(self):
        InitDB()

    def test_all_user_messages_authenticated(self):
        frank = User.objects.get(username='FrankReynolds')
        response = self.client.post(
            reverse('token'), {'username': 'FrankReynolds', 'password': 'rumHam'})
        token = response.json()['token']
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
        response = client.get(reverse('messages'))
        frankMessages = frank.sent_messages.all() | frank.received_messages.all()
        self.assertEqual(len(response.json()), frankMessages.count())


class MessageDetailTest(TestCase):
    def setUp(self):
        InitDB()

    def test_returning_a_specific_message_by_id(self):
        message = Message.objects.get(pk=1)
        response = self.client.get(
            reverse('specific_message', args=[message.pk]))
        self.assertEqual(response.status_code, 200)
        content = response.json()
        self.assertEqual(content['message'], message.message)

    def test_sender_or_receiver_can_delete_by_id(self):
        frank = User.objects.get(username='FrankReynolds')
        response = self.client.post(
            reverse('token'), {'username': 'FrankReynolds', 'password': 'rumHam'})
        token = response.json()['token']
        frankMessage = frank.sent_messages.all()[0]
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
        response = client.delete(
            reverse('specific_message', args=[frankMessage.pk]))
        self.assertEqual(response.status_code, 204)
        messageLookup = Message.objects.filter(pk=frankMessage.pk)
        self.assertEqual(len(messageLookup), 0)

    def test_not_sender_or_receiver_cant_delete(self):
        dee = User.objects.get(username='sweetDee')
        response = self.client.post(
            reverse('token'), {'username': 'sweetDee', 'password': 'notABird'})
        token = response.json()['token']
        notDeeMessages = Message.objects.exclude(
            sender=dee.pk) & Message.objects.exclude(receiver=dee.pk)
        notDeeMessage = notDeeMessages.all()[0]
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))
        response = client.delete(
            reverse('specific_message', args=[notDeeMessage.pk]))
        self.assertEqual(response.status_code, 403)
