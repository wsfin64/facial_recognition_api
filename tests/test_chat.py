import unittest
from unittest import TestCase, mock
from unittest.mock import patch
from services.chat_service import ChatService
from services.model_service import ModelService


class TestChatAPi(TestCase):

    mocked_chat_response = {"room_status": "online", "age": 27, "broadcaster_username": "gia_baker"}

    @patch('services.chat_service.ChatService.call_api', return_value=mocked_chat_response)
    def test_api(self, chat_mocked):
        chat_service = ChatService('gia_baker')

        response = chat_service.call_api()

        self.assertEqual(response, self.mocked_chat_response)

    @patch('services.chat_service.ChatService.call_api', return_value=mocked_chat_response)
    def test_api_from_model(self, mocked_model):

        model = ModelService('annie_dreams')

        is_online = model.check_model_status()

        self.assertEqual(is_online, True)


if __name__ == '__main__':
    unittest.main()
