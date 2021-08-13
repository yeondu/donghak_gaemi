from django.shortcuts import render, redirect

# Create your views here.
def home(request):
    user = request.user.is_authenticated # 사용자가 인증을 받았는지(로그인이 되어있는지)
    if user:
        return redirect('/tradingNote')
    else:
        return redirect('/sign-in')

def tradingNote(request):
    if request.method == 'GET':
        return render(request, 'tradingNote/home.html')