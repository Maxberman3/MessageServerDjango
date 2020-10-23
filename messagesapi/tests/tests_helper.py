from django.contrib.auth.models import User
from ..models import Message


def InitDB():
    frank = User.objects.create_user(
        username='FrankReynolds', password='rumHam')
    charlie = User.objects.create_user(
        username='charlieDay', password='fightMilk')
    dee = User.objects.create_user(
        username='sweetDee', password="notABird")
    initialMessage1 = Message(sender=frank, receiver=charlie,
                              subject="My last will", message="When I'm dead, throw me in the trash")
    initialMessage2 = Message(sender=charlie, receiver=frank,
                              subject="Spa Policy", message="What's the spaghetti policy here?", read=True)
    initialMessage3 = Message(sender=dee, receiver=charlie, subject="Charlie!",
                              message="If you don't insurance you better have dental, because I'm gonna grind your teeth into dust")
    initialMessage1.save()
    initialMessage2.save()
    initialMessage3.save()
