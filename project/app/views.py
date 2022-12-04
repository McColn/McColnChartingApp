from django.shortcuts import render,redirect
from .models import *
from django.views import View
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.db.models import Q

# Create your views here.

def home(request):
	return render(request,'app/home.html')

def base(request):
	return render(request,'app/base.html')

def signin(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password1 = request.POST.get('password1')
		user = authenticate(username=username,password=password1)

		if user is not None:
			login(request,user)
			
			return render(request,'app/home.html')

		else:
			messages.error(request,'Bad authenticate')
			return redirect('signin')


	return render(request,'app/signin.html')

def signup(request):
	if request.method == 'POST':
		username=request.POST['username']
		firstname=request.POST['firstname']
		lastname=request.POST['lastname']
		email=request.POST['username']
		password1=request.POST['password1']
		password2=request.POST['password2']

		myuser=User.objects.create_user(username,email,password1)
		myuser.first_name=firstname
		myuser.last_name=lastname
		myuser.save()
		messages.success(request,'You registered successfully')
		return redirect('signin')
	return render(request,'app/signup.html')

def signout(request):
	logout(request)
	messages.success(request,"you logged out successfully")
	return redirect('home')
	return render(request,'app/signout.html')



class ListThreads(View):
	def get(self, request, *args, **kwargs):
		threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user))

		context = {
			'threads':threads
		}
		return render(request, 'app/inbox.html',context)

class CreateThread(View):
	def get(self,request,*args,**kwargs):
		form = ThreadForm()

		context = {
			'form':form
		}
		return render(request, 'app/create_thread.html',context)


	def post(self,request,*args,**kwargs):
		form = ThreadForm(request.POST)

		username = request.POST.get('username')

		try:
			receiver = User.objects.get(username=username)
			if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
				thread = ThreadModel.objects.filter(user=request.user, receiver=receiver)[0]
				return redirect('thread', pk=thread.pk)
			elif ThreadModel.objects.filter(user=receiver, receiver=request.user).exists():
					thread = ThreadModel.objects.filter(user=receiver, receiver=request.user)[0]
					return redirect('thread', pk=thread.pk)

			if form.is_valid():
				thread = ThreadModel(
						user = request.user,
						receiver=receiver
					)
				thread.save()

				return redirect('thread', pk=thread.pk)
		except:
			messages.error(request, 'Invalid username')
			return redirect('create-thread')

class ThreadView(View):
	def get(self, request, pk, *args, **kwargs):
		form = MessageForm()
		thread = ThreadModel.objects.get(pk=pk)
		message_list = MessageModel.objects.filter(thread__pk__contains=pk)
		context = {
			'thread':thread,
			'form':form,
			'message_list':message_list,
		}
		return render(request, 'app/thread.html', context)

class CreateMessage(View):
	def post(self, request, pk, *args, **kwargs):
		#add image
		form = MessageForm(request.POST,request.FILES)
		##############
		thread = ThreadModel.objects.get(pk=pk)

		if thread.receiver == request.user:
			receiver = thread.user
		else:
			receiver = thread.receiver

		# message = MessageModel(
		# 	thread=thread,
		# 	sender_user=request.user,
		# 	receiver_user=receiver,
		# 	body=request.POST.get('message')
		# 	)
		# message.save()


		#add image
		if form.is_valid():
			message = form.save(commit=False)
			message.thread = thread
			message.sender_user = request.user
			message.receiver_user = receiver
			message.save()
		##########################

		return redirect('thread', pk=pk)