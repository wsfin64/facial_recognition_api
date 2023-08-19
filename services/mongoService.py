import pymongo
from pymongo import MongoClient
import uuid


class MongoService(object):
    def __init__(self):
        self.cluster = MongoClient('localhost', 27017)
        self.db = self.cluster["facial-recognition"]
        self.individual_collection = self.db['individuals']
        self.recognition_collection = self.db['recognitionAnalysis']

    def save_individual(self, payload: dict) -> dict:
        payload['_id'] = payload.get('id')
        self.individual_collection.insert_one(payload)
        print({"model created": payload.get('id')})
        return payload

    def save_analysis(self, payload: dict) -> dict:
        print('Saving analysis')
        payload['_id'] = payload.get('processId')
        self.recognition_collection.insert_one(payload)

    def find_all_individuals(self):
        results = self.individual_collection.find()
        return [result for result in results]

    def find_individual_by_id(self, id):
        result = self.individual_collection.find_one({"id": id})

        return result

    def find_analysis_by_processId(self, processId):
        result = self.recognition_collection.find_one({"processId": processId})
        return result

    def update_analysis(self, payload: dict) -> dict:
        self.recognition_collection.update_one({"processId": payload.get("processId")}, {"$set": {"status": payload.get("status"), "modelsMatched": payload.get('modelsMatched')}})