from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework import permissions
from rest_framework.views import APIView
from django.contrib.auth.models import User
from core.models import Parent, Children
from rest_framework.authtoken.models import Token


class ChangeApi(APIView, permissions.BasePermission):
    def post(self, request):
        try:
            token = request.data['token']
            user_change = request.POST.get('user',False)
            if user_change is not False:
                try:
                    user = User.objects.get(username=user_change)
                    user_root = Token.objects.get(key=token).user
                    try:
                        if user_root.parent is not None:
                            self.change_user(request, user.children)
                    except:
                        print("только родителям доступно")
                except User.DoesNotExist:
                    print("not found")
            else:
                user_from_token = Token.objects.get(key=token).user
                user_change = None
                try:
                    user_change = user_from_token.children
                except Children.DoesNotExist:
                    user_change = user_from_token.parent
                self.change_user(request, user_change)
        except:
            pass
        pass

    def change_user(self, request, user):
        if request.POST.get('name', False):
            name_change = request.POST.get('name', False)
            user.name = name_change
        user.link_to_image = save_photo(request, user)
        user.save()


def save_photo(request, login_p):
    """
    сохраняет и возвращяет путь до фото
    :rtype: путь до фото
    """
    try:
        data = request.FILES['image']
        path = default_storage.save('image_user/{0}/image.jpeg'
                                    .format(login_p),
                                    ContentFile(data.read()))
    except:
        path = 'image_user/No_person.jpg'
    return path
