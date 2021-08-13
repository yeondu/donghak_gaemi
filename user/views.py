from django.shortcuts import render, redirect
from .models import UserModel
from django.http import HttpResponse
from django.contrib.auth import get_user_model # 사용자가 있는지 검사하는 함수
from django.contrib import auth # 사용자 auth 기능

def sign_up_view(request):
    if request.method == 'GET':
        return render(request, 'user/signup.html')
    elif request.method == 'POST':
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        password2 = request.POST.get('password2', None)
        name = request.POST.get('name', None)
        phone = request.POST.get('phone', None)
        birthdate = request.POST.get('birthdate', None)
        gender = request.POST.get('gender', None)

        if password != password2:
            return render(request, 'user/signup.html')
        else:
            exist_user = get_user_model().objects.filter(email=email)
            if exist_user:
                return render(request, 'user/signup.html') # 사용자가 존재하기 때문에 사용자를 저장하지 않고 회원가입 페이지를 다시 띄움
            else:
                UserModel.objects.create_user(email=email, password=password, name=name, phone=phone, birthdate=birthdate, gender=gender)
                return redirect('/sign-in') # 회원가입이 완료되었으므로 로그인 페이지로 이동

def sign_in_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)

        me = auth.authenticate(request, email=email, password=password)  # 사용자 불러오기
        if me is not None: # 저장된 사용자의 패스워드와 입력받은 패스워드 비교
            auth.login(request, me)
            return redirect('/')
        else: # 로그인이 실패하면 다시 로그인 페이지를 보여주기
            return redirect('/sign-in') # 로그인 실패
    elif request.method == 'GET':
        return render(request, 'user/signin.html')