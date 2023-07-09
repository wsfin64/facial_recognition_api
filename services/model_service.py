from services.chat_service import ChatService


class ModelService:

    def __init__(self, model):
        self._model = model
        self.chat_service = ChatService(model)


    def check_model_status(self):
        response = self.chat_service.call_api()
        print(response)
        if response.get('room_status') == 'online':
            return True
        return False