import json

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from core.models import Parent, Children


def get_list_relation(obj_some):
    """
    собирает все отношения
    :param obj_some: объект, для которого нужно собрать все отношения
    :return: список отношений
    """
    common_people = []
    obj_some = User.objects.get(username=obj_some)
    try:
        children = obj_some.parent.child.all()
        common_people.extend(children)
    except AttributeError:
        parent_child = obj_some.children.parent_set.all()
        children = obj_some.children.parent_set.get().child.all()
        common_people.extend(parent_child)
        common_people.extend(children)

    clear_self(common_people, obj_some)
    return common_people


def clear_self(common_people, obj_some):
    for i in range(len(common_people)):
        if (common_people[i].user == obj_some):
            common_people.pop(i)
            break


class Check():
    common_request = {}

    def user_leave(self, websocket):
        print("lol")
        pass

    def handler_socket(self, json, request):
        """
        делегирует управление
        :param json:входящий json
        :param request: сокет - соединение
        """

        # json = str(json_ss).replace("'",'"')
        print(json)

        method = json['method']
        print(method)
        if method == 'auth':

            self.__auth(json, request)

        elif method == 'update':
            user = self.__return_username(json)

            try:
                if user is None or self.common_request[user] is None:
                    request.websocket.send(self.__make_json_error("update", 5))
            except:
                request.websocket.send(self.__make_json_error("update", 6))

            self.__update(json)

        elif method == 'list_relation':

            user = self.__return_username(json)

            if user is not None:
                relation_list = self.__make_json_from_attribute_user(user)
                print("user ok")

            else:
                request.websocket.send(self.__make_json_error("list_relation", 6))
                print("user not")

            return request.websocket.send(relation_list)

    def __auth(self, json_received, request):

        """
        метод аутентификации
        :param json: аутентификации
        :param request: сокет - соединение
        :return: сообщение клиенту
        """
        user = self.__return_username(json_received)

        if user is not None:

            self.common_request.update({user: request})
            return request.websocket.send(self.__make_json_error("auth", 666))
        else:
            request.websocket.send(self.__make_json_error("auth", 6))

    def __return_username(self, json):
        """
        возращает юзера из БД
        :param json: json, где есть логин
        :return: возращает юзера из БД
        """
        try:
            user = Token.objects.get(key=json['data']['token']).user
        except:
            user = None

        return user

    def __update(self, json):

        """
        метод обновляет объект
        и отправляет его на оповещения подписанных участников
        :param json:пришедший с клиента
        """
        user = self.__return_username(json)

        if user is not None:

            try:
                obj_some = Parent.objects.get(user=user)
            except Parent.DoesNotExist:
                obj_some = Children.objects.get(user=user)

            # парсинг джсона
            device_ID, latitude, longitude = self.__parse_JSON(json)

            # обновление данных для модели
            self.__bind_user(device_ID, latitude, longitude, obj_some)

            obj_some.save()

            self.observer(obj_some)

    def __bind_user(self, device_ID, latitude, longitude, parent):
        """
        обновляет свойства у юзера
        :param IMEI:
        :param device_ID:
        :param latitude:
        :param longitude:
        :param parent:
        """
        parent.latitude = latitude
        parent.longitude = longitude
        parent.device_ID = device_ID

    def __parse_JSON(self, json):

        """
        парсинг на значение
        :param json: который нужно пропарсить
        :return: значения из json
        """
        latitude = json['data']['latitude']
        longitude = json['data']['longitude']
        device_ID = json['data']['device_ID']
        return device_ID, latitude, longitude

    def observer(self, obj_some):

        """
        оповещает подписчиков
        :param obj_some: юзер, который обновился
        """
        common_people = get_list_relation(obj_some)
        print(common_people)
        for i in common_people:

            try:
                request = self.common_request[i.user]

                request.websocket.send(self.__encode_JSON(obj_some))
            except KeyError:
                pass

    def __encode_JSON(self, user):
        """
        создание json
        :param user: юзер,для которого нужно сделать json
        :return: json
        """
        json_model = {}
        json_model["method"] = "update"
        json_model["data"] = self.__get_attribute_user(user)

        return json.dumps(json_model).encode()

    def __get_attribute_user(self, user):
        """
        выделяет свойства из юзера
        :param user:из которого нужно выделить свойство
        :return:словарь из значений юзера
        """
        data = {
            "latitude": user.latitude,
            "longitude": user.longitude,
            "device_ID": user.device_ID,
            "name": user.name,
            "link_to_image": user.link_to_image,
            "user": str(user)
        }
        return data

    # ответ на запрос
    def __make_json_from_attribute_user(self, users):
        """
        создает json из атрибутов юзера
        :param users: список отношений юзера
        :return: готовый json
        """
        relation = []
        data = {}
        for user in get_list_relation(users):
            relation.append(self.__get_attribute_user(user))

        data["method"] = "list_relation"
        data["data"] = relation

        return json.dumps(data).encode()

    def __make_json_error(self, method, code):
        json_model = {}
        json_model["method"] = method
        json_model["data"] = {"code": code}

        return json.dumps(json_model).encode()
