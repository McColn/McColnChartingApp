from django import forms
from .models import *

class ThreadForm(forms.Form):
	username = forms.CharField(label='', max_length=100)

class MessageForm(forms.ModelForm):
	body = forms.CharField(label='', max_length=100)
	image = forms.ImageField(required=False)

	class Meta:
		model = MessageModel
		fields = ['body','image']