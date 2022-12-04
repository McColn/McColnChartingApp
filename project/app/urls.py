
from django.urls import path
from . import views
from .views import ListThreads,CreateThread,ThreadView,CreateMessage

urlpatterns = [
    path('', views.home, name='home'),
    path('base/', views.base, name='base'),
    path('signup/', views.signup, name='signup'),
    path('inbox', ListThreads.as_view(),name='inbox'),
    path('inbox/create-thread',CreateThread.as_view(), name='create-thread'),

    path('signin/', views.signin,name='signin'),
    path('signup/', views.signup,name='signup'),
    path('signout/', views.signout,name='signout'),

    path('inbox/<int:pk>/', ThreadView.as_view(), name='thread'),
    path('inbox/<int:pk>/create-message/', CreateMessage.as_view(), name='create-messsage'),
   
]