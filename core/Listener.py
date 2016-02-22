import json


class Listener():
    listerner = []

    client_websocket = {}

    def send_socket(self,Query):
        """
        отправляет коордитнаты сокетам
        :param Query: выборка из бд
        """
        live_client = []
        for socket in Query:
            client = self.client_websocket.get(socket.device_ID)
            if client is not None:
                json = self.create_JSON(socket.device_ID,
                                 socket.latitude,
                                 socket.longitude)

                client.send(json.encode())
                live_client.append(client)


    def create_JSON(self,device_ID,latitude,longitude):
        data = {'device_ID': device_ID, 'latitude': latitude, 'longitude': longitude}
        return json.dumps(data)


    def get_life_socket(self,Query):
        self.get_socket(Query)

    def setListener(self,model,socket):
        self.client_websocket.update({model:socket})






