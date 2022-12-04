from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class ThreadModel(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='+')
	receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name='+')

class MessageModel(models.Model):
	thread = models.ForeignKey('ThreadModel', related_name='+', on_delete=models.CASCADE,blank=True,null=True)
	sender_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='+')
	receiver_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='+')
	body = models.CharField(max_length=1000)
	image = models.ImageField(blank=True,null=True,upload_to="media/uploads/message_photos")
	date = models.DateTimeField(default=timezone.now)
	is_read = models.BooleanField(default=False)