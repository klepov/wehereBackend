from django.contrib.auth.models import User
from django.shortcuts import render

from core.forms import Reg_child
from core.models import Children


class Reg:
    def __init__(self):
        self.POST = None

    def reg_child_form(request):
        if request.POST:
            form = Reg_child(request.POST)

            if form.is_valid():
                login = form.data['name_child']
                if not User.objects.filter(username=login):
                    password1 = form.data['password1']
                    password2 = form.data['password2']

                    if password1 == password2:
                        user = User.objects.create_user(username=login,
                                                        password=password1)
                        user.save()

                        children = Children(user=user)

                        children.save()

        form = Reg_child()

        return render(request, 'reg_child.html', {'form': form})
