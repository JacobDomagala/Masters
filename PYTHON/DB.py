from pymongo import MongoClient

class DB:
     def __init__(self):
         self.client = MongoClient()
         db = self.client['baza']


