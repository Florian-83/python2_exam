from django.shortcuts import render, redirect
from .models import User, Session, Answer


def login(request):
    return redirect("http://127.0.0.1:5000")

def teacher_view(request):
    var_users = User.objects.all()
    var_sessions = Session.objects.all()
    var_answers = Answer.objects.all()
    return render(request, 'teacher_view.html', {'answers': var_answers,'sessions': var_sessions,'users': var_users})

def student_list(request):
    var_students = User.objects.all()
    return render(request, 'student_list.html', {'students': var_students})

def session_list(request):
    var_sessions = Session.objects.all()    
    return render(request, 'session_list.html', {'sessions': var_sessions})

def answers_list(request):
    var_answers = Answer.objects.all()
    return render(request, 'answers_list.html', {'answers': var_answers})