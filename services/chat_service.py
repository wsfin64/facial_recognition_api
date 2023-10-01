import requests


class ChatService:

    def __init__(self, modelo_name):
        self.__modelo_name = modelo_name
        self._chat_url = "https://chaturbate.com/api/chatvideocontext/"
        self._chat_url_bio_context = "https://chaturbate.com/api/biocontext/"

    def call_api(self):

        response = requests.get(f'{self._chat_url}{self.__modelo_name}')

        if response.ok:

            return response.json()


if __name__ == '__main__':

    chat = ChatService('gia_baker')

    chat_response = chat.call_api()

    print(chat_response)
