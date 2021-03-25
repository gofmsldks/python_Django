"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from pybo import views

app_name = 'pybo'
urlpatterns = [
    path('<int:question_id>/', views.detail, name = 'detail'),
    path('answer/create/<int:question_id>/', views.answer_create, name = 'answer_create'),
    path('question/create/', views.question_create, name = 'question_create'),
    path('', views.index, name='index'),
    path('question/modify/<int:question_id>/', views.question_modify, name = 'question_modify'),
    path('question/delete/<int:question_id>/', views.question_delete, name='question_delete'),
    path('answer/delete/<int:answer_id>/', views.answer_delete, name='answer_delete'),
    path('answer/modify/<int:answer_id>/', views.answer_modify, name='answer_modify'),
    path('comment/create/question/<int:question_id>/', views.comment_create_question, name='comment_create_question'),
    path('comment/modify/question/<int:comment_id>/', views.comment_modify_question, name='comment_modify_question'),
    path('comment/delete/question/<int:comment_id>/', views.comment_delete_question, name='comment_delete_question'),
    path('comment/create/answer/<int:answer_id>/', views.comment_create_answer, name='comment_create_answer'),
    path('comment/modify/answer/<int:comment_id>/', views.comment_modify_answer, name='comment_modify_answer'),
    path('comment/delete/answer/<int:comment_id>/', views.comment_delete_answer, name='comment_delete_answer'),
]

'''
제너릭 뷰 url

from django.urls import path

from . import views

app_name = 'pybo'
urlpatterns = [
    path('', views.IndexView.as_view()),
    path('<int:pk>/', views.DetailView.as_view()),
]
'''