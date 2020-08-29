from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import logout
from django.shortcuts import redirect


class Home(View):
    def get(self, request):
        user_authenticated = request.user.is_authenticated
        return render(request, "home.html", 
            context={'user_authenticated': user_authenticated,
                     'active_page': "home"})

def logout_view(request):
    logout(request)
    return redirect("main")