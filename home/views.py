from .models import IntroInfo
from django.shortcuts import render
from django.views.generic import View


class HomeView(View):
    """
        View to show introductory info and availability
        of site functionality, depending on either user
        is authenticated or not.
    """

    def get(self, request):
        user_authenticated = request.user.is_authenticated
        show = True

        if user_authenticated:
            try:
                introinfo = IntroInfo.objects.filter(author=request.user).get()
                show = introinfo.show
            except IntroInfo.DoesNotExist:
                introinfo = IntroInfo(author=request.user)
                introinfo.save()
        return render(
            request,
            "home.html",
            context={
                "user_authenticated": user_authenticated,  # availability of site functionality
                "active_page": "home",  # separeate active and non active pages on navbar
                "show": show,  # show ot not introductory info
            },
        )
