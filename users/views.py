from django.shortcuts import render

def AddUser(request):
    return render(request, 'new_user.html')