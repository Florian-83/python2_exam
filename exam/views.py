from django.shortcuts import render, redirect
from .models import User, Session, Answer
import jwt

# Clé secrète
jwt_secret_key = "MAsuperclé"

def login(request):
    return redirect("http://127.0.0.1:5000")

def teacher_view(request):
    token = request.COOKIES.get('jwt')
    decode_token = jwt.decode(token, jwt_secret_key, algorithms=['HS256'])
    mail = decode_token.get('mail')
    teacher = User.objects.filter(mail=mail, is_teacher=True).first()

    if teacher.is_teacher == True:
        var_users = User.objects.all()
        var_sessions = Session.objects.all()
        var_answers = Answer.objects.all()
        return render(request, 'teacher_view.html', {'answers': var_answers,'sessions': var_sessions,'users': var_users, 'teacher':teacher})
    else:
        return redirect("http://127.0.0.1:5000")