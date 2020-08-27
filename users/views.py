from django.shortcuts import render
from .forms import UserForm
from .models import User
from django.views.generic import View
from django.shortcuts import redirect


class AddUser(View):
    
    def get(self, request):
        form = UserForm()
        return render(request, "new_user.html", context={"form": form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("new_user")
        return render(request, "new_user.html", context={"form": form})